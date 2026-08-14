# Detailed Database Schema

SQLite is the primary datastore. We utilize BSON documents for flexible storage of agent outputs.

## Tables

### 1. `businesses`
Stores core immutable and contact data.
- `_id` (UUID, Primary Key)
- `name` (VARCHAR, Not Null)
- `phone` (VARCHAR)
- `email` (VARCHAR)
- `address` (VARCHAR)
- `category` (VARCHAR)
- `location` (GeoJSON Point)
- `created_at` (TIMESTAMP)

**Indexes**: 
- `2dsphere` index on `location` for fast nearby searches.
- Index on `category`.

### 2. `websites`
Stores website audit results.
- `_id` (UUID, Primary Key)
- `business_id` (UUID, Reference)
- `url` (VARCHAR)
- `status` (VARCHAR) - e.g., 'online', 'timeout', 'ssl_error'
- `metrics` (JSON) - Stores exact boolean/integer metrics from the Website Agent.
- `lighthouse_scores` (JSON)
- `last_audited` (TIMESTAMP)

**Indexes**:
- Index on `business_id`.
- Index on `metrics` fields as needed for fast querying (e.g., `{"metrics.ssl_enabled": 1}`).

### 3. `recommendations`
Stores the LLM-generated roadmap items.
- `_id` (UUID, Primary Key)
- `business_id` (UUID, Reference)
- `priority` (INT)
- `title` (VARCHAR)
- `description` (VARCHAR)
- `estimated_cost_usd` (DECIMAL)
- `expected_impact` (VARCHAR)
- `created_at` (TIMESTAMP)
