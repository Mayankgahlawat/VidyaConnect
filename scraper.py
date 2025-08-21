import requests
from bs4 import BeautifulSoup
from app import create_app, db
from app.models import Job
import re

# Create a Flask app instance to access the database
app = create_app()

def find_hiring_thread_url():
    """Finds the URL of the latest 'Who is hiring?' thread on Hacker News."""
    print("Finding the latest 'Who is hiring?' thread...")
    search_url = "https://hn.algolia.com/api/v1/search?query=who%20is%20hiring&tags=story"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if data['hits']:
            thread_id = data['hits'][0]['objectID']
            return f"https://news.ycombinator.com/item?id={thread_id}"
    except requests.exceptions.RequestException as e:
        print(f"Could not find the hiring thread: {e}")
    return None

def scrape_jobs():
    hiring_url = find_hiring_thread_url()
    if not hiring_url:
        return

    print(f"Scraping jobs from: {hiring_url}")
    
    try:
        response = requests.get(hiring_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # CORRECTED SELECTOR: Find all comment table rows
    comments = soup.select('tr.comtr')
    new_jobs_found = 0

    with app.app_context():
        for comment in comments:
            # CORRECTED SELECTOR: Find the comment content within the div
            comment_text_element = comment.select_one('div.comment')
            if comment_text_element:
                comment_text = comment_text_element.get_text(separator=' ').strip()
                
                lines = comment_text.split('\n')
                if not lines:
                    continue

                title_line = lines[0]
                job_title = title_line[:150]
                company_name = "Various (see link)"

                # CORRECTED SELECTOR: Find the permalink within the comment
                link_tag = comment.select_one('a[href^="item?id="]')
                job_url = f"https://news.ycombinator.com/{link_tag['href']}" if link_tag else hiring_url

                if Job.query.filter_by(url=job_url).first():
                    continue

                new_job = Job(
                    title=job_title,
                    company=company_name,
                    location="Remote available",
                    url=job_url,
                    category='cs_job'
                )
                db.session.add(new_job)
                new_jobs_found += 1

        if new_jobs_found > 0:
            db.session.commit()
            print(f"Success! Found and saved {new_jobs_found} new jobs.")
        else:
            print("No new jobs found to save.")

if __name__ == '__main__':
    scrape_jobs()