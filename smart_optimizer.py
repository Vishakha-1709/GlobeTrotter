"""
Smart Route Optimizer — AI Geospatial Travel Sequencer
(WOW Factor 2)

Solves the Travelling Salesperson / Proximity Sequencing Problem for day-wise itinerary items.
Given a list of scheduled activities in a city with GPS coordinates (lat, lng), it computes
the optimal visitation sequence to minimize total transit distance and travel time.
"""

import math
from typing import List, Dict, Any


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two geographic points in kilometers."""
    R = 6371.0  # Earth radius in kilometers

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def compute_route_metrics(items: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculates total distance (km) and estimated transit time (mins) for a sequence of stops."""
    total_km = 0.0
    for i in range(len(items) - 1):
        p1 = items[i]
        p2 = items[i + 1]
        lat1, lng1 = p1.get("lat"), p1.get("lng")
        lat2, lng2 = p2.get("lat"), p2.get("lng")

        if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
            dist = haversine_distance_km(lat1, lng1, lat2, lng2)
            # Add 25% urban routing factor (streets are not straight flight paths)
            total_km += dist * 1.25

    # Assume average city transit speed = 20 km/h + 5 min waiting/parking per leg
    legs = max(0, len(items) - 1)
    transit_mins = (total_km / 20.0) * 60.0 + (legs * 5.0)

    return {
        "total_distance_km": round(total_km, 2),
        "transit_time_minutes": round(transit_mins, 1),
    }


def optimize_day_schedule(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Re-orders items using a Nearest-Neighbor heuristic with 2-Opt local search refinement.
    
    Returns:
    {
        "original_metrics": {"total_distance_km": 14.2, "transit_time_minutes": 55},
        "optimized_metrics": {"total_distance_km": 6.8, "transit_time_minutes": 27},
        "distance_saved_km": 7.4,
        "time_saved_minutes": 28.0,
        "optimized_items": [...]
    }
    """
    if len(items) <= 2:
        metrics = compute_route_metrics(items)
        return {
            "original_metrics": metrics,
            "optimized_metrics": metrics,
            "distance_saved_km": 0.0,
            "time_saved_minutes": 0.0,
            "optimized_items": items,
        }

    original_metrics = compute_route_metrics(items)

    # Nearest Neighbor starting from the first item
    unvisited = items[1:].copy()
    route = [items[0]]

    while unvisited:
        current = route[-1]
        cur_lat = current.get("lat") or 0.0
        cur_lng = current.get("lng") or 0.0

        best_idx = 0
        best_dist = float("inf")

        for idx, candidate in enumerate(unvisited):
            cand_lat = candidate.get("lat") or 0.0
            cand_lng = candidate.get("lng") or 0.0
            d = haversine_distance_km(cur_lat, cur_lng, cand_lat, cand_lng)
            if d < best_dist:
                best_dist = d
                best_idx = idx

        route.append(unvisited.pop(best_idx))

    # 2-Opt local search improvement
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for k in range(i + 1, len(route)):
                new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
                if compute_route_metrics(new_route)["total_distance_km"] < compute_route_metrics(route)["total_distance_km"]:
                    route = new_route
                    improved = True

    optimized_metrics = compute_route_metrics(route)
    dist_saved = max(0.0, original_metrics["total_distance_km"] - optimized_metrics["total_distance_km"])
    time_saved = max(0.0, original_metrics["transit_time_minutes"] - optimized_metrics["transit_time_minutes"])

    return {
        "original_metrics": original_metrics,
        "optimized_metrics": optimized_metrics,
        "distance_saved_km": round(dist_saved, 2),
        "time_saved_minutes": round(time_saved, 1),
        "optimized_items": route,
    }
