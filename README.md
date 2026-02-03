# 🎯 Enterprise Deal Scorer

Score and evaluate partnership opportunities with consistent criteria.

## Features

- **Weighted scoring system** (0-100 scale)
- **Auto-recommendation**: Go / Explore / Pause / Pass
- **Google Sheets integration** for tracking
- **Score breakdown** for transparency

## Scoring Criteria

| Criteria | Weight | Best → Worst |
|----------|--------|--------------|
| Product Fit | 20% | High → Low |
| Technical Effort | 15% | Low → High |
| Timeline Alignment | 15% | Aligns → Does NOT |
| Engineering Lift | 10% | Light → Heavy |
| Cross-Team Involvement | 5% | Light → Heavy |
| Commercial Potential | 20% | High → Too Early |
| Strategic Value | 10% | High → Neutral |
| Ongoing Support Load | 5% | Low → High |

## Recommendations

- **🟢 GO** (70-100): Strong fit — pursue actively
- **🟡 EXPLORE** (50-69): Worth discussing — needs alignment
- **🟠 PAUSE** (30-49): Significant concerns — park for now
- **🔴 PASS** (0-29): Not a fit — politely decline

## Setup

### Streamlit Cloud Secrets

Add these secrets in Streamlit Cloud:

```toml
google_sheet_id = "YOUR_SHEET_ID"

[gcp_service_account]
type = "service_account"
project_id = "your-project"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

### Google Sheets Setup

1. Create a GCP service account with Sheets API access
2. Share your Google Sheet with the service account email
3. Add credentials to Streamlit secrets

## Local Development

```bash
# Create secrets file
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
# Edit with your credentials

# Run
streamlit run app.py
```

---
Built by Inception Point AI
