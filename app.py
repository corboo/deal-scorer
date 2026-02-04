"""
Enterprise Deal Scorer
Score and evaluate partnership opportunities
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Deal Scorer",
    page_icon="🎯",
    layout="centered"
)

# Scoring weights and values
SCORING = {
    "product_fit": {
        "weight": 20,
        "options": {"Low": 0, "Medium": 10, "High": 20}
    },
    "technical_effort": {
        "weight": 15,
        "options": {"Low": 15, "Medium": 8, "High": 0}
    },
    "timeline_alignment": {
        "weight": 15,
        "options": {"Aligns": 15, "Sort of Aligned": 8, "Does NOT Align": 0}
    },
    "engineering_lift": {
        "weight": 10,
        "options": {"Light": 10, "Medium": 5, "Heavy": 0}
    },
    "cross_team": {
        "weight": 5,
        "options": {"Light": 5, "Medium": 3, "Heavy": 0}
    },
    "commercial_potential": {
        "weight": 20,
        "options": {"High": 20, "Medium": 12, "Low": 5, "Too Early to Tell": 0}
    },
    "strategic_value": {
        "weight": 10,
        "options": {"High": 10, "Moderate": 6, "Neutral": 0}
    },
    "support_load": {
        "weight": 5,
        "options": {"Low": 5, "Medium": 3, "High": 0}
    }
}

def get_recommendation(score: int) -> tuple[str, str, str]:
    """Return recommendation, color, and description based on score"""
    if score >= 70:
        return "🟢 GO", "green", "Strong fit — pursue actively"
    elif score >= 50:
        return "🟡 EXPLORE", "orange", "Worth discussing — needs alignment"
    elif score >= 30:
        return "🟠 PAUSE", "red", "Significant concerns — park for now"
    else:
        return "🔴 PASS", "darkred", "Not a fit — politely decline"

def calculate_score(selections: dict) -> int:
    """Calculate total score from selections"""
    total = 0
    for key, value in selections.items():
        if key in SCORING and value in SCORING[key]["options"]:
            total += SCORING[key]["options"][value]
    return total

def save_to_sheets(data: dict):
    """Save submission to Google Sheets"""
    try:
        # Load credentials from Streamlit secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet_id = st.secrets.get("google_sheet_id", "1FKJdH8fQzfOph-Ws4DwEHQ1nLhhBPvtp7EF6U2ba3mE")
        sheet = client.open_by_key(sheet_id)
        
        # Try to get or create the "Scored Deals" worksheet
        try:
            worksheet = sheet.worksheet("Scored Deals")
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Scored Deals", rows=1000, cols=20)
            # Add headers
            headers = [
                "Timestamp", "Submitted By", "Company/Deal Name", "Meeting Number",
                "Purpose of Meeting", "What They Want", "What We Get", "Product Fit", 
                "Technical Effort", "Timeline Alignment", "Engineering Lift", 
                "Cross-Team Involvement", "Commercial Potential", "Strategic Value", 
                "Support Load", "Score", "Recommendation", "Notes"
            ]
            worksheet.append_row(headers)
        
        # Append the data
        row = [
            data["timestamp"],
            data["submitted_by"],
            data["company_name"],
            data["meeting_number"],
            data["purpose"],
            data["what_they_want"],
            data["what_we_get"],
            data["product_fit"],
            data["technical_effort"],
            data["timeline_alignment"],
            data["engineering_lift"],
            data["cross_team"],
            data["commercial_potential"],
            data["strategic_value"],
            data["support_load"],
            data["score"],
            data["recommendation"],
            data["notes"]
        ]
        worksheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Failed to save to Google Sheets: {str(e)}")
        return False

# Main UI
st.title("🎯 Enterprise Deal Scorer")
st.markdown("*Evaluate partnership opportunities with consistent criteria*")
st.markdown("---")

# Basic Info
st.subheader("📋 Basic Information")
col1, col2 = st.columns(2)
with col1:
    submitted_by = st.text_input("Your Name *")
with col2:
    company_name = st.text_input("Company / Deal Name *")

meeting_number = st.selectbox(
    "This is meeting number ___ with this company",
    options=["1st", "2nd", "3rd", "4th", "5th", "6th+"],
    index=0
)

purpose = st.text_area(
    "Purpose of the Meeting",
    placeholder="What was the meeting about?",
    height=80
)

col1, col2 = st.columns(2)
with col1:
    what_they_want = st.text_area(
        "What They Want From Us",
        placeholder="Their needs and expectations...",
        height=100
    )
with col2:
    what_we_get = st.text_area(
        "What We Would Get Out of It",
        placeholder="Benefits for IPAI...",
        height=100
    )

st.markdown("---")

# Scoring Criteria
st.subheader("📊 Scoring Criteria")

col1, col2 = st.columns(2)

with col1:
    product_fit = st.select_slider(
        "Product Fit",
        options=["Low", "Medium", "High"],
        value="Medium",
        help="How well does this align with our product capabilities?"
    )
    
    technical_effort = st.select_slider(
        "Technical Effort Required",
        options=["Low", "Medium", "High"],
        value="Medium",
        help="How much technical work would this require?"
    )
    
    timeline_alignment = st.selectbox(
        "Timeline & Roadmap Alignment",
        options=["Aligns", "Sort of Aligned", "Does NOT Align"],
        help="Does this fit our current roadmap and timeline?"
    )
    
    engineering_lift = st.select_slider(
        "Engineering Lift",
        options=["Light", "Medium", "Heavy"],
        value="Medium",
        help="How much engineering resources needed?"
    )

with col2:
    cross_team = st.select_slider(
        "Cross-Team Involvement",
        options=["Light", "Medium", "Heavy"],
        value="Medium",
        help="How many teams need to be involved?"
    )
    
    commercial_potential = st.selectbox(
        "Commercial Potential",
        options=["High", "Medium", "Low", "Too Early to Tell"],
        help="Revenue/growth opportunity"
    )
    
    strategic_value = st.selectbox(
        "Strategic Value",
        options=["High", "Moderate", "Neutral"],
        help="Brand, market positioning, future opportunities"
    )
    
    support_load = st.select_slider(
        "Ongoing Support Load",
        options=["Low", "Medium", "High"],
        value="Medium",
        help="Expected ongoing support requirements"
    )

notes = st.text_area(
    "Additional Notes",
    placeholder="Any other context or considerations...",
    height=80
)

st.markdown("---")

# Calculate and display score
selections = {
    "product_fit": product_fit,
    "technical_effort": technical_effort,
    "timeline_alignment": timeline_alignment,
    "engineering_lift": engineering_lift,
    "cross_team": cross_team,
    "commercial_potential": commercial_potential,
    "strategic_value": strategic_value,
    "support_load": support_load
}

score = calculate_score(selections)
recommendation, color, description = get_recommendation(score)

# Score display
st.subheader("🎯 Score")
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.metric("Total Score", f"{score}/100")

with col2:
    st.markdown(f"### {recommendation}")

with col3:
    st.markdown(f"*{description}*")

# Score breakdown (expandable)
with st.expander("📈 Score Breakdown"):
    for key, config in SCORING.items():
        value = selections[key]
        points = config["options"].get(value, 0)
        label = key.replace("_", " ").title()
        st.write(f"**{label}:** {value} → +{points} pts")

st.markdown("---")

# Submit button
can_submit = submitted_by and company_name

if st.button("💾 Save Assessment", type="primary", disabled=not can_submit, use_container_width=True):
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "submitted_by": submitted_by,
        "company_name": company_name,
        "meeting_number": meeting_number,
        "purpose": purpose,
        "what_they_want": what_they_want,
        "what_we_get": what_we_get,
        "product_fit": product_fit,
        "technical_effort": technical_effort,
        "timeline_alignment": timeline_alignment,
        "engineering_lift": engineering_lift,
        "cross_team": cross_team,
        "commercial_potential": commercial_potential,
        "strategic_value": strategic_value,
        "support_load": support_load,
        "score": score,
        "recommendation": recommendation,
        "notes": notes
    }
    
    if save_to_sheets(data):
        st.success(f"✅ Saved! **{company_name}** scored **{score}/100** — {recommendation}")
        st.balloons()
    else:
        st.warning("Assessment calculated but couldn't save to Google Sheets. Check secrets config.")

if not can_submit:
    st.caption("*Fill in your name and company/deal name to save*")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "Inception Point AI — Deal Scoring Tool"
    "</div>",
    unsafe_allow_html=True
)
