import json
import requests
import os


def extract_image(item: dict, code: str) -> bool:
    img_url = (
        item.get("caption", {})
        .get("user", {})
        .get("hd_profile_pic_url_info", {})
        .get("url", None)
    )
    if not img_url:
        return False
    r = requests.get(img_url)
    image_path = f"frontend/images/{code}.webp"
    if not os.path.exists("frontend/images"):
        os.makedirs("frontend/images")
    with open(image_path, "wb") as f:
        f.write(r.content)

    return True


def extract_code(item: dict) -> str | None:
    return item.get("code", None)


def item_to_location(item: dict):
    _location = item.get("location", {})
    name = _location.get("name", None)
    lat = _location.get("lat", None)
    lng = _location.get("lng", None)
    if lat is None or lng is None:
        return None

    code = extract_code(item)
    if not code:
        raise Exception("No code found")

    has_image = extract_image(item, code)
    location = {
        "name": name,
        "lat": lat,
        "lng": lng,
        "code": code,
        "image": f"images/{code}.webp" if has_image else None,
    }
    return location


def get_locations(items: list[dict]) -> list[dict]:
    locations = []
    for item in items:
        location = item_to_location(item)
        if location is not None:
            locations.append(location)
    return locations


def convert_to_geojson(locations: list[dict], write: bool = False):
    new_locations = []
    for location in locations:
        new_location = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location["lng"], location["lat"]],
            },
            "properties": {
                "title": f"<a target='_blank' href='https://www.instagram.com/p/{location['code']}/'>{location.get('name', 'see')}</a>",
                "description": f"<img src='{location.get('image', '')}' width='200px' />",
                "marker-color": "#3bb2d0",
                "marker-size": "large",
                "marker-symbol": "rocket",
            },
        }
        new_locations.append(new_location)

    if write:
        with open("frontend/locations.geojson", "w") as f:
            json.dump(new_locations, f)
    return new_locations


def clean(data: list[dict], write: bool = False):
    locations = get_locations(data)
    locations = convert_to_geojson(locations, write)

    return locations


def clean_from_file(write: bool = False):
    with open("locations.json", "r") as f:
        data = json.load(f)

    return clean(data, write)
