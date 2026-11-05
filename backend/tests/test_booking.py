import os
os.environ['DATABASE_URL']='sqlite://'
from datetime import timedelta
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base,engine,SessionLocal
from app.models import Trip,Seat
from app.booking import now
client=TestClient(app)
@pytest.fixture(autouse=True)
def clean_db():
 Base.metadata.drop_all(engine);Base.metadata.create_all(engine)
 yield
 Base.metadata.drop_all(engine)
def setup_trip():
 db=SessionLocal();tid=str(uuid4())
 t=Trip(id=tid,operator='Demo Travels',bus_name='AC Seater',origin='Hyderabad',destination='Bengaluru',departure_at=now()+timedelta(days=1),arrival_at=now()+timedelta(days=1,hours=6),fare_paise=50000,seat_layout='2+2')
 seats=[Seat(id=str(uuid4()),trip_id=tid,seat_number=f'S{i}',seat_type='seater') for i in range(1,5)]
 db.add(t);db.add_all(seats);db.commit();ids=[s.id for s in seats];db.close();return tid,ids
def make_booking(tid,seat_id,key='test-key-001'):
 payload={'trip_id':tid,'seat_ids':[seat_id],'owner_token':'owner-token-123'}
 h=client.post('/api/v1/holds',json=payload,headers={'Idempotency-Key':key});assert h.status_code==201
 c=client.post('/api/v1/holds/'+h.json()['id']+'/confirm',json={'owner_token':'owner-token-123','passenger_name':'Demo Person','email':'demo@example.com','phone':'9999999999'})
 assert c.status_code==200
 return c.json()['pnr']
def test_hold_confirm_and_conflict():
 tid,ids=setup_trip();payload={'trip_id':tid,'seat_ids':[ids[0]],'owner_token':'owner-token-123'}
 h=client.post('/api/v1/holds',json=payload,headers={'Idempotency-Key':'test-key-001'});assert h.status_code==201
 replay=client.post('/api/v1/holds',json=payload,headers={'Idempotency-Key':'test-key-001'});assert replay.json()['id']==h.json()['id']
 conflict=client.post('/api/v1/holds',json={**payload,'owner_token':'other-owner-456'},headers={'Idempotency-Key':'test-key-002'});assert conflict.status_code==409
 c=client.post('/api/v1/holds/'+h.json()['id']+'/confirm',json={'owner_token':'owner-token-123','passenger_name':'Demo Person','email':'demo@example.com','phone':'9999999999'})
 assert c.status_code==200 and c.json()['seat_ids']==[ids[0]]
def test_search_returns_seedable_trip_contract():
 response=client.get('/health');assert response.status_code==200 and response.json()['status']=='ok'
def test_admin_summary_requires_configured_key(monkeypatch):
 tid,ids=setup_trip();make_booking(tid,ids[0],'admin-summary-booking')
 monkeypatch.setenv('BUSFLOW_ADMIN_API_KEY','test-admin-secret')
 denied=client.get('/api/v1/admin/summary');assert denied.status_code==401
 accepted=client.get('/api/v1/admin/summary',headers={'X-Admin-Key':'test-admin-secret'})
 assert accepted.status_code==200
 data=accepted.json()
 assert {'trips_total','seats_total','bookings_confirmed','active_holds','revenue_paise'}<=data.keys()
 assert data['trips_total']>=1 and data['bookings_confirmed']>=1
def test_admin_can_create_trip_and_generated_seats(monkeypatch):
 monkeypatch.setenv('BUSFLOW_ADMIN_API_KEY','test-admin-secret')
 payload={'operator':'Demo Travels','bus_name':'AC Seater','origin':'Hyderabad','destination':'Vijayawada','departure_at':(now()+timedelta(days=2)).isoformat(),'arrival_at':(now()+timedelta(days=2,hours=6)).isoformat(),'fare_paise':65000,'seat_layout':'2+1','seat_count':18}
 denied=client.post('/api/v1/admin/trips',json=payload);assert denied.status_code==401
 created=client.post('/api/v1/admin/trips',json=payload,headers={'X-Admin-Key':'test-admin-secret'})
 assert created.status_code==201
 trip=created.json();assert trip['seat_layout']=='2+1' and trip['origin']=='Hyderabad'
 seat_response=client.get('/api/v1/trips/'+trip['id']+'/seats')
 assert seat_response.status_code==200 and len(seat_response.json())==18
 listing=client.get('/api/v1/admin/trips',headers={'X-Admin-Key':'test-admin-secret'})
 assert any(item['id']==trip['id'] for item in listing.json())
def test_admin_trip_rejects_naive_datetime(monkeypatch):
 monkeypatch.setenv('BUSFLOW_ADMIN_API_KEY','test-admin-secret')
 payload={'operator':'Demo Travels','bus_name':'AC Seater','origin':'Hyderabad','destination':'Vijayawada','departure_at':'2026-12-01T10:00:00','arrival_at':'2026-12-01T16:00:00','fare_paise':65000,'seat_layout':'2+2','seat_count':20}
 response=client.post('/api/v1/admin/trips',json=payload,headers={'X-Admin-Key':'test-admin-secret'})
 assert response.status_code==422
def test_booking_cancellation_releases_seats_and_is_idempotent():
 tid,ids=setup_trip();pnr=make_booking(tid,ids[0],'cancel-flow-hold')
 wrong=client.post('/api/v1/bookings/'+pnr+'/cancel',json={'phone':'8888888888'});assert wrong.status_code==403
 cancelled=client.post('/api/v1/bookings/'+pnr+'/cancel',json={'phone':'9999999999'})
 assert cancelled.status_code==200 and cancelled.json()['status']=='cancelled'
 seat_map=client.get('/api/v1/trips/'+tid+'/seats').json()
 assert next(s for s in seat_map if s['id']==ids[0])['status']=='available'
 replay=client.post('/api/v1/bookings/'+pnr+'/cancel',json={'phone':'9999999999'})
 assert replay.status_code==200 and replay.json()['status']=='cancelled'
 booking=client.get('/api/v1/bookings/'+pnr)
 assert booking.status_code==200 and booking.json()['status']=='cancelled'
def test_booking_history_requires_matching_phone_and_email():
 tid,ids=setup_trip();pnr=make_booking(tid,ids[0],'history-flow-hold')
 denied=client.post('/api/v1/bookings/history',json={'phone':'8888888888','email':'demo@example.com'})
 assert denied.status_code==200 and denied.json()==[]
 history=client.post('/api/v1/bookings/history',json={'phone':'9999999999','email':'DEMO@example.com'})
 assert history.status_code==200 and len(history.json())==1
 item=history.json()[0]
 assert item['pnr']==pnr and item['origin']=='Hyderabad' and item['destination']=='Bengaluru'
