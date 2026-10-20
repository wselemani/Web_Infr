
import requests
from pathlib import Path

API_KEY = "DEMO_KEY"
API_URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/"

SAVE_FOLDER = Path.cwd() / "nasa_images"
SAVE_FOLDER.mkdir(exist_ok=True)

try:
    response = requests.get(
        API_URL,
        params={"api_key": API_KEY, "count": 5},
        timeout=30
    )
    response.raise_for_status()
    results = response.json()

    print("\n" + "=" * 55)
    print("       NASA ASTRONOMY PICTURES")
    print("=" * 55)

    downloaded = 0

    for number, item in enumerate(results[:5], start=1):
        print(f"\n{number}. {item.get('title', 'Untitled')}")
        print(f"Date: {item.get('date', 'Unknown')}")
        print(f"Explanation: {item.get('explanation', '')[:120]}...")

        if item.get("media_type") != "image":
            print("Skipped: this result is not an image.")
            continue

        image_url = item.get("hdurl") or item.get("url", "")

        try:
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()

            # Check that the response contains an image
            content_type = image_response.headers.get(
                "Content-Type", ""
            )

            if not content_type.startswith("image/"):
                print("Skipped: URL did not return an image.")
                continue

            extension = ".jpg"
            if "png" in content_type:
                extension = ".png"
            elif "gif" in content_type:
                extension = ".gif"
            elif "webp" in content_type:
                extension = ".webp"

            image_path = SAVE_FOLDER / f"nasa_image_{number}{extension}"
            image_path.write_bytes(image_response.content)

            downloaded += 1
            print(f"Image saved: {image_path.resolve()}")

        except requests.RequestException as error:
            print(f"Image download failed: {error}")

    print("\n" + "=" * 55)
    print(f"Results displayed: {min(len(results), 5)}")
    print(f"Images downloaded: {downloaded}")
    print(f"Folder: {SAVE_FOLDER.resolve()}")
    print("=" * 55)

except requests.RequestException as error:
    print(f"NASA connection error: {error}")
except (ValueError, KeyError) as error:
    print(f"Could not process NASA response: {error}")
