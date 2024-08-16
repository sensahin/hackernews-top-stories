import requests
import time
from datetime import datetime

def get_top_stories_last_24_hours(limit=50):
    # Get the current timestamp
    current_time = int(time.time())

    # Define the time range for the last 24 hours
    time_range = 24 * 60 * 60  # 24 hours in seconds

    # Get the list of top story IDs
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    story_ids = response.json()

    stories = []
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url)
        story_data = story_response.json()

        # Calculate the story's age in seconds
        story_time = story_data.get('time')
        story_age = current_time - story_time

        # Check if the story is within the last 24 hours
        if story_age <= time_range:
            # Convert the Unix timestamp to a human-readable format
            story_datetime = datetime.fromtimestamp(story_time).strftime('%Y-%m-%d %H:%M:%S')

            story_info = {
                'title': story_data.get('title'),
                'url': story_data.get('url'),
                'score': story_data.get('score'),
                'by': story_data.get('by'),
                'time': story_datetime,  # Use the formatted date and time
            }
            stories.append(story_info)

        # Stop if we have collected enough stories
        if len(stories) >= limit:
            break

    # Sort stories by score in descending order
    sorted_stories = sorted(stories, key=lambda x: x['score'], reverse=True)

    return sorted_stories[:limit]

# Example usage
popular_stories = get_top_stories_last_24_hours(limit=50)
for idx, story in enumerate(popular_stories, start=1):
    print(f"{idx}. {story['title']} ({story['url']}) - {story['score']} points by {story['by']} on {story['time']}")
