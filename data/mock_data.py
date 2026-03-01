from __future__ import annotations

from copy import deepcopy


TRANSPORT_DATA = [
    {
        "id": "TR-PAR-001",
        "destination": "paris",
        "type": "Flight",
        "provider": "Air France",
        "price": 620.0,
        "departure_time": "08:10",
        "arrival_time": "14:45",
        "duration": "6h 35m",
    },
    {
        "id": "TR-PAR-002",
        "destination": "paris",
        "type": "Train",
        "provider": "EuroRail",
        "price": 190.0,
        "departure_time": "09:00",
        "arrival_time": "18:20",
        "duration": "9h 20m",
    },
    {
        "id": "TR-PAR-003",
        "destination": "paris",
        "type": "Bus",
        "provider": "FlixBus",
        "price": 95.0,
        "departure_time": "07:00",
        "arrival_time": "20:00",
        "duration": "13h 00m",
    },
    {
        "id": "TR-TOK-001",
        "destination": "tokyo",
        "type": "Flight",
        "provider": "Japan Airlines",
        "price": 990.0,
        "departure_time": "10:25",
        "arrival_time": "23:15",
        "duration": "12h 50m",
    },
    {
        "id": "TR-TOK-002",
        "destination": "tokyo",
        "type": "Train",
        "provider": "Shinkansen Connect",
        "price": 240.0,
        "departure_time": "06:30",
        "arrival_time": "11:00",
        "duration": "4h 30m",
    },
    {
        "id": "TR-TOK-003",
        "destination": "tokyo",
        "type": "Bus",
        "provider": "Highway Express",
        "price": 70.0,
        "departure_time": "22:00",
        "arrival_time": "06:00",
        "duration": "8h 00m",
    },
    {
        "id": "TR-BAL-001",
        "destination": "bali",
        "type": "Flight",
        "provider": "Garuda Indonesia",
        "price": 540.0,
        "departure_time": "11:40",
        "arrival_time": "16:50",
        "duration": "5h 10m",
    },
    {
        "id": "TR-BAL-002",
        "destination": "bali",
        "type": "Bus",
        "provider": "Island Hopper",
        "price": 45.0,
        "departure_time": "08:00",
        "arrival_time": "12:30",
        "duration": "4h 30m",
    },
    {
        "id": "TR-BAL-003",
        "destination": "bali",
        "type": "Train",
        "provider": "Java Rail",
        "price": 120.0,
        "departure_time": "05:45",
        "arrival_time": "10:15",
        "duration": "4h 30m",
    },
]


HOTEL_DATA = [
    {
        "id": "HT-PAR-001",
        "destination": "paris",
        "name": "Seine View Hotel",
        "price_per_night": 180.0,
        "rating": 4.3,
        "location": "7th Arrondissement",
        "amenities": ["WiFi", "Breakfast", "River View"],
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34",
    },
    {
        "id": "HT-PAR-002",
        "destination": "paris",
        "name": "Louvre Central Inn",
        "price_per_night": 120.0,
        "rating": 4.0,
        "location": "1st Arrondissement",
        "amenities": ["WiFi", "Metro Access"],
        "image_url": "https://images.unsplash.com/photo-1431274172761-fca41d930114",
    },
    {
        "id": "HT-PAR-003",
        "destination": "paris",
        "name": "Paris Grand Palace",
        "price_per_night": 320.0,
        "rating": 4.8,
        "location": "Champs-Elysees",
        "amenities": ["Spa", "Pool", "Concierge"],
        "image_url": "https://images.unsplash.com/photo-1455587734955-081b22074882",
    },
    {
        "id": "HT-TOK-001",
        "destination": "tokyo",
        "name": "Shibuya Sky Stay",
        "price_per_night": 210.0,
        "rating": 4.5,
        "location": "Shibuya",
        "amenities": ["WiFi", "City View", "Gym"],
        "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf",
    },
    {
        "id": "HT-TOK-002",
        "destination": "tokyo",
        "name": "Asakusa Budget Rooms",
        "price_per_night": 95.0,
        "rating": 4.1,
        "location": "Asakusa",
        "amenities": ["WiFi", "Self Check-in"],
        "image_url": "https://images.unsplash.com/photo-1554797589-7241bb691973",
    },
    {
        "id": "HT-TOK-003",
        "destination": "tokyo",
        "name": "Imperial Tokyo Suites",
        "price_per_night": 360.0,
        "rating": 4.9,
        "location": "Chiyoda",
        "amenities": ["Spa", "Pool", "Fine Dining"],
        "image_url": "https://images.unsplash.com/photo-1513553404607-988d4c84352f",
    },
    {
        "id": "HT-BAL-001",
        "destination": "bali",
        "name": "Ubud Forest Retreat",
        "price_per_night": 160.0,
        "rating": 4.6,
        "location": "Ubud",
        "amenities": ["Breakfast", "Yoga Deck", "Pool"],
        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4",
    },
    {
        "id": "HT-BAL-002",
        "destination": "bali",
        "name": "Kuta Budget Lodge",
        "price_per_night": 75.0,
        "rating": 3.9,
        "location": "Kuta",
        "amenities": ["WiFi", "Airport Shuttle"],
        "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
    },
    {
        "id": "HT-BAL-003",
        "destination": "bali",
        "name": "Nusa Dua Luxury Bay",
        "price_per_night": 310.0,
        "rating": 4.8,
        "location": "Nusa Dua",
        "amenities": ["Private Beach", "Spa", "Infinity Pool"],
        "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4",
    },
]


