import json
import requests
import os
from scraper.settings import BASE_URL, IMAGES_RELATIVE_PATH


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
    image_path = f"{IMAGES_RELATIVE_PATH}/{code}.webp"

    with open(image_path, "wb") as f:
        f.write(r.content)

    return True


def extract_code(item: dict) -> str | None:
    return item.get("code", None)


def item_to_point(item: dict) -> dict:
    _location = item.get("location", {})
    name = _location.get("name", "see post")
    lat = _location.get("lat", None)
    lng = _location.get("lng", None)
    if lat is None or lng is None:
        return None
    code = extract_code(item)
    if not code:
        raise Exception("No code found")

    has_image = extract_image(item, code)
    description = (
        f"<img src='{BASE_URL}/frontend/images/{code}.webp' width='200px' />"
        if has_image
        else ""
    )
    title = f"<a target='_blank' href='https://www.instagram.com/p/{code}/'>{name}</a>"
    point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat],
        },
        "properties": {
            "title": title,
            "description": description,
            "marker-color": "#3bb2d0",
            "marker-size": "large",
            "marker-symbol": "rocket",
        },
    }
    return point


def clean_points(items: list[dict]) -> dict:
    for item in items:
        point = item_to_point(item)
        if point:
            yield point


def clean(items: list[dict], write: bool = False) -> dict:
    if not os.path.exists(IMAGES_RELATIVE_PATH):
        os.makedirs(IMAGES_RELATIVE_PATH)

    print(f"Cleaning {len(items)} items")
    stream = clean_points(items)

    feature_collection = {
        "type": "FeatureCollection",
        "features": list(stream),
    }
    print("done")

    if write:
        with open("frontend/locations.geojson", "w") as f:
            json.dump(feature_collection, f)
    return feature_collection


def clean_from_file(write: bool = False) -> dict:
    with open("items.json", "r") as f:
        data = json.load(f)

    return clean(data, write)
