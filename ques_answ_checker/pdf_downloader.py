import os
import requests
import re

class PDFDownloader:
    def __init__(self, save_dir="/workspaces/codespaces-blank/ques_answ_checker/Data"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def sanitize_filename(self, title):
        """Sanitize file name to remove invalid characters."""
        return re.sub(r'[\\/*?:"<>|]', "_", title)

    def download_pdf(self, pdf_link, title):
        """
        pdf_link: dict with keys 'url' and 'label'
        title: string used as filename
        """
        if not isinstance(pdf_link, dict) or 'url' not in pdf_link:
            print("⚠️ Invalid pdf_link format")
            return

        url = pdf_link['url']
        filename = self.sanitize_filename(title) + ".pdf"
        filepath = os.path.join(self.save_dir, filename)

        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ Saved: {filename}")
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
