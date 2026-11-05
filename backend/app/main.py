import json,os
from fastapi import FastAPI,Depends,Header,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import Base,engine,get_db
from .models import Trip,Seat,Hold,BookingSeat,Booking
from .schemas import TripOut,HoldIn,PassengerIn
from .booking import create_hold,confirm,utc,now
Base.metadata.create_all(engine)
app=FastAPI(title='BusFlow API',version='0.1.0',description='College project bus booking demo')
app.add_middleware(CORSMiddleware,allow_origins=os.getenv('CORS_ORIGINS','http://localhost:3000').split(','),allow_methods=['*'],allow_headers=['*'])
@app.get('/health')
def health():return {'status':'ok','service':'busflow-api'}
@app.get('/api/v1/trips',response_model=list[TripOut])
def trips(origin:str|None=None,destination:str|None=None,db:Session=Depends(get_db)):
 q=select(Trip)
 if origin:q=q.where(Trip.origin.ilike(f'%{origin}%'))
 if destination:q=q.where(Trip.destination.ilike(f'%{destination}%'))
 return db.scalars(q.order_by(Trip.departure_at)).all()
@app.get('/api/v1/trips/{tid}/seats')
def seats(tid:str,db:Session=Depends(get_db)):
 if not db.get(Trip,tid):raise HTTPException(404,'Trip not found')
 rows=db.scalars(select(Seat).where(Seat.trip_id==tid).order_by(Seat.seat_number)).all()
 holds=db.scalars(select(Hold).where(Hold.trip_id==tid,Hold.status=='held')).all();held=set()
 for h in holds:
  if utc(h.expires_at)>now():held.update(json.loads(h.seat_ids))
 booked=set(db.scalars(select(BookingSeat.seat_id).where(BookingSeat.trip_id==tid)).all())
 return [{'id':s.id,'seat_number':s.seat_number,'seat_type':s.seat_type,'status':'booked' if s.id in booked else 'held' if s.id in held else 'available'} for s in rows]
@app.post('/api/v1/holds',status_code=201)
def holds(data:HoldIn,idempotency_key:str=Header(...,alias='Idempotency-Key'),db:Session=Depends(get_db)):
 h=create_hold(db,data.trip_id,data.seat_ids,data.owner_token,idempotency_key)
 return {'id':h.id,'status':h.status,'expires_at':h.expires_at,'seat_ids':json.loads(h.seat_ids)}
@app.post('/api/v1/holds/{hid}/confirm')
def confirmation(hid:str,data:PassengerIn,db:Session=Depends(get_db)):
 b=confirm(db,hid,data);return {'pnr':b.pnr,'status':b.status,'trip_id':b.trip_id,'passenger_name':b.passenger_name,'seat_ids':json.loads(b.seat_ids),'total_paise':b.total_paise,'created_at':b.created_at}
@app.get('/api/v1/bookings/{pnr}')
def lookup(pnr:str,db:Session=Depends(get_db)):
 b=db.scalar(select(Booking).where(Booking.pnr==pnr.upper()))
 if not b:raise HTTPException(404,'Booking not found')
 return {'pnr':b.pnr,'status':b.status,'trip_id':b.trip_id,'passenger_name':b.passenger_name,'seat_ids':json.loads(b.seat_ids),'total_paise':b.total_paise,'created_at':b.created_at}
