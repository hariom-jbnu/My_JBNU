import requests
from bs4 import BeautifulSoup
import json


class CourseScrapper:

    def __init__(self):
        pass

    def scrape_course_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # raise error for bad status
        except Exception as e:
            return {"error": str(e)}

        soup = BeautifulSoup(response.content, 'html.parser')

        # Targeting the structure based on your sample HTML
        container = soup.select_one('section:nth-of-type(2) div.row')
        if not container:
            return {"error": "Content section not found"}

        data = []
        articles = container.select('article')

        for article in articles:
            try:
                title_tag = article.select_one('h6 a')
                sub_title_tag = article.select_one('.course1')
                link = title_tag['href'] if title_tag else None
                title = title_tag.get_text(strip=True) if title_tag else None
                sub_title = sub_title_tag.get_text(strip=True) if sub_title_tag else None

                if title and link:
                    data.append({
                        "title": title,
                        "sub_title": sub_title,
                        "link": link
                    })
            except Exception:
                continue  # skip if structure is broken

        return data


# Example usage
if __name__ == "__main__":
    url = "https://physicsaholics.com/Course/index/1"  # Replace with your actual URL
    scraper = CourseScrapper()
    result = scraper.scrape_course_data(url)
    print(json.dumps(result, indent=4, ensure_ascii=False))
