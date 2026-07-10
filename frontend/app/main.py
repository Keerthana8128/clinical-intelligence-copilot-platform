import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Clinical Intelligence Copilot Platform",
    page_icon="🩺",
    layout="wide"
)

st.title("Clinical Intelligence Copilot Platform")

st.write(
    "A personal healthcare document understanding platform that helps users "
    "understand health-related documents in simple language."
)

st.info("Day 2: Frontend is now connected to the FastAPI backend.")

st.subheader("Backend Connection Test")

if st.button("Check Backend Status"):
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            st.success("Backend is connected successfully.")
            st.json(data)
        else:
            st.error(f"Backend returned status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend. Make sure FastAPI is running on port 8000.")

    except requests.exceptions.Timeout:
        st.error("Backend request timed out. Please try again.")

    except Exception as error:
        st.error(f"Unexpected error: {error}")


st.subheader("Project Information")

if st.button("Load Project Info"):
    try:
        response = requests.get(f"{BACKEND_URL}/project-info", timeout=5)

        if response.status_code == 200:
            data = response.json()

            st.write(f"**Project Name:** {data['project_name']}")
            st.write(f"**Project Type:** {data['project_type']}")
            st.write(f"**Purpose:** {data['purpose']}")
            st.warning(data["safety_note"])
        else:
            st.error(f"Backend returned status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend. Make sure FastAPI is running on port 8000.")

    except requests.exceptions.Timeout:
        st.error("Backend request timed out. Please try again.")

    except Exception as error:
        st.error(f"Unexpected error: {error}")