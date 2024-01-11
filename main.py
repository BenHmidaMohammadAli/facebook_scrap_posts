from fastapi import FastAPI
from facebook_scraper import get_posts
import csv

app = FastAPI()

@app.get("/scrape/{page_username}")
def scrape_facebook_page(page_username: str):
    posts_data = []

    # Scrape the Facebook page
    try:
        # Scrape the Facebook page
        posts_generator = get_posts(page_username, pages=5)
        for post in list(posts_generator)[:10]:
            posts_data.append({
                'text': post['text'],
                'likes': post['likes'],
                'comments': post['comments'],
                'shares': post['shares'],
                'time': post['time'],
            })
    except Exception as e:
        print(f"-------- An error occurred: {e}")

    print(len(posts_data))
    
    # Save the scraped data to a CSV file
    csv_file_path = f"{page_username}_posts.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['text', 'likes', 'comments', 'shares', 'time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts_data)

    return {"message": f"Scraped data saved to {csv_file_path}"}
