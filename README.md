# ⚡ Binke: ML Annotation Quality Control System

**Binke** is a state-of-the-art Quality Control (QC) and consensus analysis platform designed for Large-Scale Machine Learning (ML) image annotation projects. It bridges the gap between raw student submissions and final, verified datasets by providing a transparent, statistically-grounded, and visually stunning dashboard for auditors.

---

## 🚀 Key Features

### 📦 Robust Data Ingestion
- **ZIP-Based Workflow**: Automatically scans the `annotations/` directory for individual student submissions in ZIP format.
- **Recursive XML Harvesting**: Recursively searches through complex nested ZIP structures to find every `.xml` annotation file.
- **Mixed Content Handling**: Seamlessly extracts accompanying images (JPG, PNG, WebP) while filtering out noise.
- **Student Attribution**: Automatically maps annotations to student names based on the ZIP filename.

### ⚖️ Advanced Voting & Consensus Logic
- **Weighted Majority Algorithm**: Implements a three-tier consensus system (Strong Majority, Weak Warning, and Noise Filtering).
- **Uncertainty Detection**: Proactively flags highly ambiguous images where annotator agreement is low (<70%).
- **Strict Complexity Enforcement**: Ensures that the core "Complexity" level of an image follows an absolute 50%+ majority rule.

### 📊 Real-Time Analytics Dashboard
- **Grouped Image Inspection**: Collapses hundreds of student rows into single, digestible image entries.
- **Accordion Detail Drills**: Instantly expandable rows allowing auditors to view every student's specific contribution.
- **Binke Inspection Modal**: A side-by-side verification tool with high-resolution image zoom and metadata summary.
- **Student Leaderboard**: Tracks total images processed, error rates, warning frequencies, and overall accuracy scores.

---

## 🧠 The Logic: Under the Hood

### 1. The Rule Engine (`check_rules`)
Before consensus is calculated, every single image is passed through a deterministic rule engine to check for logical inconsistencies:
- **Missing Complexity**: Flags if a mandatory complexity tag (e.g., `complex 1`) is forgotten.
- **Multiple Complexity**: Flags if a student provides contradictory complexity levels.
- **No Annotation Conflict**: Detects cases where "No Annotation" is combined with other contradicting tags.
- **Night/Weather Validation**: Generates warnings if `night_dark`, `Rain`, `Fog`, or `Snow` are tagged without the accompanying `blurred` tag, as per project guidelines.

### 2. The Consensus Algorithm (`get_voting_summary`)
Traditional "Winner Takes All" voting often hides subtle disagreements. Binke uses a **tiered consensus model**:

| Agreement Range | Classification | Indicator | Dashboard Representation |
| :--- | :--- | :--- | :--- |
| **>= 50%** | **Strong Majority** | ✅ | Included as a standard tag in the summary. |
| **20% - 50%** | **Warning (Weak)** | ⚠️ | Included with a warning icon and vote count. |
| **< 20%** | **Noise** | ❌ | Discarded entirely to prevent outlier corruption. |

*Note: Complexity tags do not support Warning states—they are either Strong Majorities or they are excluded.*

### 3. Student Accuracy Scoring
Accuracy is not just "matching the majority." In Binke, a student's score for an image is calculated as:
$$Score = \frac{Intersection(StudentTags, StrongMajority)}{Count(StrongMajority)}$$
If no **Strong Majority** can be established for an image, the image is considered a total failure of consensus, and all students receive a base score of 0.0 for that specific instance.

---

## 🛠️ Technology Stack

- **Backend Logic**: Python 3.x
- **Data Manipulation**: `Pandas` (Core engine for Excel transformations)
- **Excel Engineering**: `Openpyxl` (Custom chart generation and multi-sheet reporting)
- **Web App**: `Flask` (Lightweight, robust WSGI server)
- **Theme/UI**: **Binke Soft-Neobrutalist** (Custom Vanilla CSS, Google Fonts 'Plus Jakarta Sans', and Lucide Icons)

---

## 📂 Project Architecture

```text
/checking
├── annotations/            # INPUT: Drop student ZIP files here
├── static/
│   ├── images/             # AUTO: Extracted images organized by student
│   └── style.css           # UI: The Binke Design System
├── templates/
│   ├── layout.html         # UI: Sidebar & Base Navigation
│   ├── index.html          # UI: Performance Leaderboard
│   ├── errors.html         # UI: Rule Violation Report
│   └── voting_grouped.html # UI: Image-based consensus grid
├── extracted_xmls/         # AUTO: Temporary storage for parsed student XMLs
├── qa_processor.py         # LOGIC: The core brain (Extraction -> Rules -> Excel)
├── app.py                  # SERVER: The Flask dashboard server
└── final_QA_report.xlsx    # OUTPUT: Complete statistical export for stakeholders
```

---

## 🚦 Getting Started

### 1. Installation
Install the necessary Python dependencies:
```bash
pip install pandas openpyxl flask
```

### 2. Prepare Data
Simply drop your student submissions (`StudentName.zip`) into the `annotations/` folder. Ensure the ZIP contains `.xml` files.

### 3. Generate Analysis
Run the processor to extract data and build the Excel report:
```bash
python qa_processor.py
```
*Note: Ensure the Excel file is closed if you are re-running this command.*

### 4. Launch Dashboard
Start the web interface:
```bash
python app.py
```
The dashboard will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⚡ The Binke Brand Identity
The dashboard uses a custom **Neobrutalist Agency Theme** characterized by:
- **Colors**: Deep Midnight Sidebar, Lavender Accents, and Lime Green Success markers.
- **Depth**: Solid black offsets (`box-shadow: 6px 6px 0px #000`) instead of blurry shadows.
- **Interactivity**: Zoom-capable image inspectors and accordion-style data expansion.

---
© 2026 Binke - Advanced Machine Learning Quality Control.
