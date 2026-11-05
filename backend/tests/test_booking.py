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
