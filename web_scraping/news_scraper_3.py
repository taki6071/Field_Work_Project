import requests
from bs4 import BeautifulSoup
from datetime import datetime
import db_connection
import news_insert

# URL of the page to scrape
url = 'https://thefinancialexpress.com.bd/trade'

# Send a GET request to fetch the HTML content
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
articles = soup.find_all('article')
base_url = 'https://thefinancialexpress.com.bd'
conn = db_connection.create_db_connection()

# Use a default editor ID that we know exists in the editors table
DEFAULT_EDITOR_ID = 1  # Make sure this ID exists in your editors table

for article in articles:
    link = article.find('a', href=True)
    if link:
        article_link = base_url + link['href']
        print(f"Fetching article: {article_link}")
        
        try:
            article_response = requests.get(article_link)
            if article_response.status_code != 200:
                print(f"Failed to fetch article. Status code: {article_response.status_code}")
                continue
            
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            
            # Extract title
            title_tag = article_soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else 'No Title'
            
            # Extract author
            author_tag = article_soup.find('p', class_='hidden md:block text-p-light dark:text-p-dark py-1 xl:py-2 px-2 text-center font-semibold uppercase text-sm xl:text-base')
            if author_tag:
                author_link = author_tag.find('a')
                author_name = author_link.get_text(strip=True) if author_link else 'Unknown Author'
                if not author_name:
                    author_name = 'Prothom Alo'
            else:
                author_name = 'Unknown Author'
            
            # Extract time
            time_tag = article_soup.find('time', class_='text-xs xl:text-sm text-p-light dark:text-p-dark')
            publish_time = None
            if time_tag:
                time_str = time_tag.get_text(strip=True)
                publish_time = datetime.strptime(time_str, '%b %d, %Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
            
            # Extract description
            description_tag = article_soup.find('article', id='main-single-post')
            if description_tag:
                paragraphs = description_tag.find_all('p')
                description = ' '.join(p.get_text(strip=True) for p in paragraphs)
            else:
                description = 'No Description'
            
            print(f"Author: {author_name}")
            if publish_time:
                print(f"Published time: {publish_time}")
            
            # Check if author exists first
            author_id = news_insert.get_author_id(connection=conn, name=author_name)
            
            # If author doesn't exist, create new author
            if not author_id:
                try:
                    authorEmail = f"{author_name.replace(' ', '')}@gmail.com"
                    news_insert.insert_author(connection=conn, name=author_name, email=authorEmail)
                    author_id = news_insert.get_author_id(connection=conn, name=author_name)
                except Exception as e:
                    print(f"Error inserting author: {e}")
                    author_id = 1  # Default author ID
            
            news_insert.insert_category(connection=conn , name="TRADE" , description=description)
            # Insert news with default editor ID
            if publish_time:
                news_insert.insert_news(
                    connection=conn,
                    category_id=1,
                    author_id=author_id,
                    editor_id=DEFAULT_EDITOR_ID,  # Use default editor ID
                    datetime=publish_time,
                    title=title,
                    body=description,
                    link=article_link
                )
            
        except Exception as e:
            print(f"Error processing article {article_link}: {e}")