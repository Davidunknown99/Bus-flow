from datetime import datetime,timezone
from sqlalchemy import String,Integer,DateTime,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from .db import Base
def utcnow(): return datetime.now(timezone.utc)
class Trip(Base):
 __tablename__='trips'
 id:Mapped[str]=mapped_column(String(36),primary_key=True)
 operator:Mapped[str]=mapped_column(String(100)); bus_name:Mapped[str]=mapped_column(String(120))
 origin:Mapped[str]=mapped_column(String(80),index=True); destination:Mapped[str]=mapped_column(String(80),index=True)
 departure_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); arrival_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
 fare_paise:Mapped[int]=mapped_column(Integer); seat_layout:Mapped[str]=mapped_column(String(20),default='2+2')
class Seat(Base):
 __tablename__='seats'; __table_args__=(UniqueConstraint('trip_id','seat_number',name='uq_trip_seat_number'),)
 id:Mapped[str]=mapped_column(String(36),primary_key=True); trip_id:Mapped[str]=mapped_column(ForeignKey('trips.id'),index=True)
 seat_number:Mapped[str]=mapped_column(String(12)); seat_type:Mapped[str]=mapped_column(String(20),default='seater')
class Hold(Base):
 __tablename__='holds'
 id:Mapped[str]=mapped_column(String(36),primary_key=True); trip_id:Mapped[str]=mapped_column(ForeignKey('trips.id'),index=True)
 owner_token:Mapped[str]=mapped_column(String(80)); seat_ids:Mapped[str]=mapped_column(String(2000)); idempotency_key:Mapped[str]=mapped_column(String(120),unique=True)
 payload_hash:Mapped[str]=mapped_column(String(64)); status:Mapped[str]=mapped_column(String(20),default='held',index=True)
 expires_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); booking_id:Mapped[str|None]=mapped_column(String(36),nullable=True)
class Booking(Base):
 __tablename__='bookings'
 id:Mapped[str]=mapped_column(String(36),primary_key=True); pnr:Mapped[str]=mapped_column(String(12),unique=True,index=True)
 trip_id:Mapped[str]=mapped_column(ForeignKey('trips.id')); passenger_name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(254)); phone:Mapped[str]=mapped_column(String(20))
 seat_ids:Mapped[str]=mapped_column(String(2000)); total_paise:Mapped[int]=mapped_column(Integer); status:Mapped[str]=mapped_column(String(20),default='confirmed'); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
class BookingSeat(Base):
 __tablename__='booking_seats'; __table_args__=(UniqueConstraint('trip_id','seat_id',name='uq_confirmed_trip_seat'),)
 id:Mapped[str]=mapped_column(String(36),primary_key=True); trip_id:Mapped[str]=mapped_column(ForeignKey('trips.id'),index=True); seat_id:Mapped[str]=mapped_column(ForeignKey('seats.id')); booking_id:Mapped[str]=mapped_column(ForeignKey('bookings.id'),index=True)
