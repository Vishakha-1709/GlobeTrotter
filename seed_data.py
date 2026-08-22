import datetime
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
from auth import get_password_hash
from debt_engine import convert_currency


def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Check if demo user exists
    demo_user = db.query(models.User).filter(models.User.email == "alex@globetrotter.com").first()
    if not demo_user:
        demo_user = models.User(
            name="Alex River",
            email="alex@globetrotter.com",
            password_hash=get_password_hash("password123"),
            base_currency="INR",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
            is_admin=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

    # 2. Seed World Cities
    cities_data = [
        {
            "name": "Paris",
            "country": "France",
            "region": "Europe",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "cost_index": 1.4,
            "popularity_score": 98.5,
            "currency_code": "EUR",
            "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
            "description": "The City of Light, renowned for art, fashion, gastronomy, and world-class architecture.",
            "activities": [
                {"name": "Eiffel Tower Summit Tour", "category": "Sightseeing", "estimated_cost": 38.0, "duration_minutes": 150, "lat": 48.8584, "lng": 2.2945, "image_url": "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=600", "description": "Iconic panoramic views of Paris from the 3rd floor summit."},
                {"name": "Louvre Museum Guided Walk", "category": "Culture", "estimated_cost": 45.0, "duration_minutes": 180, "lat": 48.8606, "lng": 2.3376, "image_url": "https://images.unsplash.com/photo-1565099824688-e93eb20fe622?w=600", "description": "Home to the Mona Lisa and centuries of masterworks."},
                {"name": "Seine River Sunset Cruise", "category": "Sightseeing", "estimated_cost": 22.0, "duration_minutes": 75, "lat": 48.8580, "lng": 2.2960, "image_url": "https://images.unsplash.com/photo-1549144511-f099e773c147?w=600", "description": "Breathtaking boat tour passing Notre-Dame and historic bridges."},
                {"name": "Montmartre & Sacré-Cœur Food Tour", "category": "Food", "estimated_cost": 65.0, "duration_minutes": 180, "lat": 48.8867, "lng": 2.3431, "image_url": "https://images.unsplash.com/photo-1509299349698-dd22323b5963?w=600", "description": "Pastry, cheese, and wine tasting in the bohemian artist quarter."}
            ]
        },
        {
            "name": "Rome",
            "country": "Italy",
            "region": "Europe",
            "latitude": 41.9028,
            "longitude": 12.4964,
            "cost_index": 1.2,
            "popularity_score": 96.0,
            "currency_code": "EUR",
            "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
            "description": "The Eternal City, where millennia of history, ancient ruins, and gelato collide.",
            "activities": [
                {"name": "Colosseum & Roman Forum", "category": "Sightseeing", "estimated_cost": 40.0, "duration_minutes": 180, "lat": 41.8902, "lng": 12.4922, "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=600", "description": "Explore the grand gladiator arena and heart of Ancient Rome."},
                {"name": "Vatican Museums & Sistine Chapel", "category": "Culture", "estimated_cost": 48.0, "duration_minutes": 210, "lat": 41.9067, "lng": 12.4534, "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=600", "description": "Michelangelo's masterpiece ceiling and papal art treasures."},
                {"name": "Trevi Fountain & Spanish Steps Walk", "category": "Sightseeing", "estimated_cost": 0.0, "duration_minutes": 90, "lat": 41.9009, "lng": 12.4833, "image_url": "https://images.unsplash.com/photo-1531572753322-ad063cecc140?w=600", "description": "Toss a coin into the Trevi fountain and explore charming piazzas."},
                {"name": "Trastevere Street Food & Wine Crawl", "category": "Food", "estimated_cost": 55.0, "duration_minutes": 150, "lat": 41.8887, "lng": 12.4704, "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600", "description": "Crispy supplì, Roman pizza, and local Frascati wines."}
            ]
        },
        {
            "name": "Tokyo",
            "country": "Japan",
            "region": "Asia",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "cost_index": 1.3,
            "popularity_score": 97.0,
            "currency_code": "JPY",
            "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800",
            "description": "Ultra-modern neon skyscrapers harmoniously paired with timeless temples.",
            "activities": [
                {"name": "Shibuya Crossing & Hachiko Statue", "category": "Sightseeing", "estimated_cost": 0.0, "duration_minutes": 60, "lat": 35.6595, "lng": 139.7004, "image_url": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=600", "description": "Experience the world's busiest pedestrian intersection."},
                {"name": "Senso-ji Temple & Asakusa Market", "category": "Culture", "estimated_cost": 15.0, "duration_minutes": 120, "lat": 35.7148, "lng": 139.7967, "image_url": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=600", "description": "Tokyo's oldest Buddhist temple surrounded by vibrant snack stalls."},
                {"name": "teamLab Planets Digital Art", "category": "Adventure", "estimated_cost": 32.0, "duration_minutes": 120, "lat": 35.6496, "lng": 139.7898, "image_url": "https://images.unsplash.com/photo-1538991383142-36c4edeedebe?w=600", "description": "Immersive walk-through digital art museum."},
                {"name": "Tsukiji Outer Market Food Tour", "category": "Food", "estimated_cost": 50.0, "duration_minutes": 120, "lat": 35.6655, "lng": 139.7707, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600", "description": "Fresh sashimi, tamagoyaki, wagyu skewers, and matcha."}
            ]
        },
        {
            "name": "New York City",
            "country": "USA",
            "region": "North America",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "cost_index": 1.6,
            "popularity_score": 95.0,
            "currency_code": "USD",
            "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800",
            "description": "The city that never sleeps, filled with Broadway shows, skyline views, and Central Park.",
            "activities": [
                {"name": "Central Park Bike Tour", "category": "Adventure", "estimated_cost": 35.0, "duration_minutes": 120, "lat": 40.785091, "lng": -73.968285, "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600", "description": "Pedal through Bethesda Terrace, Strawberry Fields, and Bow Bridge."},
                {"name": "Summit One Vanderbilt Observation", "category": "Sightseeing", "estimated_cost": 49.0, "duration_minutes": 90, "lat": 40.7527, "lng": -73.9772, "image_url": "https://images.unsplash.com/photo-1518235506717-e1ed3306a89b?w=600", "description": "Glass-floor views overlooking the Chrysler Building and Empire State."},
                {"name": "Broadway Musical Show", "category": "Culture", "estimated_cost": 120.0, "duration_minutes": 150, "lat": 40.7590, "lng": -73.9845, "image_url": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=600", "description": "World-class musical theater in the heart of Times Square."}
            ]
        },
        {
            "name": "Barcelona",
            "country": "Spain",
            "region": "Europe",
            "latitude": 41.3879,
            "longitude": 2.1699,
            "cost_index": 1.1,
            "popularity_score": 94.0,
            "currency_code": "EUR",
            "image_url": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800",
            "description": "Gaudí architecture, Mediterranean beachfront, and lively tapas bars.",
            "activities": [
                {"name": "Sagrada Família Basilica Tour", "category": "Culture", "estimated_cost": 36.0, "duration_minutes": 120, "lat": 41.4036, "lng": 2.1744, "image_url": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=600", "description": "Antoni Gaudí's unfinished architectural marvel."},
                {"name": "Park Güell Panoramic Views", "category": "Sightseeing", "estimated_cost": 18.0, "duration_minutes": 90, "lat": 41.4145, "lng": 2.1527, "image_url": "https://images.unsplash.com/photo-1523531294919-4bcd7c65e216?w=600", "description": "Vibrant mosaic benches overlooking the Mediterranean sea."}
            ]
        },
        {
            "name": "Bengaluru",
            "country": "India",
            "region": "Asia",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "cost_index": 0.8,
            "popularity_score": 97.0,
            "currency_code": "INR",
            "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=800",
            "description": "The Garden City and Silicon Valley of India, known for lush parks, palaces, and craft microbreweries.",
            "activities": [
                {"name": "Bangalore Palace Royal Heritage Walk", "category": "Culture", "estimated_cost": 250.0, "duration_minutes": 120, "lat": 12.9988, "lng": 77.5921, "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600", "description": "Tudor-style royal estate with vintage royal artifacts."},
                {"name": "Lalbagh Botanical Garden & Glass House", "category": "Sightseeing", "estimated_cost": 50.0, "duration_minutes": 120, "lat": 12.9507, "lng": 77.5848, "image_url": "https://images.unsplash.com/photo-1600100397608-f010f443b236?w=600", "description": "Historic 240-acre botanical garden founded by Hyder Ali."},
                {"name": "Cubbon Park & Vidhana Soudha Walk", "category": "Sightseeing", "estimated_cost": 0.0, "duration_minutes": 90, "lat": 12.9763, "lng": 77.5929, "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=600", "description": "Lush green lung of the city facing Karnataka's grand legislative palace."},
                {"name": "Indiranagar Craft Microbrewery & Street Food Crawl", "category": "Food", "estimated_cost": 1200.0, "duration_minutes": 180, "lat": 12.9784, "lng": 77.6408, "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600", "description": "Artisan craft beer, dosa tastings, and vibrant pub culture."},
                {"name": "Nandi Hills Sunrise & Hilltop Cloud View", "category": "Adventure", "estimated_cost": 300.0, "duration_minutes": 240, "lat": 13.3702, "lng": 77.6835, "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600", "description": "Iconic sunrise above the clouds and historic Tipu Sultan fort."},
                {"name": "Bannerghatta Biological Park Tiger & Lion Safari", "category": "Adventure", "estimated_cost": 650.0, "duration_minutes": 210, "lat": 12.8009, "lng": 77.5777, "image_url": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=600", "description": "Wilderness safari, rescue center, and India's first butterfly park."},
                {"name": "ISKCON Temple Rajajinagar Spiritual Tour", "category": "Culture", "estimated_cost": 0.0, "duration_minutes": 90, "lat": 13.0098, "lng": 77.5511, "image_url": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=600", "description": "Grand neo-classical Dravidian temple complex with evening kirtans."},
                {"name": "Commercial Street & Brigade Road Shopping", "category": "Shopping", "estimated_cost": 1500.0, "duration_minutes": 150, "lat": 12.9822, "lng": 77.6083, "image_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=600", "description": "Bustling retail hub with silks, spices, and trendy fashion boutiques."},
                {"name": "VV Puram Food Street Midnight Dosa Trail", "category": "Food", "estimated_cost": 350.0, "duration_minutes": 120, "lat": 12.9515, "lng": 77.5772, "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600", "description": "Legendary street food alley serving butter masala dosas and jalebis."}
            ]
        },
        {
            "name": "Goa",
            "country": "India",
            "region": "Asia",
            "latitude": 15.2993,
            "longitude": 74.1240,
            "cost_index": 0.9,
            "popularity_score": 98.0,
            "currency_code": "INR",
            "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800",
            "description": "Sun-kissed Arabian Sea beaches, Portuguese colonial cathedrals, and coastal seafood.",
            "activities": [
                {"name": "Baga & Anjuna Beach Water Sports", "category": "Adventure", "estimated_cost": 1500.0, "duration_minutes": 180, "lat": 15.5553, "lng": 73.7517, "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600", "description": "Parasailing, jet ski, and relaxing beach shacks."},
                {"name": "Old Goa Basilica of Bom Jesus Tour", "category": "Culture", "estimated_cost": 0.0, "duration_minutes": 90, "lat": 15.5009, "lng": 73.9116, "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600", "description": "UNESCO World Heritage site holding the mortal remains of St. Francis Xavier."}
            ]
        },
        {
            "name": "Jaipur",
            "country": "India",
            "region": "Asia",
            "latitude": 26.9124,
            "longitude": 75.7873,
            "cost_index": 0.7,
            "popularity_score": 96.5,
            "currency_code": "INR",
            "image_url": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800",
            "description": "The Pink City of Rajasthan, famous for grand hilltop forts and majestic palaces.",
            "activities": [
                {"name": "Amber Fort Elephant & Jeep Heritage Tour", "category": "Culture", "estimated_cost": 500.0, "duration_minutes": 180, "lat": 26.9855, "lng": 75.8513, "image_url": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600", "description": "Majestic hilltop fort with Sheesh Mahal (Mirror Palace)."},
                {"name": "Hawa Mahal & City Palace Photo Walk", "category": "Sightseeing", "estimated_cost": 300.0, "duration_minutes": 120, "lat": 26.9239, "lng": 75.8267, "image_url": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600", "description": "Iconic honeycomb pink sandstone palace of the winds."}
            ]
        }
    ]

    city_objs = {}
    for c_data in cities_data:
        acts = c_data.pop("activities")
        existing_city = db.query(models.City).filter(models.City.name == c_data["name"]).first()
        if not existing_city:
            city = models.City(**c_data)
            db.add(city)
            db.commit()
            db.refresh(city)
            city_objs[city.name] = city

            for a_data in acts:
                if "lat" in a_data:
                    a_data["latitude"] = a_data.pop("lat")
                if "lng" in a_data:
                    a_data["longitude"] = a_data.pop("lng")
                act = models.Activity(city_id=city.id, **a_data)
                db.add(act)
            db.commit()
        else:
            city_objs[existing_city.name] = existing_city

    # 3. Create Pre-Populated Sample Multi-City Trip (Paris + Rome)
    sample_trip = db.query(models.Trip).filter(models.Trip.share_slug == "euro-trip-alex-2026").first()
    if not sample_trip:
        sample_trip = models.Trip(
            user_id=demo_user.id,
            title="European Odyssey: Paris & Rome",
            description="7 unforgettable days exploring iconic art, gastronomy, and historic architecture.",
            start_date=datetime.date(2026, 9, 10),
            end_date=datetime.date(2026, 9, 17),
            cover_image="https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1000",
            total_budget=250000.0,
            currency="INR",
            is_public=True,
            share_slug="euro-trip-alex-2026"
        )
        db.add(sample_trip)
        db.commit()
        db.refresh(sample_trip)

    # Add Group Members for GlobeSplit Demo
    db.add_all([
        models.TripMember(trip_id=sample_trip.id, user_id=demo_user.id, guest_name="Alex (Me)", role="owner"),
        models.TripMember(trip_id=sample_trip.id, guest_name="Sarah", role="editor"),
        models.TripMember(trip_id=sample_trip.id, guest_name="Liam", role="viewer")
    ])
    db.commit()

    # Add Stop 1: Paris
    paris = city_objs["Paris"]
    stop_paris = models.TripStop(
        trip_id=sample_trip.id,
        city_id=paris.id,
        arrival_date=datetime.date(2026, 9, 10),
        departure_date=datetime.date(2026, 9, 13),
        order_index=0,
        stop_budget=125000.0
    )
    db.add(stop_paris)

    # Add Stop 2: Rome
    rome = city_objs["Rome"]
    stop_rome = models.TripStop(
        trip_id=sample_trip.id,
        city_id=rome.id,
        arrival_date=datetime.date(2026, 9, 13),
        departure_date=datetime.date(2026, 9, 17),
        order_index=1,
        stop_budget=125000.0
    )
    db.add(stop_rome)
    db.commit()
    db.refresh(stop_paris)
    db.refresh(stop_rome)

    # Schedule Itinerary Items in Paris (Day 1)
    paris_acts = db.query(models.Activity).filter(models.Activity.city_id == paris.id).all()
    for idx, act in enumerate(paris_acts):
        item = models.ItineraryItem(
            stop_id=stop_paris.id,
            activity_id=act.id,
            custom_title=act.name,
            day_number=1 if idx < 2 else 2,
            start_time="10:00" if idx % 2 == 0 else "14:30",
            duration_minutes=act.duration_minutes,
            cost=round(act.estimated_cost * 90.0, 0),
            order_index=idx,
            notes="Book tickets online in advance"
        )
        db.add(item)

    # Schedule Itinerary Items in Rome (Day 1)
    rome_acts = db.query(models.Activity).filter(models.Activity.city_id == rome.id).all()
    for idx, act in enumerate(rome_acts):
        item = models.ItineraryItem(
            stop_id=stop_rome.id,
            activity_id=act.id,
            custom_title=act.name,
            day_number=1 if idx < 2 else 2,
            start_time="09:30" if idx % 2 == 0 else "15:00",
            duration_minutes=act.duration_minutes,
            cost=round(act.estimated_cost * 90.0, 0),
            order_index=idx
        )
        db.add(item)
    db.commit()

    # 4. Add Sample Multi-Currency Expenses for GlobeSplit (Converted to INR)
    exp1 = models.Expense(
        trip_id=sample_trip.id,
        paid_by_name="Alex (Me)",
        category="Stay",
        description="Paris Boutique Hotel (3 Nights)",
        amount=450.0,
        currency="EUR",
        converted_amount=convert_currency(450.0, "EUR", "INR"),
        expense_date=datetime.date(2026, 9, 10)
    )
    db.add(exp1)
    db.commit()
    db.refresh(exp1)

    # Split equally among Alex, Sarah, Liam
    share_inr = round(exp1.converted_amount / 3.0, 2)
    db.add_all([
        models.ExpenseSplit(expense_id=exp1.id, member_name="Alex (Me)", share_amount=share_inr),
        models.ExpenseSplit(expense_id=exp1.id, member_name="Sarah", share_amount=share_inr),
        models.ExpenseSplit(expense_id=exp1.id, member_name="Liam", share_amount=share_inr)
    ])

    exp2 = models.Expense(
        trip_id=sample_trip.id,
        paid_by_name="Sarah",
        category="Transport",
        description="High Speed Train (Paris to Rome)",
        amount=280.0,
        currency="EUR",
        converted_amount=convert_currency(280.0, "EUR", "INR"),
        expense_date=datetime.date(2026, 9, 13)
    )
    db.add(exp2)
    db.commit()
    db.refresh(exp2)
    share_inr2 = round(exp2.converted_amount / 3.0, 2)
    db.add_all([
        models.ExpenseSplit(expense_id=exp2.id, member_name="Alex (Me)", share_amount=share_inr2),
        models.ExpenseSplit(expense_id=exp2.id, member_name="Sarah", share_amount=share_inr2),
        models.ExpenseSplit(expense_id=exp2.id, member_name="Liam", share_amount=share_inr2)
    ])

    exp3 = models.Expense(
        trip_id=sample_trip.id,
        paid_by_name="Liam",
        category="Meals",
        description="Trastevere Italian Dinner & Wine",
        amount=120.0,
        currency="EUR",
        converted_amount=convert_currency(120.0, "EUR", "INR"),
        expense_date=datetime.date(2026, 9, 14)
    )
    db.add(exp3)
    db.commit()
    db.refresh(exp3)
    share_inr3 = round(exp3.converted_amount / 3.0, 2)
    db.add_all([
        models.ExpenseSplit(expense_id=exp3.id, member_name="Alex (Me)", share_amount=share_inr3),
        models.ExpenseSplit(expense_id=exp3.id, member_name="Sarah", share_amount=share_inr3),
        models.ExpenseSplit(expense_id=exp3.id, member_name="Liam", share_amount=share_inr3)
    ])

    db.commit()
    print("Seed data successfully created! Demo trip ready.")
    db.close()


if __name__ == "__main__":
    seed_database()
