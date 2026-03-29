import streamlit as st
import plotly.express as px
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Foster to Adopt Hub", layout="wide", initial_sidebar_state="expanded")

st.title("👨‍👩‍👧 Foster to Adopt Hub")
st.markdown("**Simple official links for foster care adoption • Public system focus • Low or no cost paths**")
st.caption(f"Updated {datetime.now().strftime('%B %Y')} – FY2024 AFCARS data")

# Load state data
try:
    with open("state_data.json", "r") as f:
        state_data = json.load(f)
except FileNotFoundError:
    st.error("Please create the state_data.json file first.")
    st.stop()

# National stats (FY2024)
st.sidebar.markdown("### National Snapshot (FY2024)")
st.sidebar.info("""**70,418 children** waiting for adoption in foster care.

**46,935** adopted from foster care that year.

Many are sibling groups, older youth, or have special needs.""")
st.sidebar.markdown("[🔗 Official AFCARS Dashboard](https://tableau-public.acf.gov/views/afcars_dashboard_main_page/mainpage)")

# Search
search_query = st.text_input("🔍 Search across states (e.g., 'siblings', 'older youth', 'county', 'low cost')", "")

# US Map – color scale completely removed
states_list = sorted(state_data.keys())
fig = px.choropleth(
    locations=states_list,
    locationmode="USA-states",
    color=[1] * len(states_list),
    scope="usa",
    title="U.S. Map (Visual Reference Only)"
)
fig.update_layout(
    height=400, 
    margin={"r":0,"t":40,"l":0,"b":0},
    coloraxis_showscale=False   # <-- This line removes the color scale
)
st.plotly_chart(fig, use_container_width=True)

st.info("👆 The map is for visual reference only. **Please use the dropdown below** to select a state.")

# State selector
selected_state = st.selectbox("Select a state to view foster-to-adopt information", ["Select a state..."] + states_list)

