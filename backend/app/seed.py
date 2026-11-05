from datetime import datetime,timedelta,timezone
from uuid import uuid4
from .db import Base,engine,SessionLocal
from .models import Trip,Seat
Base.metadata.create_all(engine); db=SessionLocal()
try:
 if db.query(Trip).count()==0:
  today=datetime.now(timezone.utc).date()
  rows=[('Metro Travels','Volvo AC Sleeper','Hyderabad','Bengaluru',21,9,149900,'sleeper'),('Orange Express','AC Semi Sleeper','Hyderabad','Vijayawada',7,6,79900,'2+2'),('Kaveri Lines','BharatBenz Sleeper','Hyderabad','Chennai',22,10,129900,'sleeper')]
  for i,(op,bus,src,dst,hour,duration,fare,layout) in enumerate(rows):
   day=today+timedelta(days=i+1); dep=datetime(day.year,day.month,day.day,hour,tzinfo=timezone.utc); tid=str(uuid4())
   db.add(Trip(id=tid,operator=op,bus_name=bus,origin=src,destination=dst,departure_at=dep,arrival_at=dep+timedelta(hours=duration),fare_paise=fare,seat_layout=layout))
   for n in range(1,25): db.add(Seat(id=str(uuid4()),trip_id=tid,seat_number=('L' if layout=='sleeper' else 'S')+str(n).zfill(2),seat_type=layout))
  db.commit()
finally: db.close()
