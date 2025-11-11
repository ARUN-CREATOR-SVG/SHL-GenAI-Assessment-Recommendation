import os
import requests
import streamlit as st

BACKEND_URL_LOCAL = "http://127.0.0.1:8000"
BACKEND_URL_ONLINE = "https://shl-genai-assessment-recommendation.onrender.com"

st.set_page_config(
    page_title="SHL GenAI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🧠 SHL GenAI Assistant")
st.markdown("Ask me anything related to SHL assessments, products, or solutions!")

query = st.text_input("💬 Enter your query here:", placeholder="Content Writer required, expert in English and SEO.")

if st.button("Ask") and query.strip():
    with st.spinner("Fetching relevant info... ⏳"):
        try:
            response = requests.post(
                f"{BACKEND_URL_ONLINE}/recommend",
                json={"query": query},
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()

                if "recommended_assessments" in data:
                    assessments = data["recommended_assessments"]

                    if not assessments:
                        st.warning("No recommendations found for your query ")
                    else:
                        st.markdown("### 🧾 Recommended Assessments:")
                        for i, rec in enumerate(assessments, start=1):
                            name = rec.get("name", "Unnamed Assessment")
                            url = rec.get("url", "#")
                            desc = rec.get("description", "")
                            duration = rec.get("duration", "")
                            adaptive = rec.get("adaptive_support", "")
                            remote = rec.get("remote_support", "")
                            test_types = ", ".join(rec.get("test_type", []))

                            st.markdown(f"**{i}. [{name}]({url})**")
                            st.caption(desc)
                            st.markdown(f"-  Duration: {duration} mins")
                            st.markdown(f"-  Adaptive: {adaptive}")
                            st.markdown(f"-  Remote Support: {remote}")
                            st.markdown(f"-  Test Types: {test_types}")
                            st.markdown("---")


                else:
                    st.error(data.get("error", "Unexpected response from server."))
            else:
                st.error(f"Backend error: HTTP Status {response.status_code}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

else:
    st.markdown("> Type a question above and hit **Ask** ")
