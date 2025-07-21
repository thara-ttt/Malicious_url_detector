import streamlit as st
import requests

st.set_page_config(page_title="Malicious URL Detector", page_icon="🔗", layout="centered")
st.title("🔗 Malicious URL Detector")
st.markdown("""
Enter a URL below to check if it is **benign** or **malicious**. This tool uses a machine learning model trained on real-world data.
""")

url = st.text_input("Enter a URL to check:", placeholder="https://example.com")

if st.button("Check URL"):
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Analyzing URL..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/predict",
                    json={"url": url},
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    if result["prediction"] == "benign":
                        st.success(f"✅ The URL is likely benign.")
                    else:
                        st.error(f"⚠️ The URL is likely malicious!")
                    st.markdown(f"**Prediction:** `{result['prediction']}`")
                else:
                    st.error(f"Server error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

st.markdown("---")
st.caption("Made with Streamlit & Flask | 2025")
