# Digital Maturity Score Logic

The Digital Score is a deterministic aggregation of agent metrics, not an LLM hallucination.

## Scoring Formula Breakdown (Max 100 Points)

### 1. Website (20 Points)
- `ssl_enabled == true`: +5
- `mobile_responsive == true`: +5
- `load_time_ms < 3000`: +5 (0 if > 5000)
- `broken_links == 0`: +5

### 2. SEO (15 Points)
- `meta_title_present == true`: +3
- `h1_present == true`: +3
- `sitemap_present == true`: +4
- `local_schema_present == true`: +5

### 3. Contact & AI Support (10 Points)
- `contact_form_present == true`: +3
- `online_booking_present == true`: +4
- `chat_widget_present == true`: +3

### Classification
- **0–30: Offline Business**. Critical need for basic website and Google Maps profile.
- **31–50: Basic Digital Presence**. Needs SEO and Social Media push.
- **51–75: Growing Business**. Needs automation (Booking/Chatbots).
- **76–90: Advanced Business**. Optimization and CRM phase.
- **91–100: Digitally Mature**. Ready for advanced AI integrations.
