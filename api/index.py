from flask import Flask, render_template, url_for, jsonify, send_file, request
import pandas as pd
import os
from collections import defaultdict

# CRITICAL: Find the project root directory (one level up from /api)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure Flask to look for templates and static files in the ROOT folder
app = Flask(__name__, 
            template_folder=os.path.join(ROOT_DIR, 'templates'),
            static_folder=os.path.join(ROOT_DIR, 'static'))

# Update Constants with absolute paths
API_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_IN_API = os.path.join(API_DIR, "final_QA_report.xlsx")
EXCEL_FILE_IN_ROOT = os.path.join(ROOT_DIR, "final_QA_report.xlsx")
EXCEL_FILE = EXCEL_FILE_IN_API if os.path.exists(EXCEL_FILE_IN_API) else EXCEL_FILE_IN_ROOT
IMAGE_STORAGE = os.path.join(ROOT_DIR, "static", "images")

def read_excel_sheet(sheet_name):
    if not os.path.exists(EXCEL_FILE):
        print(f"Excel file NOT found at: {EXCEL_FILE}")
        return []
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading {sheet_name}: {e}")
        return []

def find_image_path(filename):
    """Finds the first occurrence of an image in any student folder."""
    if not os.path.exists(IMAGE_STORAGE): return None
    for student in os.listdir(IMAGE_STORAGE):
        path = os.path.join(IMAGE_STORAGE, student, filename)
        if os.path.exists(path):
            return url_for('static', filename=f'images/{student}/{filename}')
    return None

@app.route("/")
def home():
    data = read_excel_sheet("Summary")
    return render_template("index.html", tables=data, active_page='home')

@app.route("/errors")
def errors():
    data = read_excel_sheet("Errors")
    return render_template("errors.html", tables=data, active_page='errors')

@app.route("/voting")
def voting():
    # Group flat data by image
    raw_data = read_excel_sheet("Voting")
    grouped = defaultdict(list)
    for row in raw_data:
        img_name = str(row.get("image"))
        row["img_url"] = find_image_path(img_name)
        grouped[img_name].append(row)
    
    # Create summarized image list
    summary_list = []
    for img_name, votes in grouped.items():
        summary_list.append({
            "image": img_name,
            "img_url": votes[0].get("img_url"),
            "voting_summary": votes[0].get("voting_summary", "Calculating..."),
            "votes": votes,
            "total_votes": len(votes)
        })

    # Pagination Logic
    page = request.args.get('page', 1, type=int)
    per_page = 50
    total_images = len(summary_list)
    total_pages = (total_images + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_images = summary_list[start_idx:end_idx]
    
    return render_template("voting_grouped.html", 
                           images=paginated_images, 
                           page=page, 
                           total_pages=total_pages,
                           total_images=total_images,
                           active_page='voting')

@app.route("/review")
def review():
    data = read_excel_sheet("Review")
    for row in data:
        row["img_url"] = find_image_path(row.get("image"))
    return render_template("review.html", tables=data, active_page='review')

@app.route("/download-excel")
def download_excel():
    if not os.path.exists(EXCEL_FILE):
        return "File not found", 404
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
