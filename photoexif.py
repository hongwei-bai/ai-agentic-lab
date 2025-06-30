from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim

img = "photos/PXL_20250505_004455271.MP.jpg"

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_raw = image._getexif()
    exif = {}
    if exif_raw:
        for tag_id, value in exif_raw.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = value
    return exif

def get_device_info(exif):
    make = exif.get("Make", "Unknown")
    model = exif.get("Model", "Unknown")
    return f"{make} {model}"

def get_gps_info(exif):
    gps_info = exif.get("GPSInfo")
    if not gps_info:
        return None, None

    def to_degrees(dms):
        d, m, s = dms
        return float(d) + float(m)/60 + float(s)/3600

    lat = to_degrees(gps_info[2])
    lon = to_degrees(gps_info[4])

    if gps_info[1] == 'S':
        lat = -lat
    if gps_info[3] == 'W':
        lon = -lon

    return lat, lon

def get_country_from_coords(lat, lon):
    geolocator = Nominatim(user_agent="photo_meta_reader")
    location = geolocator.reverse((lat, lon), language='en')
    if location and 'country' in location.raw['address']:
        return location.raw['address']['country']
    return "Unknown"

def get_location_from_coords(lat, lon):
    geolocator = Nominatim(user_agent="photo_meta_reader", timeout=10)
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        address = location.raw.get('address', {})
        country = address.get('country', 'Unknown')
        city = address.get('city') or address.get('town') or address.get('village') or address.get('suburb') or 'Unknown'
        return city, country
    return "Unknown", "Unknown"

def get_location_details(lat, lon):
    geolocator = Nominatim(user_agent="photo_meta_reader", timeout=10)
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        address = location.raw.get('address', {})
        poi = address.get('attraction') or address.get('building') or address.get('theatre') or address.get('museum') or address.get('office') or address.get('amenity') or 'Unknown'
        city = address.get('city') or address.get('town') or address.get('village') or address.get('suburb') or 'Unknown'
        country = address.get('country', 'Unknown')
        return poi, city, country
    return "Unknown", "Unknown", "Unknown"

# Main
exif = get_exif_data(img)
device = get_device_info(exif)
lat, lon = get_gps_info(exif)

if lat and lon:
    poi, city, country = get_location_details(lat, lon)
else:
    poi, city, country = "No POI", "No GPS data", "No GPS data"

print(f"📱 Device: {device}")
print(f"📌 POI: {poi}")
print(f"📍 City: {city}")
print(f"🌍 Country: {country}")
