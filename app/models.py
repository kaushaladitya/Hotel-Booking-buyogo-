from sqlalchemy import Column, Integer, String, Boolean, Date, Float, ForeignKey, Double, ForeignKeyConstraint, TIMESTAMP, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HotelManagement(Base):
    __tablename__ = 'hotel_management'

    id = Column(Integer, primary_key=True)
    hotel = Column(String, nullable=False)
    is_canceled = Column(Boolean, nullable=False)
    lead_time = Column(Integer, nullable=False)
    arrival_date_year = Column(Integer, nullable=False)
    arrival_date_month = Column(String, nullable=False)
    arrival_date_week_number = Column(Integer, nullable=False)
    arrival_date_day_of_month = Column(Integer, nullable=False)
    stays_in_weekend_nights = Column(Integer, nullable=False)
    stays_in_week_nights = Column(Integer, nullable=False)
    adults = Column(Integer, nullable=False)
    children = Column(Integer, nullable=True)
    babies = Column(Integer, nullable=True)
    meal = Column(String, nullable=False)
    country = Column(String, nullable=True)
    market_segment = Column(String, nullable=False)
    distribution_channel = Column(String, nullable=False)
    is_repeated_guest = Column(Boolean, nullable=False)
    previous_cancellations = Column(Integer, nullable=False)
    previous_bookings_not_canceled = Column(Integer, nullable=False)
    reserved_room_type = Column(String, nullable=False)
    assigned_room_type = Column(String, nullable=False)
    booking_changes = Column(Integer, nullable=False)
    deposit_type = Column(String, nullable=False)
    agent = Column(String, nullable=True)
    company = Column(String, nullable=True)
    days_in_waiting_list = Column(Integer, nullable=False)
    customer_type = Column(String, nullable=False)
    adr = Column(Float, nullable=False)
    required_car_parking_spaces = Column(Integer, nullable=False)
    total_of_special_requests = Column(Integer, nullable=False)
    reservation_status = Column(String, nullable=False)
    reservation_status_date = Column(String, nullable=True)

class SearchHistory(Base):
    __tablename__ = 'search_history'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    query = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)