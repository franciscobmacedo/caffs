import requests
from decouple import config
import json
from scraper.exceptions import InstagramScraperException
from scraper.cleaner import clean

URL = "https://www.instagram.com/api/v1/feed/user/21749057675/"


def get_location_set(
    headers: dict, cookies: dict, max_id: str | None
) -> tuple[list[dict], str]:
    params = {"count": "12"}
    if max_id is not None:
        params["max_id"] = max_id
    response = requests.get(URL, params=params, headers=headers, cookies=cookies)
    data = response.json()
    if data["status"] == "fail":
        raise InstagramScraperException(data["message"])

    if "items" not in data:
        raise InstagramScraperException("no more data")

    items = data["items"]
    if len(items) == 0:
        raise InstagramScraperException("no more data")

    print("getting data for ", len(items), "possible locations")

    max_id = items[-1]["id"]
    return items, max_id


def get_locations() -> list[dict]:
    x_ig_app_id = config("X_IG_APP_ID")
    sessionid = config("SESSION_ID")

    headers = {"x-ig-app-id": x_ig_app_id}
    cookies = {"sessionid": sessionid}
    max_id = None
    all_locations = []
    while True:
        try:
            locations, max_id = get_location_set(headers, cookies, max_id)
        except InstagramScraperException as e:
            print(e)
            break
        all_locations.extend(locations)

    return all_locations


def pipeline():
    locations = get_locations()
    with open("locations.json", "w") as f:
        json.dump(locations, f)
    clean(locations, True)


if __name__ == "__main__":
    pipeline()