import json
import os

def fix_pdf_link(link):
    """Convert plain URL to a dict with label + URL."""
    filename = os.path.basename(link).split('.')[0].replace('-', ' ').replace('_', ' ').strip()
    label = filename if filename else "Download PDF"
    return {
        "url": link,
        "label": label
    }

def clean_course_data(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    for course in data:
        # Promote main_title to top-level title if different
        if 'dpp_content' in course:
            dpp_main_title = course['dpp_content'].get('main_title', '').strip()
            if dpp_main_title and dpp_main_title != course.get('title', '').strip():
                course['title'] = dpp_main_title

            # Remove main_title inside dpp_content
            course['dpp_content'].pop('main_title', None)

            # Fix pdf_link to be a dict with url and label
            for lesson in course['dpp_content'].get('lessons', []):
                if 'pdf_link' in lesson and isinstance(lesson['pdf_link'], str):
                    lesson['pdf_link'] = fix_pdf_link(lesson['pdf_link'])

    # Save the cleaned data
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    print(f"✅ Cleaned data written to {output_path}")

# Example usage
if __name__ == "__main__":
    clean_course_data(r"/workspaces/codespaces-blank/ques_answ_checker/physics_jbnu.json", "physics_jbnu_cleaned.json")
