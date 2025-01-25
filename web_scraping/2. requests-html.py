from requests_html import HTMLSession
from datetime import datetime
def render_javascript(url):
    """
    Demonstrates how to render JavaScript using the `requests-html` library.
    This function fetches the page content after JavaScript has been executed.

    Parameters:
    url : str
        The URL of the website to scrape.

    Returns:
    None
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found
        print("Rendered web page:", response.html.html)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def extract_information(url):
    """
    Extracts and prints specific information from a webpage using CSS selectors.

    Parameters:
    url : str
        The URL of the website to scrape.

    Returns:
    None
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        # print(response.html.html)
        title_tag = response.html.find('h1')
        print(len(title_tag), "title tags found:")
        print("Title: ", title_tag[0].text)


        datetime_element = response.html.find('time', first=True)
        # datetime = datetime_element.attrs['datetime']
        # print("Datetime attribute: ", datetime)
        # print("Datetime:" , datetime_element.text)
        
        parsed_datetime = datetime.strptime(datetime_element.text, '%b %d, %Y %H:%M')  # Parse input
        formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Format output
        print("Formatted Datetime: ", formatted_datetime)
      

      
        # advanced usages of extraction
        temp = response.html.xpath('//*[@id="post_275181"]/div[2]/section[1]/div[2]/div/section[1]/time', first=True)
        # print(temp.text)
        # datetime = temp.attrs['datetime']
        # print(datetime)

        body = response.html.find('article.post-details')
        # print(len(title_tag), "title tags found:")
        print("Body is  found : ", body[0].text)

        # Example: Extracting all links
        links = response.html.find('a')
        print(len(links), "links found:")

        # for link in links:
        #     print("Link Text: ", link.text, "Link href: ", link.attrs['href'])
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def main():
    """
    Main function to execute the web scraping examples.
    """
    # print("Rendering JavaScript on a web page...")
    # render_javascript('https://example.com')

    print("\nExtracting information from a web page...")
    extract_information('https://thefinancialexpress.com.bd/trade/annual-business-conference-2025-of-midland-bank-plc-held')

if __name__ == "__main__":
    main()
