import json
import time
import os
import requests  # for downloading PDFs
from CourseDetailScraper import CourseDetailScraper
from CourseScrapper import CourseScrapper

class PDFDownloader:
    def __init__(self, save_dir='pdfs'):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def download_pdf(self, pdf_info, title=None):
        url = pdf_info.get('url')
        label = pdf_info.get('label', 'downloaded_pdf')

        # Sanitize filename
        if title:
            filename = f"{title}.pdf"
        else:
            # fallback from label
            filename = f"{label}.pdf"
        
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
        filepath = os.path.join(self.save_dir, filename)

        try:
            print(f"⬇️ Downloading PDF: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Saved PDF to: {filepath}")
        except Exception as e:
            print(f"⚠️ Failed to download PDF {url}: {e}")

def fix_pdf_link(link):
    """Convert PDF link string into a dict with 'url' and 'label'."""
    filename = os.path.basename(link).split('.')[0].replace('-', ' ').replace('_', ' ').strip()
    label = filename if filename else "Download PDF"
    return {
        "url": link,
        "label": label
    }

def main():
    # Initialize scrapers
    dpp_scrapper = CourseDetailScraper()
    course_scrapper = CourseScrapper()
    pdf_downloader = PDFDownloader()

    # List of paginated URLs
    page_link_list = [
        'https://physicsaholics.com/Course/index/1',
        'https://physicsaholics.com/Course/index/2',
        'https://physicsaholics.com/Course/index/3',
        'https://physicsaholics.com/Course/index/4',
        'https://physicsaholics.com/Course/index/5',
        'https://physicsaholics.com/Course/index/6',
        'https://physicsaholics.com/Course/index/7',
    ]

    all_courses = []

    # Scrape all pages
    for page_url in page_link_list:
        course_list = course_scrapper.scrape_course_data(page_url)
        print(f"✅ Fetched {len(course_list)} courses from {page_url}")
        time.sleep(2)

        for course in course_list:
            try:
                dpp_data = dpp_scrapper.get_data(course['link'])
                print(f"🔍 DPP fetched for: {course['title']}")

                # Promote 'main_title' to top-level title if different
                if 'main_title' in dpp_data:
                    dpp_main_title = dpp_data['main_title']
                    if dpp_main_title and dpp_main_title != course['title']:
                        course['title'] = dpp_main_title
                    dpp_data.pop('main_title', None)

                # Fix PDF link formatting
                for lesson in dpp_data.get('lessons', []):
                    if isinstance(lesson.get('pdf_link'), str):
                        lesson['pdf_link'] = fix_pdf_link(lesson['pdf_link'])
                        
                        # Optionally download the PDF here:
                        pdf_downloader.download_pdf(
                            lesson['pdf_link'], 
                            title=f"{course['title']} - {lesson.get('title', 'Lesson')}"
                        )

                # Attach DPP content
                course['dpp_content'] = dpp_data

            except Exception as e:
                print(f"⚠️ Error fetching DPP for {course['title']}: {e}")
                course['dpp_content'] = {}

            time.sleep(2)

        all_courses.extend(course_list)

    # Save to file
    output_path = 'physics_jbnu.json'
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(all_courses, file, indent=4, ensure_ascii=False)

    print(f"✅ All course data saved to {output_path}")

if __name__ == "__main__":
    main()
