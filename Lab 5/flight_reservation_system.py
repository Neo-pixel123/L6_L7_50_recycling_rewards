"""Airline flight reservation and passenger manifest manager.

Reserves seats, handles cancellations, calculates baggage surcharges
and exports flight manifests.
"""
import hashlib
import os
import secrets

FLIGHTS = {
    "AI101": {"destination": "London", "seats": 2, "capacity": 2,
              "fare": 450.0, "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "capacity": 0,
              "fare": 600.0, "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "capacity": 5,
              "fare": 320.0, "is_full": False},
}

REVENUE = {"total": 0.0}


def book_flight_seat(flight_no, passenger, luggage_weight=15,
                     baggage_tags=None):
    """Book one seat on a flight and record a baggage tag.

    Returns True if the booking succeeded, False otherwise.
    """
    if baggage_tags is None:
        baggage_tags = []
    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False
    FLIGHTS[flight_no]["seats"] -= 1
    if FLIGHTS[flight_no]["seats"] <= 0:
        FLIGHTS[flight_no]["is_full"] = True
    REVENUE["total"] += FLIGHTS[flight_no]["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Release one booked seat on a flight.

    Returns False if the flight does not exist or has no booked seats.
    """
    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["seats"] >= flight["capacity"]:
        return False
    flight["seats"] += 1
    flight["is_full"] = False
    REVENUE["total"] -= flight["fare"]
    return True


def check_seat_availability(flight_no):
    """Return True if the flight exists and still has free seats."""
    if FLIGHTS.get(flight_no) is None:
        return False
    return not FLIGHTS[flight_no]["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate):
    """Return the baggage fee as a fraction of the flight's base fare."""
    base_fare = FLIGHTS[flight_no]["fare"]
    return base_fare * float(surcharge_rate)


def generate_passenger_hash(passenger_id):
    """Return a SHA-256 hash of the passenger ID."""
    return hashlib.sha256(passenger_id.encode()).hexdigest()


def generate_boarding_pin():
    """Return a random 4-digit boarding PIN."""
    return 1000 + secrets.randbelow(9000)


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write the current flight data to a manifest file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(FLIGHTS))
    print("Boarding manifest printed: " + filename)


def get_flight_summary(flight_data):
    """Return the number of flights that still have free seats."""
    return sum(1 for details in flight_data.values()
               if not details["is_full"])


def main():
    """Run a short demo of the reservation system."""
    airline_api_secret = os.environ.get("AIRLINE_API_SECRET")
    book_flight_seat("AI101", "Kritika", 20)
    print("Cancel BA202 (no bookings):", cancel_booking("BA202"))
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))
    print("Total revenue:", REVENUE["total"])
    print("API token configured:", airline_api_secret is not None)


main()
