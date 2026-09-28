import streamlit as st
import requests

st.set_page_config(page_title="AgriSetu AI - Code for Communities", layout="wide", page_icon="🌾")

st.title("🌾 AgriSetu AI: Interoperable Digital Agriculture Network")
st.caption("Build with AI: Code for Communities Hackathon — Agricultural Intelligence Track")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Gemini Multimodal Crop Diagnostic")
    uploaded_file = st.file_uploader("Upload leaf/crop photo", type=["jpg", "png", "jpeg"])
    
    state = st.selectbox("Select State", ["Telangana", "Punjab", "Maharashtra", "Karnataka", "Uttar Pradesh", "Bihar"])
    language = st.selectbox("Select Preferred Language", ["Hindi", "Telugu", "Tamil", "Marathi", "Bengali", "English"])
    soil_ph = st.slider("Soil pH Level", 4.0, 9.0, 6.5)

    if uploaded_file is not None and st.button("Analyze & Get Advisory"):
        with st.spinner("Gemini AI is analyzing crop health and soil metrics..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"language": language, "state": state, "soil_ph": soil_ph}
            
            try:
                res = requests.post("http://127.0.0.1:8000/api/v1/diagnose-crop", files=files, data=data)
                if res.status_code == 200:
                    result = res.json()
                    st.success("Diagnosis Complete!")
                    st.markdown(result["advisory"])
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

with col2:
    st.subheader("🗣️ Vernacular Agro-Voice Advisory Engine")
    voice_query = st.text_area("Ask a question (e.g., 'When is the best time to sow paddy this season?')")
    
    if st.button("Submit Voice/Text Query"):
        if voice_query:
            with st.spinner("Generating advisory..."):
                data = {"user_query": voice_query, "language": language, "state": state}
                try:
                    res = requests.post("http://127.0.0.1:8000/api/v1/voice-advisory", data=data)
                    if res.status_code == 200:
                        st.info(res.json()["response"])
                    else:
                        st.error("Error generating response.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

st.divider()
st.caption("Built with Gemini 2.0 API, FastAPI, Streamlit | Scalable Digital Public Infrastructure for India")
