import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/charchaa_db')
# Set a shorter timeout for server selection to fail faster if the DB is unreachable
client = MongoClient(MONGO_URI)
db = client.get_database()

menu_collection = db.menu
reservations_collection = db.reservations

def seed_initial_menu():
    """Initializes the database with the Charchaa specialty menu if empty."""
    try:
        # Verify connection before attempting operations
        client.admin.command('ping')
    except Exception:
        print(f"\n[CRITICAL] Could not connect to MongoDB at {MONGO_URI}. Please ensure your database is running and reachable.\n")
        return

    if menu_collection.count_documents({}) == 0:
        initial_items = [
            {"category": "Hot Coffee", "name": "Espresso", "price": 60, "description": "Pure coffee extract 36ML", "is_available": True},
            {"category": "Hot Coffee", "name": "Americano / Long Black", "price": 90, "description": "Espresso with hot water", "is_available": True},
            {"category": "Hot Coffee", "name": "Cortado", "price": 80, "description": "Equal parts of espresso & milk", "is_available": True},
            {"category": "Hot Coffee", "name": "Cappuccino", "price": 90, "description": "Equal parts of espresso, milk & foam", "is_available": True},
            {"category": "Hot Coffee", "name": "Flat White", "price": 100, "description": "Espresso with steamed milk", "is_available": True},
            {"category": "Hot Coffee", "name": "Caffè Latte", "price": 110, "description": "Espresso with steamed milk & light foam", "is_available": True},
            {"category": "Hot Coffee", "name": "Caffè Mocha", "price": 130, "description": "Dark chocolate with espresso & steamed milk", "is_available": True},
            
            {"category": "Iced Coffee", "name": "Iced Americano", "price": 90, "description": "Ice, cold water & espresso", "is_available": True},
            {"category": "Iced Coffee", "name": "Iced Latte", "price": 110, "description": "Ice, milk & espresso layered on top", "is_available": True},
            {"category": "Iced Coffee", "name": "Hazelnut Iced Latte", "price": 130, "description": "Ice, milk, hazelnut & espresso layered", "is_available": True},
            {"category": "Iced Coffee", "name": "Vanilla Iced Latte", "price": 130, "description": "Ice, milk, vanilla & espresso layered", "is_available": True},
            {"category": "Iced Coffee", "name": "Strawberry Iced Latte", "price": 140, "description": "Ice, milk, strawberry crush & espresso layered", "is_available": True},
            {"category": "Iced Coffee", "name": "Iced Mocha", "price": 130, "description": "Ice, dark chocolate, milk & espresso shaken together", "is_available": True},
            {"category": "Iced Coffee", "name": "Iced Cortado", "price": 90, "description": "Ice with equal parts of milk & espresso", "is_available": True},
            {"category": "Iced Coffee", "name": "Classic Cold Coffee", "price": 120, "description": "Ice, vanilla ice cream, milk, chocolate & espresso blended", "is_available": True},
            {"category": "Iced Coffee", "name": "Espresso Tonic", "price": 110, "description": "Tonic water topped with espresso", "is_available": True},
            {"category": "Iced Coffee", "name": "Caramel Iced Latte", "price": 130, "description": "Ice, milk, caramel & espresso layered", "is_available": True},

            {"category": "Charchaa Brew Bar", "name": "House Cold Brew", "price": 110, "description": "Slow steeped for 18 hours", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Cold Tonic Tales", "price": 120, "description": "Fizzy tonic water topped with in-house cold brew", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Ginger Buzz", "price": 120, "description": "Refreshing ginger ale topped with in-house cold brew", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Vanilla Velvet Cloud", "price": 140, "description": "In-house cold brew floated with vanilla foam", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Taazgi Ki Charchaa", "price": 130, "description": "Fresh basil leaves shaken with in-house cold brew & sour mix", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Berry Herbal Brew", "price": 130, "description": "In-house cold brew floated with strawberry foam", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Orange Espresso Tonic", "price": 130, "description": "Fruity orange juice, tonic water & a shot of espresso", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Golden Hour In A Glass", "price": 130, "description": "Orange juice & espresso served over ice", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Irish Indulgence", "price": 130, "description": "Americano topped with Irish cream foam", "is_available": True},
            {"category": "Charchaa Brew Bar", "name": "Lavender Cold Brew", "price": 130, "description": "In-house cold brew floated with silky floral lavender foam", "is_available": True},

            {"category": "Desserts", "name": "Affogato", "price": 90, "description": "Vanilla ice cream, espresso", "is_available": True},
            {"category": "Desserts", "name": "Mocha Affogato", "price": 110, "description": "Vanilla ice cream, chocolate syrup, chocochips, espresso", "is_available": True}
        ]
        menu_collection.insert_many(initial_items)

def get_grouped_menu():
    """Fetches and groups menu items by category."""
    items = list(menu_collection.find({}))
    grouped = {}
    for item in items:
        cat = item['category']
        if cat not in grouped:
            grouped[cat] = []
        item['_id'] = str(item['_id'])
        grouped[cat].append(item)
    return grouped

def toggle_menu_item(item_id, status):
    """Updates availability of a menu item."""
    menu_collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"is_available": status}})

def create_reservation(data):
    """Validates and inserts a new reservation."""
    # Validation: 5:00 PM to 12:00 AM (17:00 to 00:00)
    time_parts = data['time_slot'].split(':')
    hour = int(time_parts[0])
    
    # 12:00 AM is 00:00. 17:00 is 5:00 PM.
    is_valid_time = False
    if hour >= 17 or hour == 0:
        is_valid_time = True
        
    if not is_valid_time:
        return False, "Reservations are only available during operational hours (5 PM - 12 AM)."

    reservation = {
        "name": data['name'],
        "phone": data['phone'],
        "date": data['date'],
        "time_slot": data['time_slot'],
        "guest_count": int(data['guest_count']),
        "session_type": data['session_type'],
        "created_at": datetime.now(timezone.utc)
    }
    reservations_collection.insert_one(reservation)
    return True, "Reservation successful. We'll see you for चर्चा!"

def get_all_reservations():
    """Fetches all reservations sorted by date created."""
    res = list(reservations_collection.find().sort("created_at", -1))
    for r in res:
        r['_id'] = str(r['_id'])
        r['created_at'] = r['created_at'].strftime("%Y-%m-%d %H:%M")
    return res

def get_all_menu_flat():
    """Fetches all menu items for admin management."""
    items = list(menu_collection.find())
    for i in items:
        i['_id'] = str(i['_id'])
    return items