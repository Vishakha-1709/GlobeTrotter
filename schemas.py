import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# --- USER SCHEMAS ---
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    base_currency: Optional[str] = "INR"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    base_currency: str
    avatar_url: Optional[str] = None
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# --- CITY & ACTIVITY SCHEMAS ---
class ActivityOut(BaseModel):
    id: int
    city_id: int
    name: str
    category: str
    estimated_cost: float
    duration_minutes: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CityOut(BaseModel):
    id: int
    name: str
    country: str
    region: Optional[str] = None
    latitude: float
    longitude: float
    cost_index: float
    popularity_score: float
    currency_code: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    activities: List[ActivityOut] = []

    class Config:
        from_attributes = True


# --- ITINERARY ITEM SCHEMAS ---
class ItineraryItemCreate(BaseModel):
    stop_id: int
    activity_id: Optional[int] = None
    custom_title: Optional[str] = None
    day_number: int = 1
    start_time: str = "10:00"
    duration_minutes: int = 120
    cost: float = 0.0
    notes: Optional[str] = None
    order_index: int = 0


class ItineraryItemOut(BaseModel):
    id: int
    stop_id: int
    activity_id: Optional[int] = None
    custom_title: Optional[str] = None
    day_number: int
    start_time: str
    duration_minutes: int
    cost: float
    order_index: int
    notes: Optional[str] = None
    is_completed: bool
    activity: Optional[ActivityOut] = None

    class Config:
        from_attributes = True


# --- TRIP STOP SCHEMAS ---
class TripStopCreate(BaseModel):
    city_id: Optional[int] = None
    custom_city_name: Optional[str] = None
    custom_country: Optional[str] = "India"
    arrival_date: datetime.date
    departure_date: datetime.date
    order_index: int = 0
    stop_budget: float = 0.0


class TripStopOut(BaseModel):
    id: int
    trip_id: int
    city_id: int
    arrival_date: datetime.date
    departure_date: datetime.date
    order_index: int
    stop_budget: float
    city: CityOut
    itinerary_items: List[ItineraryItemOut] = []

    class Config:
        from_attributes = True


# --- EXPENSE SCHEMAS ---
class ExpenseSplitCreate(BaseModel):
    member_name: str
    share_amount: float
    user_id: Optional[int] = None


class ExpenseSplitOut(BaseModel):
    id: int
    member_name: str
    share_amount: float

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    category: str = "Activities"
    description: str
    amount: float
    currency: str = "USD"
    expense_date: datetime.date
    paid_by_name: str = "Me"
    splits: List[ExpenseSplitCreate] = []


class ExpenseOut(BaseModel):
    id: int
    trip_id: int
    paid_by_name: str
    category: str
    description: str
    amount: float
    currency: str
    converted_amount: float
    expense_date: datetime.date
    splits: List[ExpenseSplitOut] = []

    class Config:
        from_attributes = True


# --- TRIP SCHEMAS ---
class TripMemberCreate(BaseModel):
    guest_name: str
    role: Optional[str] = "editor"


class TripMemberOut(BaseModel):
    id: int
    user_id: Optional[int] = None
    guest_name: Optional[str] = None
    role: str

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime.date
    end_date: datetime.date
    cover_image: Optional[str] = None
    total_budget: float = 0.0
    currency: str = "USD"
    is_public: bool = False


class TripSummaryOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_date: datetime.date
    end_date: datetime.date
    cover_image: Optional[str] = None
    total_budget: float
    currency: str
    is_public: bool
    share_slug: Optional[str] = None
    destination_count: int = 0
    total_spent: float = 0.0

    class Config:
        from_attributes = True


class TripDetailOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    start_date: datetime.date
    end_date: datetime.date
    cover_image: Optional[str] = None
    total_budget: float
    currency: str
    is_public: bool
    share_slug: Optional[str] = None
    created_at: datetime.datetime
    creator: UserOut
    stops: List[TripStopOut] = []
    expenses: List[ExpenseOut] = []
    members: List[TripMemberOut] = []

    class Config:
        from_attributes = True


# --- WOW FACTOR 1: GLOBESPLIT SCHEMAS ---
class GlobeSplitReport(BaseModel):
    base_currency: str
    total_trip_spent: float
    member_balances: Dict[str, float]
    settlement_transactions: List[Dict[str, Any]]


# --- WOW FACTOR 2: OPTIMIZER SCHEMAS ---
class DayOptimizeRequest(BaseModel):
    stop_id: int
    day_number: int


class DayOptimizeResponse(BaseModel):
    original_metrics: Dict[str, float]
    optimized_metrics: Dict[str, float]
    distance_saved_km: float
    time_saved_minutes: float
    optimized_items: List[Dict[str, Any]]


# --- ADMIN ANALYTICS SCHEMA (Screen 13) ---
class AdminAnalyticsOut(BaseModel):
    total_users: int
    total_trips: int
    total_itinerary_activities: int
    total_expenses_logged_usd: float
    top_destinations: List[Dict[str, Any]]
    popular_activity_categories: List[Dict[str, Any]]
