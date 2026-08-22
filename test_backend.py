from database import SessionLocal
import models
from debt_engine import compute_net_balances, settle_debts_min_cash_flow
from smart_optimizer import optimize_day_schedule

db = SessionLocal()

print("--- 1. Testing Database Queries ---")
user = db.query(models.User).first()
trip = db.query(models.Trip).first()
print(f"User: {user.name} ({user.email})")
print(f"Trip: {trip.title}, Total Budget: ₹{trip.total_budget}")
print(f"Stops count: {len(trip.stops)}")

print("\n--- 2. Testing GlobeSplit (WOW Factor 1: Debt Settlement) ---")
expenses_payload = []
for exp in trip.expenses:
    splits_list = [{"name": sp.member_name, "share": sp.share_amount} for sp in exp.splits]
    expenses_payload.append({
        "paid_by": exp.paid_by_name,
        "converted_amount": exp.converted_amount,
        "splits": splits_list
    })

balances = compute_net_balances(expenses_payload)
print("Member Balances (₹):", balances)
settlements = settle_debts_min_cash_flow(balances)
print("Settlement Transactions (Min-Cash-Flow):")
for s in settlements:
    print(f"  -> {s['from_user']} pays {s['to_user']} ₹{s['amount']:.2f}")

print("\n--- 3. Testing Smart Route Optimizer (WOW Factor 2: TSP) ---")
stop = trip.stops[0]  # Paris
items = db.query(models.ItineraryItem).filter(models.ItineraryItem.stop_id == stop.id).all()
payload = []
for it in items:
    payload.append({
        "id": it.id,
        "title": it.custom_title,
        "lat": it.activity.latitude,
        "lng": it.activity.longitude,
        "cost": it.cost,
        "duration": it.duration_minutes
    })

opt_res = optimize_day_schedule(payload)
print(f"Original Distance : {opt_res['original_metrics']['total_distance_km']} km ({opt_res['original_metrics']['transit_time_minutes']} mins)")
print(f"Optimized Distance: {opt_res['optimized_metrics']['total_distance_km']} km ({opt_res['optimized_metrics']['transit_time_minutes']} mins)")
print(f"Saved: {opt_res['distance_saved_km']} km & {opt_res['time_saved_minutes']} mins!")

print("\nAll Backend Engines Working Perfectly!")
db.close()
