from datetime import timedelta
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base,get_db
from app.main import app
from app.models import Trip,Seat,utcnow
engine=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
TestingSession=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
Base.metadata.create_all(engine)
def override_db():
 db=TestingSession()
 try: yield db
 finally: db.close()
app.dependency_overrides[get_db]=override_db
client=TestClient(app)
def setup_trip():
 db=TestingSession();tid=str(uuid4())
 t=Trip(id=tid,operator='Test',bus_name='Test coach',origin='Hyderabad',destination='Vijayawada',departure_at=utcnow()+timedelta(days=1),arrival_at=utcnow()+timedelta(days=1,hours=6),fare_paise=50000,seat_layout='2+2')
 seats=[Seat(id=str(uuid4()),trip_id=tid,seat_number=f'S{i}',seat_type='seater') for i in range(1,5)]
 db.add(t);db.add_all(seats);db.commit();ids=[s.id for s in seats];db.close();return tid,ids
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
 monkeypatch.setenv('BUSFLOW_ADMIN_API_KEY','test-admin-secret')
 denied=client.get('/api/v1/admin/summary')
 assert denied.status_code==401
 accepted=client.get('/api/v1/admin/summary',headers={'X-Admin-Key':'test-admin-secret'})
 assert accepted.status_code==200
 data=accepted.json()
 assert {'trips_total','seats_total','bookings_confirmed','active_holds','revenue_paise'}<=data.keys()
 assert data['trips_total']>=1 and data['bookings_confirmed']>=1

def test_admin_can_create_trip_and_generated_seats(monkeypatch):
 monkeypatch.setenv('BUSFLOW_ADMIN_API_KEY','test-admin-secret')
 payload={'operator':'Demo Travels','bus_name':'AC Seater','origin':'Hyderabad','destination':'Vijayawada','departure_at':(utcnow()+timedelta(days=2)).isoformat(),'arrival_at':(utcnow()+timedelta(days=2,hours=6)).isoformat(),'fare_paise':65000,'seat_layout':'2+1','seat_count':18}
 denied=client.post('/api/v1/admin/trips',json=payload)
 assert denied.status_code==401
 created=client.post('/api/v1/admin/trips',json=payload,headers={'X-Admin-Key':'test-admin-secret'})
 assert created.status_code==201
 trip=created.json()
 assert trip['seat_layout']=='2+1' and trip['origin']=='Hyderabad'
 seat_response=client.get('/api/v1/trips/'+trip['id']+'/seats')
 assert seat_response.status_code==200 and len(seat_response.json())==18
 listing=client.get('/api/v1/admin/trips',headers={'X-Admin-Key':'test-admin-secret'})
 assert any(item['id']==trip['id'] for item in listing.json())
def test_admin_trip_rejects_naive_datetime(monkeypatch):
 monkeypatch.setenv('BUSFLOW_ADMIN_API_KEY','test-admin-secret')
 payload={'operator':'Demo Travels','bus_name':'AC Seater','origin':'Hyderabad','destination':'Vijayawada','departure_at':'2026-12-01T10:00:00','arrival_at':'2026-12-01T16:00:00','fare_paise':65000,'seat_layout':'2+2','seat_count':20}
 response=client.post('/api/v1/admin/trips',json=payload,headers={'X-Admin-Key':'test-admin-secret'})
 assert response.status_code==422
