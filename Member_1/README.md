# 📝 Member 1: AI Product Assistant Microservice

## 📌 Microservice Overview
[cite_start]This microservice automates the generation of text-based marketing and optimization assets for the e-commerce catalog. [cite_start]By passing simple garment descriptions, it programmatically creates professional titles, rich item summaries, SEO target strings, and platform indexing tags[cite: 26, 27, 28, 29].

### Core Responsibilities
* [cite_start]**Product Title Generation:** Forms clean, optimized titles for marketplace interfaces[cite: 26].
* [cite_start]**Product Description Generation:** Creates rich, engaging promotional text copies[cite: 27].
* [cite_start]**SEO & Tag Analytics Extractor:** Structures metadata indexes to improve catalog search metrics[cite: 28, 29].

---

## 🏗️ System Architecture & Data Flow
[cite_start]The microservice sits at the start of the Team 1 pipeline[cite: 134]:

[Garment Metadata Input] ──> [Member 1: FastAPI Gateway]
│
├──> [NLP Template Processing] ──> Title & Description ├──> [SEO Ingestion Matrix] ────> Keyword Generator 
└──> [Pandas Logger Engine] ────> Append to CSV Metrics  
---

## 🌐 API Specifications & Integration Mapping

### Generate Product Metadata
* **Endpoint:** `POST /generate-metadata/`
* **Content-Type:** `application/json`

#### Expected Success Response (`200 OK`)
```json
{
  "status": "Success",
  "timestamp": "2026-06-11 12:05:14",
  "generated_title": "Essential Crimson red Hoodie for Men",
  "generated_description": "Step up your personal fashion collection with this masterfully designed crimson red hoodie...",
  "seo_keywords": "buy crimson red hoodie, high-quality hoodie...",
  "product_tags": ["hoodie", "crimson red", "men", "fashion-ai"]
}
