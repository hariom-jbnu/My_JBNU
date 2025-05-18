import requests
from bs4 import BeautifulSoup
import json

class CourseDetailScraper:
    def __init__(self):
        self.soup = None

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch page: {e}")

    def extract_main_title(self):
        try:
            title_tag = self.soup.select_one("section:nth-of-type(1) div > div > div:nth-of-type(1) h6")
            return title_tag.get_text(strip=True) if title_tag else None
        except Exception:
            return None

    def extract_cards(self):
        cards = []
        articles = self.soup.select("section:nth-of-type(1) div > div > div:nth-of-type(2) article")

        for article in articles:
            try:
                title_tag = article.select_one(".bottom-text h6")
                pdf_link_tag = article.select_one(".bottom-text a[href$='.pdf']")
                youtube_iframe = article.select_one("iframe")

                title = title_tag.get_text(strip=True) if title_tag else None
                pdf_link = pdf_link_tag['href'] if pdf_link_tag else None
                yt_link = youtube_iframe['src'] if youtube_iframe else None

                cards.append({
                    "title": title,
                    "pdf_link": pdf_link,
                    "yt_link": yt_link
                })
            except Exception:
                continue

        return cards

    def get_data(self, url):
        self.fetch_page(url)
        return {
            "main_title": self.extract_main_title(),
            "lessons": self.extract_cards()
        }

# Example usage:
if __name__ == "__main__":
    url = "https://physicsaholics.com/home/courseDetails/92"  # Change to your desired URL
    scraper = CourseDetailScraper()
    try:
        data = scraper.get_data(url)
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    scraper = CourseDetailScraper()
    json_data = scraper.get_data(r"https://physicsaholics.com/home/courseDetails/92")

    try:
        data = scraper.get_data()
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
