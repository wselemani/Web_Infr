
import requests
from pathlib import Path
from html import unescape
import re

SHOW = "breaking"
URL = f"https://api.tvmaze.com/search/shows?q={SHOW}"

response_obj = requests.get(URL, timeout=30)
response_obj.raise_for_status()
json_data = response_obj.json()

# Save images in a folder beside this Python file
SAVE_FOLDER = Path(__file__).parent / "show_images"
SAVE_FOLDER.mkdir(exist_ok=True)

for number, item in enumerate(json_data[:5], start=1):
    show = item["show"]

    print("\n" + "=" * 40)
    print(f"RESULT {number}")
    print("=" * 40)

    print(f"Name: {show['name']}")
    print(f"Genres: {', '.join(show.get('genres', [])) or 'Not available'}")

    summary = show.get("summary") or "No summary available"
    summary = re.sub(r"<[^>]+>", "", summary)
    print(f"Summary: {unescape(summary)}")

    image_info = show.get("image")

    if image_info and image_info.get("original"):
        try:
            image_url = image_info["original"]
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()

            filename = f"show_image_{number}.jpg"
            image_path = SAVE_FOLDER / filename
            image_path.write_bytes(image_response.content)

            print(f"Image saved to: {image_path.resolve()}")

        except requests.RequestException as error:
            print(f"Image download failed: {error}")
    else:
        print("No image available for this show.")

print("\nFinished displaying the top five results.")
print(f"Images folder: {SAVE_FOLDER.resolve()}")
