# MongoDB Schema Design: InsightPoint Platform

This document describes the schema design, field constraints, collections, and lifecycle states utilized in the MongoDB database of the **InsightPoint AI News Intelligence Platform**.

---

## 1. Collection Overview
The application utilizes three main MongoDB collections within the `news_sentiment_intelligence_db` database:

1. **`users`**: Contains registered user credentials, profile settings, roles, and session audit logs.
2. **`news_dataset`**: Contains real-time and ingested multi-lingual news articles from RSS feeds and historical sources, complete with full NLP enrichment outputs.
3. **`documents`**: Contains user-uploaded multi-format files (PDF, DOCX, TXT) and pasted text snippets with step-by-step pipeline metric traces.

---

## 2. Detailed Schemas

### A. `users` Collection
Stores user profiles and UI preferences.

```json
{
  "_id": "ObjectId",
  "username": "String (unique)",
  "email": "String (unique, indexed)",
  "password_hash": "String (bcrypt hash)",
  "role": "String ('user' | 'admin')",
  "created_at": "ISODate",
  "last_login": "ISODate | null",
  "is_active": "Boolean",
  "settings": {
    "theme": "String ('light' | 'dark')",
    "language": "String (e.g., 'en', 'hi', 'zh')",
    "notifications": "Boolean"
  }
}
```

### B. `news_dataset` (Articles) Collection
Stores fully enriched articles gathered by the scraping and ingestion pipelines. Contains translated fields, geocoded locations, and vector embeddings for semantic search.

```json
{
  "_id": "ObjectId",
  "title": "String",
  "translated_title": "String | null",
  "original_url": "String (indexed, unique)",
  "source": "String (e.g., 'BBC News', 'BBC Hindi')",
  "published_date": "ISODate",
  "summary": "String",
  "translated_summary": "String | null",
  "image_url": "String | null",
  "language": "String (two-letter code, e.g., 'hi', 'zh', 'en')",
  "country": "String | null",
  "continent": "String | null",
  "category": "String (e.g., 'disaster', 'terrorism', 'infrastructure', 'sports')",
  "inferred_category": "String",
  "category_confidence": "Double (0.0 to 1.0)",
  "inferred_categories": "Array [String]",
  "created_at": "ISODate",
  "processed_at": "ISODate | null",
  "analyzed": "Boolean",
  "status": "String ('pending' | 'fully_analyzed' | 'failed')",
  "retry_count": "Int",
  "last_error": "String | null",
  "keywords": "Array [String]",
  "locations": "Array [Object]",
  "embedding": "Array [Double] (dimension 1024, for semantic search)"
}
```

### C. `documents` (Uploads) Collection
Stores documents uploaded manually by the user or text pasted for direct evaluation. Contains performance metrics for tracing execution time through the NLP DAG executor.

```json
{
  "_id": "ObjectId",
  "user_id": "String (references users._id)",
  "filename": "String | null",
  "file_path": "String | null",
  "file_type": "String (e.g., '.pdf', '.docx', '.txt' or null)",
  "source": "String ('file' | 'pasted_text')",
  "raw_text": "String",
  "clean_text": "String | null",
  "language": "String | null",
  "translated_text": "String | null",
  "translated_to_en": "Boolean",
  "translation_engine": "String | null",
  "sentiment": {
    "label": "String ('positive' | 'negative' | 'neutral')",
    "confidence": "Double",
    "method": "String ('RoBERTa' | 'VADER' | 'TextBlob')",
    "scores": {
      "positive": "Double",
      "negative": "Double",
      "neutral": "Double"
    }
  },
  "category": "String | null",
  "category_confidence": "Double | null",
  "event_type": "String | null",
  "event_confidence": "Double | null",
  "keywords": "Array [String]",
  "locations": "Array [Object]",
  "processed": "Boolean",
  "processing_time": "Double (seconds)",
  "pipeline_metrics": {
    "preprocessing_time": "Double",
    "translation_time": "Double",
    "sentiment_time": "Double",
    "event_detection_time": "Double",
    "ner_time": "Double"
  },
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

---

## 3. Database Indexes
To maintain sub-millisecond query performance on large datasets, the following indexes are applied:

1. `users.email` -> Unique Index (for quick login/lookup).
2. `news_dataset.original_url` -> Unique Index (prevents duplicating articles during RSS scrape updates).
3. `news_dataset.status` -> Single Field Index (for scheduling worker queries).
4. `news_dataset.category` -> Single Field Index (for rapid category search).
5. `documents.user_id` -> Single Field Index (for user profile document lists).
