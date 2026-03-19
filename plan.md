
```markdown
# 🚗 Indian License Plate Recognition (LPR) System

![Project Status](https://img.shields.io/badge/status-in%20progress-yellow)
![ML Pipeline](https://img.shields.io/badge/pipeline-detection%20%2B%20OCR-blue)
![Dataset](https://img.shields.io/badge/dataset-custom-green)

---

## 📌 Overview

This project aims to build a complete **License Plate Recognition (LPR)** system for Indian vehicles using a **2-stage deep learning pipeline**:

1. **Detection Model** → Finds license plates in images  
2. **OCR Model** → Reads text from detected plates  

---

## 🧠 System Architecture

```mermaid
flowchart TD
    A["📸 Input Image / Video"] 
    --> B["🔍 Detection Model<br>(YOLOv8 / YOLOv11)"]
    --> C["📦 Bounding Box + Confidence"]
    --> D["✂️ Cropping Module<br>(OpenCV)"]
    --> E["🔤 OCR Model<br>(EasyOCR / PaddleOCR / LPRNet)"]
    --> F["📝 License Plate Text<br>e.g. KA01AB1234"]

    classDef default fill:#f8f9fa,stroke:#333,stroke-width:2px;
    classDef input fill:#e3f2fd;
    classDef output fill:#e8f5e9;
    class A input
    class F output
```

---

## 🔁 End-to-End Pipeline

```mermaid
flowchart LR
    A[1. Data Collection] 
    --> B[2. Bounding Box Annotation]
    --> C[3. Train Detection Model]
    --> D[4. Auto Cropping]
    --> E[5. Create OCR Dataset]
    --> F[6. Train OCR Model]
    --> G[7. Integrate System]
    --> H[8. Evaluate & Optimize]
```

---

## 📦 Dataset Strategy

### 🔹 Detection Dataset
- **Input**: Full vehicle images  
- **Annotation**: Bounding boxes (YOLO format)

```yaml
class x_center y_center width height
```

### 🔹 OCR Dataset
- **Input**: Cropped plates  
- **Annotation**: Text only

**Example**: `img_001.jpg` → `KA01AB1234`

### 🔁 Data Flow

```mermaid
flowchart TD
    A[Raw Images] 
    --> B[Bounding Box Annotation]
    --> C[Detection Dataset]
    --> D[Auto Cropping Script]
    --> E[Cropped Plates]
    --> F[Text Labeling]
    --> G[OCR Dataset]
```

---

## ✏️ Annotation Guidelines

### ✅ Detection Rules
- Tight bounding boxes only  
- Include entire plate  
- Avoid background noise  

### 🔤 OCR Rules
- Exact text (no guessing)  
- Maintain Indian format (KA01AB1234, DL7C1234, etc.)  

### ❌ Common Mistakes to Avoid
- Loose boxes  
- Cut-off characters  
- Confusing O/0, I/1, B/8  

### 🏷️ Optional Attributes
```text
blur: yes/no
tilted: yes/no
occluded: yes/no
night: yes/no
```

---

## 👥 Team Workflow
- **Team A** → Bounding Box Annotation  
- **Team B** → Quality Check  
- **Team C** → Cropping + OCR Labeling  
- **Team D** → Final Validation  

---

## ⚙️ Detection Model
**Recommended**: YOLOv8 / YOLOv11  
**Metrics**: mAP@0.5, mAP@0.5:0.95

---

## ✂️ Cropping Module
Simple OpenCV script (not a model).

---

## 🔤 OCR Model
**Recommended Options**:
- EasyOCR (quick start)
- PaddleOCR (better for Indian fonts)
- LPRNet / CRNN (custom trained)

**Metrics**: Character Accuracy + Full Plate Accuracy

---

## 🔁 Integration Pipeline

```mermaid
flowchart LR
    Image["Image / Video"] 
    --> Det["Detection Model"]
    --> Box["Bounding Box"]
    --> Crop["Cropping"]
    --> OCR["OCR Model"]
    --> Text["Clean Text Output"]
```

### 🎥 Real-Time Pipeline

```mermaid
flowchart LR
    Cam["Camera / CCTV"] 
    --> Det["Detection"]
    --> Crop["Crop"]
    --> OCR["OCR"]
    --> Display["Display / Store / Alert"]
```

---

## ⚠️ Challenges & Improvements

**Main Challenges**:
- Small/distant plates
- Dirty, reflective, multi-line plates
- Similar characters (0/O, 1/I, etc.)

**Improvements**:
- Heavy data augmentation
- Perspective correction
- End-to-end model (future)

---

## 🔐 Legal Considerations
- License plates contain sensitive data  
- **Never** publicly share raw dataset  
- Use IDD dataset or synthetic data for sharing

---

## 📁 Project Structure

```bash
indian-lpr/
├── data/
│   ├── raw_images/
│   ├── detection_labels/
│   ├── cropped_plates/
│   └── ocr_labels/
├── models/
│   ├── detector.py
│   └── ocr.py
├── scripts/
│   ├── crop_from_detections.py
│   └── inference.py
├── inference/
│   └── main.py
├── config.yaml
├── requirements.txt
└── README.md
```

---

## 🔥 Key Takeaways
- Detection = bounding boxes only  
- OCR = text only  
- Cropping = simple script (NOT a model)  
- Good data > complex models

---

## 🚀 Execution Plan

**Phase 1**: Data Collection & Annotation  
**Phase 2**: Train Detection Model  
**Phase 3**: Create OCR Dataset (auto-crop)  
**Phase 4**: Train OCR Model  
**Phase 5**: Full Pipeline Integration  
**Phase 6**: Optimization & Real-time Testing

---

## 📊 Future Scope
- Real-time CCTV deployment
- Edge device (Jetson/Raspberry Pi)
- Web API + Dashboard
- Traffic violation integration

---

## 📌 Conclusion

This is a **complete production-ready ML system**, not just a model.

> “Good data beats complex models.”

---

## 🤝 Contribution
- Follow annotation guidelines strictly
- Keep consistency across the team
- Report unclear images
