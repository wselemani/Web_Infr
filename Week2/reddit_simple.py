import requests

# Step 1: Choose the subreddit we want information about
subreddit = "python"

# Step 2: Set a User-Agent header.
# Reddit requires this so it knows who is making the request.
# Without it, Reddit may block us.
headers = {"User-Agent": "script:alu.subreddit.info:v1.0 (by /u/wezzie_malisa)"}

# Step 3: Build the URLs for the three things we need
about_url = f"https://api.reddit.com/r/{subreddit}/about"
rules_url = f"https://api.reddit.com/r/{subreddit}/about/rules"
posts_url = f"https://api.reddit.com/r/{subreddit}/new?limit=10"

# Step 4: Get the subreddit name, description and number of subscribers
response = requests.get(about_url, headers=headers)
print(response.status_code)
print(response.text[:300])

if response.status_code == 200:
    data = response.json()["data"]
    print("Subreddit name:", data["display_name"])
    print("Description:", data["public_description"])
    print("Number of subscribers:", data["subscribers"])
else:
    print("Could not get subreddit info. Status code:", response.status_code)

# Step 5: Get the subreddit rules
response = requests.get(rules_url, headers=headers)

print("\nRules:")
if response.status_code == 200:
    rules = response.json()["rules"]
    number = 1
    for rule in rules:
        print(number, "-", rule["short_name"])
        number = number + 1
else:
    print("Could not get rules. Status code:", response.status_code)

# Step 6: Get the 10 newest posts
response = requests.get(posts_url, headers=headers)

print("\n10 Newest posts:")
if response.status_code == 200:
    posts = response.json()["data"]["children"]
    number = 1
    for post in posts:
        print(number, "-", post["data"]["title"])
        number = number + 1
else:
    print("Could not get posts. Status code:", response.status_code)