if selected_state != "Select a state...":
    data = state_data.get(selected_state, {})
    
    st.subheader(f"📍 {selected_state} – Foster to Adopt Information")
    
    tab1, tab2, tab3 = st.tabs(["Public Foster-to-Adopt", "Waiting Children", "Private / Infant Options"])
    
    with tab1:
        st.markdown("**Foster-to-Adopt (Public System)** – Usually low or no cost. Many families start as foster parents.")
        if data.get("county_administered", False):
            st.warning("⚠️ This state is county-administered – processes can vary by county.")
        st.write(data.get("public_processes", "Contact your local county child welfare office or state agency to begin. Home study and training are required."))
        st.markdown(f"[🔗 Official {selected_state} Child Welfare / Adoption Agency]({data.get('state_agency', 'https://www.childwelfare.gov')})")
        if data.get("county_finder"):
            st.markdown(f"[🏠 Find Your County Office]({data.get('county_finder')})")
        st.info("**Typical next steps**: Attend orientation → Complete home study & training → Get approved → Match with waiting children.")
    
    with tab2:
        st.markdown("**Waiting Children in Foster Care**")
        st.markdown(f"[🔍 AdoptUSKids National Search – Filter by {selected_state}](https://adoptuskids.org/meet-the-children/search-for-children/search)")
        st.markdown(f"[📸 State Photolists & Additional Resources]({data.get('photolist_link', 'https://adoptuskids.org/meet-the-children/search-for-children/state-photolists')})")
        st.write(data.get("waiting_notes", "Not every waiting child is photolisted online. Register on AdoptUSKids (free) after your home study is approved."))
    
    with tab3:
        st.markdown("**Private Agency or Infant Adoption** (for comparison)")
        st.write(data.get("private_processes", "Private agencies often focus on newborns/infants and have variable fees. A home study is still required."))
        st.markdown("[National Council For Adoption – Agency Directory](https://adoptioncouncil.org/directory/)")
        st.markdown(f"[🔗 More {selected_state} Private Resources]({data.get('private_link', '#')})")
    
    # PDF Download
    if st.button("📄 Download My State Summary PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, f"Foster to Adopt Summary – {selected_state}")
        c.drawString(100, height - 140, f"Generated: {datetime.now().strftime('%B %d, %Y')}")
        y = height - 200
        lines = [
            "Public/Foster-to-Adopt: " + data.get("public_processes", "")[:220],
            "Waiting Children Link: " + data.get("photolist_link", ""),
            "Note: Always verify current details on official state websites."
        ]
        for line in lines:
            c.drawString(100, y, line)
            y -= 40
        c.save()
        buffer.seek(0)
        st.download_button("Click here to Download PDF", buffer, f"{selected_state}_foster_to_adopt_summary.pdf", "application/pdf")

else:
    st.info("Select a state above to see foster-to-adopt processes, waiting children resources, and next steps.")
    st.markdown("### Quick National Starting Points")
    st.markdown("- [AdoptUSKids – Search Waiting Children](https://adoptuskids.org/meet-the-children/search-for-children/search)")
    st.markdown("- [Child Welfare Information Gateway](https://www.childwelfare.gov/topics/adoption/)")

st.sidebar.header("Tips for Prospective Families")
st.sidebar.info("Many successful adoptions begin with fostering first.\nStart with your county or state agency for low-cost paths.\nA completed home study is required for most options.")

st.sidebar.caption("Mobile-friendly: Open this app on your phone → Share → 'Add to Home Screen' for quick access.")
{
  "Alabama": {
    "state_agency": "https://dhr.alabama.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact your local county Department of Human Resources office or the state adoption unit. Home study and training required for foster-to-adopt.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search and filter by Alabama. Not all waiting children are photolisted."
  },
  "Alaska": {
    "state_agency": "https://dhss.alaska.gov/ocs/Pages/adoption/default.aspx",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "State-administered system. Contact the Office of Children's Services for foster-to-adopt information and home study.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Alaska."
  },
  "Arizona": {
    "state_agency": "https://dcs.az.gov/foster",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Child Safety for foster care and adoption. Home study required.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Arizona has additional heart gallery resources in some areas."
  },
  "Arkansas": {
    "state_agency": "https://humanservices.arkansas.gov/divisions-shared-services/children-family-services/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Division of Children and Family Services for foster-to-adopt pathways.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Arkansas waiting children."
  },
  "California": {
    "state_agency": "https://www.cdss.ca.gov/adoption",
    "county_administered": true,
    "county_finder": "https://www.cdss.ca.gov/county-offices",
    "public_processes": "County-administered system. Contact your local county child welfare office. Home study required. Priority often given to relatives and current foster parents.",
    "private_processes": "Search licensed private agencies through state resources.",
    "private_link": "https://www.cdss.ca.gov/adoption",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Large foster care system with many sibling groups and older youth. Some counties have local photolists."
  },
  "Colorado": {
    "state_agency": "https://cdhs.colorado.gov/adoption",
    "county_administered": true,
    "county_finder": "https://cdhs.colorado.gov/counties",
    "public_processes": "County-administered. Contact your county human services department for foster-to-adopt information.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Colorado."
  },
  "Connecticut": {
    "state_agency": "https://portal.ct.gov/dcf",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children and Families for foster care and adoption services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Connecticut has heart gallery resources."
  },
  "Delaware": {
    "state_agency": "https://kids.delaware.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Services for Children, Youth and Their Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Delaware waiting children."
  },
  "District of Columbia": {
    "state_agency": "https://cfsa.dc.gov/service/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Child and Family Services Agency (CFSA) for foster-to-adopt options in DC.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by District of Columbia."
  },
  "Florida": {
    "state_agency": "https://www.myflfamilies.com/services/child-family/foster-care-adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children and Families or your local community-based care lead agency.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Florida has a large foster care system with many waiting children."
  },
  "Georgia": {
    "state_agency": "https://dfcs.georgia.gov/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Division of Family & Children Services for foster-to-adopt information.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Georgia waiting children."
  },
  "Hawaii": {
    "state_agency": "https://dhs.hawaii.gov/ssd/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Human Services for adoption services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Hawaii."
  },
  "Idaho": {
    "state_agency": "https://healthandwelfare.idaho.gov/services-programs/children-and-families/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Health and Welfare.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Idaho waiting children."
  },
  "Illinois": {
    "state_agency": "https://www.dcfs.illinois.gov/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children and Family Services for foster-to-adopt.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Illinois has a significant number of waiting children."
  },
  "Indiana": {
    "state_agency": "https://www.in.gov/dcs/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Child Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Indiana."
  },
  "Iowa": {
    "state_agency": "https://dhs.iowa.gov/services/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Iowa waiting children."
  },
  "Kansas": {
    "state_agency": "https://www.dcf.ks.gov/Services/Pages/Adoption.aspx",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department for Children and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Kansas."
  },
  "Kentucky": {
    "state_agency": "https://www.chfs.ky.gov/agencies/dcbs/dpp/Pages/default.aspx",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department for Community Based Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Kentucky waiting children."
  },
  "Louisiana": {
    "state_agency": "https://www.dcfs.louisiana.gov/page/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children and Family Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Louisiana."
  },
  "Maine": {
    "state_agency": "https://www.maine.gov/dhhs/ocfs/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Office of Child and Family Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Maine waiting children."
  },
  "Maryland": {
    "state_agency": "https://dhs.maryland.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Human Services or your local department.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Maryland."
  },
  "Massachusetts": {
    "state_agency": "https://www.mass.gov/info-details/adoption-in-massachusetts",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Massachusetts waiting children."
  },
  "Michigan": {
    "state_agency": "https://www.michigan.gov/mdhhs/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Health and Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Michigan."
  },
  "Minnesota": {
    "state_agency": "https://mn.gov/dhs/people-we-serve/children-and-families/adoption/",
    "county_administered": true,
    "county_finder": "https://mn.gov/dhs/people-we-serve/children-and-families/services/child-protection/contact-us/",
    "public_processes": "County-administered system. Contact your local county human services office for foster-to-adopt.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Minnesota waiting children."
  },
  "Mississippi": {
    "state_agency": "https://www.mdhs.ms.gov/families-and-children/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Mississippi."
  },
  "Missouri": {
    "state_agency": "https://dss.mo.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Social Services / Children's Division.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Missouri waiting children."
  },
  "Montana": {
    "state_agency": "https://dphhs.mt.gov/cfsd/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Public Health and Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Montana."
  },
  "Nebraska": {
    "state_agency": "https://dhhs.ne.gov/Pages/Adoption.aspx",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Health and Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Nebraska waiting children."
  },
  "Nevada": {
    "state_agency": "https://dcfs.nv.gov/Programs/CWS/Adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Hybrid system – contact your county or the Division of Child and Family Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Nevada."
  },
  "New Hampshire": {
    "state_agency": "https://www.dhhs.nh.gov/programs-services/children/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Health and Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search New Hampshire waiting children."
  },
  "New Jersey": {
    "state_agency": "https://www.nj.gov/dcf/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by New Jersey."
  },
  "New Mexico": {
    "state_agency": "https://cyfd.nm.gov/childrens-and-family-services/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Children, Youth and Families Department.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search New Mexico waiting children."
  },
  "New York": {
    "state_agency": "https://ocfs.ny.gov/programs/adoption/",
    "county_administered": true,
    "county_finder": "https://ocfs.ny.gov/main/localoffices/",
    "public_processes": "County-administered system. Contact your local county Department of Social Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "New York has county-specific resources in addition to AdoptUSKids."
  },
  "North Carolina": {
    "state_agency": "https://www.ncdhhs.gov/divisions/child-and-family-well-being/adoption",
    "county_administered": true,
    "county_finder": "https://www.ncdhhs.gov/divisions/child-and-family-well-being/county-dss-directory",
    "public_processes": "County-administered. Contact your local county Department of Social Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by North Carolina."
  },
  "North Dakota": {
    "state_agency": "https://www.nd.gov/dhs/services/child-family/adoption/",
    "county_administered": true,
    "county_finder": "https://www.nd.gov/dhs/locations/county-social-services/",
    "public_processes": "County-administered system. Contact your local county social services office.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search North Dakota waiting children."
  },
  "Ohio": {
    "state_agency": "https://fosterandadopt.dcy.ohio.gov/",
    "county_administered": true,
    "county_finder": "https://fosterandadopt.dcy.ohio.gov/county-offices",
    "public_processes": "County-administered. Contact your local county children services agency.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Ohio has dedicated adoption profiles and photolists."
  },
  "Oklahoma": {
    "state_agency": "https://oklahoma.gov/okdhs/services/adoption.html",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Oklahoma."
  },
  "Oregon": {
    "state_agency": "https://www.oregon.gov/dhs/CHILDREN/ADOPTION/Pages/index.aspx",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Human Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Oregon waiting children."
  },
  "Pennsylvania": {
    "state_agency": "https://www.dhs.pa.gov/Children/Adoption/Pages/default.aspx",
    "county_administered": true,
    "county_finder": "https://www.dhs.pa.gov/Children/Adoption/Pages/County-Adoption-Offices.aspx",
    "public_processes": "County-administered system. Contact your local county children and youth agency.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Pennsylvania."
  },
  "Rhode Island": {
    "state_agency": "https://dcyf.ri.gov/adoption.php",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children, Youth and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Rhode Island waiting children."
  },
  "South Carolina": {
    "state_agency": "https://dss.sc.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Social Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by South Carolina."
  },
  "South Dakota": {
    "state_agency": "https://dss.sd.gov/cfs/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Social Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search South Dakota waiting children."
  },
  "Tennessee": {
    "state_agency": "https://www.tn.gov/dcs/adoption.html",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children's Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Tennessee."
  },
  "Texas": {
    "state_agency": "https://www.dfps.texas.gov/Adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Family and Protective Services. Some regions have additional local resources.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://www.dfps.texas.gov/Adoption/",
    "photolist_link": "https://www.dfps.texas.gov/application/tare/search.aspx/children",
    "waiting_notes": "Texas maintains its own searchable waiting children database in addition to AdoptUSKids."
  },
  "Utah": {
    "state_agency": "https://dcfs.utah.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Division of Child and Family Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Utah waiting children."
  },
  "Vermont": {
    "state_agency": "https://dcf.vermont.gov/foster-adopt",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department for Children and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Vermont."
  },
  "Virginia": {
    "state_agency": "https://www.dss.virginia.gov/family/adoption/",
    "county_administered": true,
    "county_finder": "https://www.dss.virginia.gov/localagency/",
    "public_processes": "County-administered system. Contact your local Department of Social Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Virginia waiting children."
  },
  "Washington": {
    "state_agency": "https://www.dcyf.wa.gov/services/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Children, Youth, and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Washington."
  },
  "West Virginia": {
    "state_agency": "https://dhhr.wv.gov/bcf/Pages/default.aspx",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Bureau for Children and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search West Virginia waiting children."
  },
  "Wisconsin": {
    "state_agency": "https://dcf.wisconsin.gov/adoption",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Hybrid system – contact your county or the Department of Children and Families.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids national search filtered by Wisconsin."
  },
  "Wyoming": {
    "state_agency": "https://dfs.wyo.gov/adoption/",
    "county_administered": false,
    "county_finder": "",
    "public_processes": "Contact the Department of Family Services.",
    "private_processes": "Search licensed private agencies or attorneys. Home study still required.",
    "private_link": "https://adoptioncouncil.org/directory/",
    "photolist_link": "https://adoptuskids.org/meet-the-children/search-for-children/search",
    "waiting_notes": "Use AdoptUSKids to search Wyoming waiting children."
  }
}

