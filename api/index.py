from flask import Flask, render_template, url_for, jsonify, send_file, request
import pandas as pd
import os
from collections import defaultdict, Counter
import re

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
    # Load and calculate global stats for the overview
    voting_data = read_excel_sheet("Voting")
    summary_data = read_excel_sheet("Summary")
    
    # Unique images count
    unique_images = len(set(str(row.get("image")).strip() for row in voting_data if not pd.isna(row.get("image"))))
    
    # Label breakdown (calculate from all voting summary strings)
    global_label_counts = Counter()
    for row in voting_data:
        v_summary = str(row.get("voting_summary", ""))
        labels_found = re.findall(r'([a-zA-Z0-9_\s]+?)\s*(?:⚠️)?\s*\(\d+\)', v_summary)
        for lbl in labels_found:
            clean_lbl = lbl.strip().upper()
            if clean_lbl:
                global_label_counts[clean_lbl] += 1
    
    # Sort top labels
    label_stats = dict(global_label_counts.most_common(12))
    
    return render_template("index.html", 
                           tables=summary_data, 
                           total_images=unique_images,
                           label_stats=label_stats,
                           active_page='home')

@app.route("/errors")
def errors():
    data = read_excel_sheet("Errors")
    return render_template("errors.html", tables=data, active_page='errors')

@app.route("/voting")
def voting():
    raw_data = read_excel_sheet("Voting")
    grouped = defaultdict(list)
    
    # Phase Filtering
    # If the user has a "phase" column in the sheet, use it; otherwise, everything is Phase 1
    phases_found = set()
    current_phase = request.args.get('phase', 'Phase 1').strip()
    
    for row in raw_data:
        # Automatically detect phases if the column exists
        phase_val = str(row.get("phase", "Phase 1")).strip() if "phase" in row else "Phase 1"
        phases_found.add(phase_val)
        
        img_raw = row.get("image")
        if pd.isna(img_raw): continue
        
        # Filter by selected phase
        row_phase = str(row.get("phase", "Phase 1")).strip() if "phase" in row else "Phase 1"
        if row_phase != current_phase: continue
        
        img_name = str(img_raw).strip()
        if not img_name or img_name.lower() in ["nan", "none"]: continue
        
        row["img_url"] = find_image_path(img_name)
        grouped[img_name].append(row)
    
    # Sort phases for the UI selector
    all_phases = sorted(list(phases_found)) if phases_found else ["Phase 1"]
    
    # Search Query
    query = request.args.get('q', '').lower()
    
    # Create summarized image list and calculate Global Label Stats
    summary_list = []
    global_label_counts = Counter()
    
    for img_name, votes in grouped.items():
        v_summary = str(votes[0].get("voting_summary", ""))
        
        # Robust parsing for label stats
        labels_found = re.findall(r'([a-zA-Z0-9_\s]+?)\s*(?:⚠️)?\s*\(\d+\)', v_summary)
        for lbl in labels_found:
            clean_lbl = lbl.strip().upper()
            if clean_lbl:
                global_label_counts[clean_lbl] += 1

        img_data = {
            "image": img_name,
            "img_url": votes[0].get("img_url"),
            "voting_summary": v_summary,
            "votes": votes,
            "total_votes": len(votes)
        }
        
        # Filter logic
        if not query or query in v_summary.lower() or query in img_name.lower():
            summary_list.append(img_data)
    
    # Sort global stats by frequency
    sorted_labels = dict(global_label_counts.most_common(8))

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
                           query=query,
                           label_stats=sorted_labels,
                           all_phases=all_phases,
                           current_phase=current_phase,
                           active_page='voting')

@app.route("/review")
def review():
    data = read_excel_sheet("Review")
    for row in data:
        row["img_url"] = find_image_path(row.get("image"))
    return render_template("review.html", tables=data, active_page='review')

@app.route("/plan")
def plan():
    content = ""
    plan_path = os.path.join(os.getcwd(), "plan.md")
    if os.path.exists(plan_path):
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
    return render_template("plan.html", content=content, active_page='plan')

@app.route("/download-excel")
def download_excel():
    if not os.path.exists(EXCEL_FILE):
        return "File not found", 404
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
