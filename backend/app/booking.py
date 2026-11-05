import hashlib,json,os,secrets
from datetime import datetime,timedelta,timezone
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import Trip,Seat,Hold,Booking,BookingSeat
TTL=int(os.getenv('HOLD_TTL_SECONDS','300'))
def now(): return datetime.now(timezone.utc)
def utc(v): return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v.astimezone(timezone.utc)
def create_hold(db:Session,trip_id:str,seat_ids:list[str],owner:str,key:str):
 if not key or len(key)>120: raise HTTPException(400,'A valid Idempotency-Key is required')
 ids=sorted(set(seat_ids))
 if len(ids)!=len(seat_ids): raise HTTPException(422,'Duplicate seat IDs')
 digest=hashlib.sha256(json.dumps([trip_id,ids,owner]).encode()).hexdigest()
 old=db.scalar(select(Hold).where(Hold.idempotency_key==key))
 if old:
  if old.payload_hash!=digest: raise HTTPException(409,'Idempotency key reused with different request')
  return old
 if not db.get(Trip,trip_id): raise HTTPException(404,'Trip not found')
 seats=db.scalars(select(Seat).where(Seat.trip_id==trip_id,Seat.id.in_(ids)).order_by(Seat.id).with_for_update()).all()
 if len(seats)!=len(ids): raise HTTPException(404,'Seat does not belong to trip')
 booked=set(db.scalars(select(BookingSeat.seat_id).where(BookingSeat.trip_id==trip_id,BookingSeat.seat_id.in_(ids))).all())
 active=db.scalars(select(Hold).where(Hold.trip_id==trip_id,Hold.status=='held')).all();held=set();stamp=now()
 for h in active:
  if utc(h.expires_at)>stamp: held.update(json.loads(h.seat_ids))
  else: h.status='expired'
 if booked.intersection(ids) or held.intersection(ids): db.rollback();raise HTTPException(409,'Seat is no longer available')
 h=Hold(id=str(uuid4()),trip_id=trip_id,owner_token=owner,seat_ids=json.dumps(ids),idempotency_key=key,payload_hash=digest,status='held',expires_at=stamp+timedelta(seconds=TTL))
 db.add(h)
 try: db.commit()
 except IntegrityError:
  db.rollback();old=db.scalar(select(Hold).where(Hold.idempotency_key==key))
  if old and old.payload_hash==digest:return old
  raise HTTPException(409,'Concurrent seat hold conflict; refresh seats')
 db.refresh(h);return h
def confirm(db:Session,hid:str,data):
 h=db.scalar(select(Hold).where(Hold.id==hid).with_for_update())
 if not h:raise HTTPException(404,'Hold not found')
 if h.status=='confirmed' and h.booking_id:return db.get(Booking,h.booking_id)
 if h.owner_token!=data.owner_token:raise HTTPException(403,'Hold owner mismatch')
 if h.status!='held' or utc(h.expires_at)<=now():
  if h.status=='held':h.status='expired'
  db.commit();raise HTTPException(410,'Hold expired; choose seats again')
 trip=db.get(Trip,h.trip_id);ids=json.loads(h.seat_ids);bid=str(uuid4())
 b=Booking(id=bid,pnr=secrets.token_hex(4).upper(),trip_id=h.trip_id,passenger_name=data.passenger_name,email=data.email,phone=data.phone,seat_ids=h.seat_ids,total_paise=trip.fare_paise*len(ids),status='confirmed')
 db.add(b)
 for sid in ids:db.add(BookingSeat(id=str(uuid4()),trip_id=h.trip_id,seat_id=sid,booking_id=bid))
 h.status='confirmed';h.booking_id=bid
 try:db.commit()
 except IntegrityError:db.rollback();raise HTTPException(409,'Seat already booked; refresh availability')
 db.refresh(b);return b
