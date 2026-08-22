import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, Table
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    base_currency = Column(String(10), default="INR")  # INR, USD, EUR, GBP, JPY
    avatar_url = Column(String(500), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    trips = relationship("Trip", back_populates="creator", cascade="all, delete-orphan")
    expense_splits = relationship("ExpenseSplit", back_populates="user")
    memberships = relationship("TripMember", back_populates="user")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    cover_image = Column(String(500), nullable=True)
    total_budget = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")
    is_public = Column(Boolean, default=False)
    share_slug = Column(String(64), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="trips")
    stops = relationship("TripStop", back_populates="trip", order_by="TripStop.order_index", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")
    members = relationship("TripMember", back_populates="trip", cascade="all, delete-orphan")


class TripMember(Base):
    """Associates travelers/friends with a trip for group collaboration and expense sharing."""
    __tablename__ = "trip_members"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    guest_name = Column(String(100), nullable=True)  # in case a friend isn't a registered user
    role = Column(String(20), default="editor")      # owner, editor, viewer

    trip = relationship("Trip", back_populates="members")
    user = relationship("User", back_populates="memberships")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    country = Column(String(100), index=True, nullable=False)
    region = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    cost_index = Column(Float, default=1.0)          # 1.0 = average, 1.5 = expensive, 0.7 = cheap
    popularity_score = Column(Float, default=80.0)
    currency_code = Column(String(10), default="USD")
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    activities = relationship("Activity", back_populates="city", cascade="all, delete-orphan")
    stops = relationship("TripStop", back_populates="city")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(50), default="Sightseeing")  # Sightseeing, Food, Adventure, Culture, Nightlife
    estimated_cost = Column(Float, default=0.0)
    duration_minutes = Column(Integer, default=120)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    city = relationship("City", back_populates="activities")
    itinerary_items = relationship("ItineraryItem", back_populates="activity")


class TripStop(Base):
    """Represents a city destination within a multi-city trip."""
    __tablename__ = "trip_stops"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    order_index = Column(Integer, default=0)
    stop_budget = Column(Float, default=0.0)

    trip = relationship("Trip", back_populates="stops")
    city = relationship("City", back_populates="stops")
    itinerary_items = relationship(
        "ItineraryItem", back_populates="stop",
        order_by="ItineraryItem.order_index",
        cascade="all, delete-orphan"
    )


class ItineraryItem(Base):
    """Represents a specific activity scheduled on a day within a city stop."""
    __tablename__ = "itinerary_items"

    id = Column(Integer, primary_key=True, index=True)
    stop_id = Column(Integer, ForeignKey("trip_stops.id", ondelete="CASCADE"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    custom_title = Column(String(200), nullable=True)
    day_number = Column(Integer, default=1)           # Day 1, Day 2, etc. of the stop
    start_time = Column(String(10), default="10:00")  # "10:00 AM"
    duration_minutes = Column(Integer, default=120)
    cost = Column(Float, default=0.0)
    order_index = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    stop = relationship("TripStop", back_populates="itinerary_items")
    activity = relationship("Activity", back_populates="itinerary_items")


class Expense(Base):
    """Tracks financial records for budget breakdowns and group expense settlement."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    paid_by_name = Column(String(100), default="Me")
    category = Column(String(50), default="Activities")  # Stay, Transport, Meals, Activities, Shopping, Other
    description = Column(String(250), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    converted_amount = Column(Float, nullable=False)      # normalized to trip base currency
    expense_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete-orphan")


class ExpenseSplit(Base):
    """Represents who owes what share of an individual expense."""
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    member_name = Column(String(100), nullable=False)
    share_amount = Column(Float, nullable=False)

    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")
