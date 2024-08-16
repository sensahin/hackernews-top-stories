import requests
import time
from datetime import datetime

def get_top_stories_last_24_hours(limit=50):
    current_time = int(time.time())
    time_range = 24 * 60 * 60  # 24 hours in seconds
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    story_ids = response.json()

    stories = []
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url)
        story_data = story_response.json()

        story_time = story_data.get('time')
        story_age = current_time - story_time

        if story_age <= time_range:
            story_datetime = datetime.fromtimestamp(story_time).strftime('%Y-%m-%d %H:%M:%S')
            story_info = {
                'title': story_data.get('title'),
                'url': story_data.get('url'),
                'score': story_data.get('score'),
                'by': story_data.get('by'),
                'time': story_datetime,
                'id': story_data.get('id')  # Include the story ID for comments link
            }
            stories.append(story_info)

        if len(stories) >= limit:
            break

    sorted_stories = sorted(stories, key=lambda x: x['score'], reverse=True)

    return sorted_stories[:limit]

# Generate the HTML email body
popular_stories = get_top_stories_last_24_hours(limit=50)
email_body = """
<html>
<head></head>
<body>
    <h2>Here are the most popular Hacker News stories from the last 24 hours:</h2>
    <ol>
"""
for idx, story in enumerate(popular_stories, start=1):
    comments_link = f'https://news.ycombinator.com/item?id={story["id"]}'
    email_body += f'<li><a href="{story["url"]}">{story["title"]}</a> - {story["score"]} points by {story["by"]} on {story["time"]} - <a href="{comments_link}">Comments</a></li>\n'

email_body += """
    </ol>
</body>
</html>
"""

# Save the HTML email body to a file
with open('email_body.html', 'w') as f:
    f.write(email_body)
