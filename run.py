import instagraper
from decouple import config

static_url = config("STATIC_URL", default=None)

instagraper.scrape(
    username="caffs_not_cafes",
    target="frontend",
    with_map=True,
    with_images=True,
)
