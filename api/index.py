from flask import Flask, render_template, url_for, jsonify
import pandas as pd
import os
from collections import defaultdict

app = Flask(__name__)

# Constants
EXCEL_FILE = "final_QA_report.xlsx"
IMAGE_STORAGE = os.path.join("static", "images")

def read_excel_sheet(sheet_name):
    if not os.path.exists(EXCEL_FILE): return []
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        # Ensure 'accuracy' and 'score' are rounded or handled correctly
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
        # All votes for the same image share the same summary string
        summary_list.append({
            "image": img_name,
            "img_url": votes[0].get("img_url"),
            "voting_summary": votes[0].get("voting_summary", "Calculating..."),
            "votes": votes,
            "total_votes": len(votes)
        })
    
    return render_template("voting_grouped.html", images=summary_list, active_page='voting')

@app.route("/review")
def review():
    data = read_excel_sheet("Review")
    for row in data:
        row["img_url"] = find_image_path(row.get("image"))
    return render_template("review.html", tables=data, active_page='review')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
