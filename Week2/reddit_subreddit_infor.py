import requests

# Step 1: Choose the subreddit we want information about
subreddit = "python"

# Step 2: Set a User-Agent header (Reddit's API rules require this)
headers = {"User-Agent": "script:alu.subreddit.info:v1.0 (by /u/wezzie_malisa)"}

# Step 3: The three Reddit addresses (URLs) we need
about_url = f"https://www.reddit.com/r/{subreddit}/about.json"
rules_url = f"https://www.reddit.com/r/{subreddit}/about/rules.json"
posts_url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=10"


def get_data(url):
    """Ask Reddit for data. Returns the data, or None if something went wrong."""
    response = requests.get(url, headers=headers)

    # 200 means success. Anything else (like 403) means Reddit refused us.
    if response.status_code != 200:
        print("Reddit refused the request. Status code:", response.status_code)
        return None

    # Sometimes Reddit sends a web page instead of data, so we check first
    try:
        return response.json()
    except ValueError:
        print("Reddit sent a web page instead of data (request was blocked).")
        return None


# Step 4: Subreddit name, description and number of subscribers
print("--- Subreddit Info ---")
about = get_data(about_url)
if about is not None:
    info = about["data"]
    print("Subreddit name:", info["display_name"])
    print("Description:", info["public_description"])
    print("Number of subscribers:", info["subscribers"])

# Step 5: Subreddit rules
print("\n--- Rules ---")
rules = get_data(rules_url)
if rules is not None:
    number = 1
    for rule in rules["rules"]:
        print(number, "-", rule["short_name"])
        number = number + 1

# Step 6: The 10 newest posts
print("\n--- 10 Newest Posts ---")
posts = get_data(posts_url)
if posts is not None:
    number = 1
    for post in posts["data"]["children"]:
        print(number, "-", post["data"]["title"])
        number = number + 1