FALLBACK_HOTEL_IMAGE = "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800"
FALLBACK_DESTINATION_IMAGE = "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1200"
FALLBACK_PLACE_IMAGE = "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800"

DESTINATION_IMAGES = {
    "paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200",
    "tokyo": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200",
    "bali": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200",
    "london": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200",
    "new york": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?w=1200",
    "rome": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200",
    "barcelona": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1200",
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200",
    "singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=1200",
    "sydney": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200",
    "bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c8dd0d5?w=1200",
    "amsterdam": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=1200",
    "istanbul": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200",
}


PLACE_IMAGES = {
    # Paris
    "Eiffel Tower": "https://images.unsplash.com/photo-1549144511-f099e773c147?w=800",
    "Louvre Museum": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800",
    "Montmartre": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=800",
    "Notre-Dame Cathedral": "https://images.unsplash.com/photo-1478391679764-b2d8b3cd1e94?w=800",
    # Tokyo
    "Shibuya Crossing": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=800",
    "Senso-ji Temple": "https://images.unsplash.com/photo-1570459027563-4a916cc6113f?w=800",
    "Tokyo Skytree": "https://images.unsplash.com/photo-1538037172739-c15f723fcb00?w=800",
    "Shinjuku": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
    # Bali
    "Uluwatu Temple": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=800",
    "Tegallalang Rice Terrace": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800",
    "Nusa Penida": "https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=800",
    # Rome
    "Colosseum": "https://images.unsplash.com/photo-1552432552-06c0b0a94dda?w=800",
    "Trevi Fountain": "https://images.unsplash.com/photo-1555993539-1732b0258235?w=800",
    "Vatican Museums": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800",
    # Barcelona
    "Sagrada Familia": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=800",
    "Park Guell": "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800",
    "Las Ramblas": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800",
    # Dubai
    "Burj Khalifa": "https://images.unsplash.com/photo-1518684079-3c830dcef090?w=800",
    "Dubai Mall": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800",
    "Palm Jumeirah": "https://images.unsplash.com/photo-1580674684081-7617fbf3d745?w=800",
    # Singapore
    "Marina Bay Sands": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800",
    "Gardens by the Bay": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800",
    "Sentosa Island": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800",
    # Sydney
    "Sydney Opera House": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800",
    "Bondi Beach": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800",
    "Sydney Harbour Bridge": "https://images.unsplash.com/photo-1524293568345-75d62c3664f7?w=800",
    # Bangkok
    "Grand Palace": "https://images.unsplash.com/photo-1508009603885-50cf7c8dd0d5?w=800",
    "Wat Arun": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800",
    "Chatuchak Market": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    # Amsterdam
    "Anne Frank House": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=800",
    "Rijksmuseum": "https://images.unsplash.com/photo-1576662712957-9c79ae1280f8?w=800",
    "Amsterdam Canals": "https://images.unsplash.com/photo-1512470876302-972faa2aa9a4?w=800",
    # Istanbul
    "Hagia Sophia": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800",
    "Blue Mosque": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=800",
    "Grand Bazaar": "https://images.unsplash.com/photo-1527838832700-5059252407fa?w=800",
}


DEFAULT_PLACES_BY_DESTINATION = {
    "paris": ["Eiffel Tower", "Louvre Museum", "Montmartre"],
    "tokyo": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Skytree"],
    "bali": ["Uluwatu Temple", "Tegallalang Rice Terrace", "Nusa Penida"],
    "rome": ["Colosseum", "Trevi Fountain", "Vatican Museums"],
    "barcelona": ["Sagrada Familia", "Park Guell", "Las Ramblas"],
    "dubai": ["Burj Khalifa", "Dubai Mall", "Palm Jumeirah"],
    "singapore": ["Marina Bay Sands", "Gardens by the Bay", "Sentosa Island"],
    "sydney": ["Sydney Opera House", "Bondi Beach", "Sydney Harbour Bridge"],
    "bangkok": ["Grand Palace", "Wat Arun", "Chatuchak Market"],
    "amsterdam": ["Anne Frank House", "Rijksmuseum", "Amsterdam Canals"],
    "istanbul": ["Hagia Sophia", "Blue Mosque", "Grand Bazaar"],
}


def normalize_destination(destination: str) -> str:
    return destination.strip().lower()


def get_transport_data(destination: str) -> list[dict]:
    normalized = normalize_destination(destination)
    records = [item for item in TRANSPORT_DATA if item["destination"] == normalized]
    if records:
        return deepcopy(records)
    return deepcopy(TRANSPORT_DATA[:3])


def get_hotel_data(destination: str) -> list[dict]:
    normalized = normalize_destination(destination)
    records = [item for item in HOTEL_DATA if item["destination"] == normalized]
    if records:
        return deepcopy(records)
    return deepcopy(HOTEL_DATA[:3])


def get_destination_image(destination: str) -> str:
    normalized = normalize_destination(destination)
    return DESTINATION_IMAGES.get(normalized, FALLBACK_DESTINATION_IMAGE)


def get_place_image(place_name: str) -> str:
    return PLACE_IMAGES.get(place_name, FALLBACK_PLACE_IMAGE)


def get_default_places(destination: str) -> list[str]:
    normalized = normalize_destination(destination)
    return deepcopy(DEFAULT_PLACES_BY_DESTINATION.get(normalized, ["City Center", "Local Market", "Museum District"]))
