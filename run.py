import instagraper
from decouple import config

static_url = config("STATIC_URL", default=None)

instagraper.scrape(
    username="caffs_not_cafes",
    target="frontend",
    map_output="index.html",
    with_images=True,
    static_url=static_url,
)
