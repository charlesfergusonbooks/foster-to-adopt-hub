import streamlit as st
import plotly.express as px
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Foster to Adopt Hub", layout="wide", initial_sidebar_state="expanded")

# Mobile-friendly CSS
st.markdown("""
<style>
    .main .block-container { padding: 1rem; }
    h1 { font-size: 1.9rem !important; }
    .stButton>button { width: 100%; height: 3rem; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

st.title("👨‍👩‍👧 Foster to Adopt Hub")
st.markdown("**Simple official links for foster care adoption • Public system focus • Low or no cost paths**")
st.caption(f"Updated {datetime.now().strftime('%B %Y')} – FY2024 AFCARS data")

# Load JSON
with open("state_data.json", "r") as f:
    state_data = json.load(f)

# Rest of the app (same as the mobile-improved version)
st.sidebar.markdown("### National Snapshot (FY2024)")
st.sidebar.info("""**70,418 children** waiting for adoption in foster care.

**46,935** adopted from foster care that year.

Many are sibling groups, older youth, or have special needs.""")
st.sidebar.markdown("[🔗 AFCARS Dashboard](https://tableau-public.acf.gov/views/afcars_dashboard_main_page/mainpage)")

search_query = st.text_input("🔍 Search across states (e.g., 'siblings', 'older youth', 'county')", "")

states_list = sorted(state_data.keys())
fig = px.choropleth(
    locations=states_list,
    locationmode="USA-states",
    color=[1] * len(states_list),
    scope="usa",
    title="U.S. Map (Visual Reference Only)"
)
fig.update_layout(height=320, margin={"r":0,"t":40,"l":0,"b":0}, coloraxis_showscale=False)
st.plotly_chart(fig, use_container_width=True)

st.info("👆 The map is visual only. Use the dropdown below to select a state.")

selected_state = st.selectbox("Select a state", ["Select a state..."] + states_list)

if selected_state != "Select a state...":
    data = state_data.get(selected_state, {})
    st.subheader(f"📍 {selected_state}")
    tab1, tab2, tab3 = st.tabs(["🏠 Public Foster-to-Adopt", "👦 Waiting Children", "🤝 Private Options"])
    
    with tab1:
        st.markdown("**Public Foster-to-Adopt** – Usually low or no cost.")
        if data.get("county_administered", False):
            st.warning("⚠️ **County-administered**: Processes vary by county.")
        st.write(data.get("public_processes", ""))
        st.markdown(f"[🔗 Official Agency]({data.get('state_agency')})")
        if data.get("county_finder"):
            st.markdown(f"[🏠 Find County Offices]({data.get('county_finder')})")
    
    with tab2:
        st.markdown("**Waiting Children**")
        st.markdown(f"[🔍 AdoptUSKids – Filter {selected_state}](https://adoptuskids.org/meet-the-children/search-for-children/search)")
        st.markdown(f"[📸 State Photolists]({data.get('photolist_link', 'https://adoptuskids.org/meet-the-children/search-for-children/state-photolists')})")
        st.write(data.get("waiting_notes", ""))
    
    with tab3:
        st.markdown("**Private / Infant Options**")
        st.write(data.get("private_processes", ""))
        st.markdown("[Agency Directory](https://adoptioncouncil.org/directory/)")
    
    if st.button("📄 Download PDF Summary", use_container_width=True):
        # PDF code (shortened)
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 700, f"Foster to Adopt Summary – {selected_state}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, f"{selected_state}_summary.pdf", "application/pdf", use_container_width=True)

else:
    st.info("Select a state above.")

st.sidebar.caption("Add to Home Screen on your phone for app-like experience.")
