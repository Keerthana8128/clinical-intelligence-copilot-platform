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

st.info("Day 10: PDF upload validation and document metadata.")

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


st.subheader("Upload Health Document")

uploaded_file = st.file_uploader(
    "Upload a sample healthcare PDF document",
    type=["pdf"]
)

if "chunks_filename" not in st.session_state:
    st.session_state.chunks_filename = None

if uploaded_file is not None:
    st.write(f"Selected file: **{uploaded_file.name}**")

    if st.button("Upload PDF to Backend"):
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{BACKEND_URL}/documents/upload",
                files=files,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                if data["status"] == "success":
                    st.session_state.chunks_filename = data["chunks_filename"]

                    st.success(data["message"])

                    st.write(f"**Filename:** {data['filename']}")
                    st.write(f"**File Size:** {data['file_size_kb']} KB")
                    st.write(f"**Page Count:** {data['page_count']}")
                    st.write(f"**Saved PDF Path:** {data['saved_path']}")
                    st.write(f"**Extracted Text Path:** {data['processed_text_path']}")
                    st.write(f"**Chunks Path:** {data['chunks_path']}")
                    st.write(f"**Chunks Filename:** {data['chunks_filename']}")
                    st.write(f"**Character Count:** {data['character_count']}")
                    st.write(f"**Chunk Count:** {data['chunk_count']}")

                    st.subheader("Extracted Text Preview")
                    st.text_area(
                        "First 1000 characters from the PDF",
                        data["text_preview"],
                        height=250
                    )

                    st.subheader("Preview Chunks")

                    for chunk in data["preview_chunks"]:
                        with st.expander(f"Chunk {chunk['chunk_id']}"):
                            st.write(f"Character Count: {chunk['character_count']}")
                            st.write(chunk["text"])

                else:
                    st.error(data["message"])
            else:
                st.error(f"Backend returned status code: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Make sure FastAPI is running on port 8000.")

        except requests.exceptions.Timeout:
            st.error("Upload request timed out. Please try again.")

        except Exception as error:
            st.error(f"Unexpected error: {error}")


st.subheader("Search Uploaded Document Chunks")

search_query = st.text_input(
    "Enter a keyword or short question for chunk search",
    placeholder="Example: diabetes medication, blood pressure, follow up"
)

top_k = st.number_input(
    "Number of chunks to return",
    min_value=1,
    max_value=10,
    value=3
)

if st.button("Search Chunks"):
    if not st.session_state.chunks_filename:
        st.error("Please upload a PDF first before searching.")
    elif not search_query.strip():
        st.error("Please enter a search query.")
    else:
        try:
            params = {
                "chunks_filename": st.session_state.chunks_filename,
                "query": search_query,
                "top_k": top_k
            }

            response = requests.get(
                f"{BACKEND_URL}/documents/search",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                if data["status"] == "success":
                    st.success(data["message"])
                    st.write(f"**Query:** {data['query']}")
                    st.write(f"**Result Count:** {data['result_count']}")

                    if data["result_count"] == 0:
                        st.warning("No matching chunks found.")
                    else:
                        for result in data["results"]:
                            with st.expander(
                                f"Chunk {result['chunk_id']} | Score: {result['score']}"
                            ):
                                st.write(f"Character Count: {result['character_count']}")
                                st.write(result["text"])

                else:
                    st.error(data["message"])
            else:
                st.error(f"Backend returned status code: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Make sure FastAPI is running on port 8000.")

        except requests.exceptions.Timeout:
            st.error("Search request timed out. Please try again.")

        except Exception as error:
            st.error(f"Unexpected error: {error}")


st.subheader("Ask a Question About the Uploaded Document")

question = st.text_input(
    "Ask a basic question",
    placeholder="Example: What medications are mentioned?"
)

if st.button("Generate Basic Answer"):
    if not st.session_state.chunks_filename:
        st.error("Please upload a PDF first before asking a question.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        try:
            params = {
                "chunks_filename": st.session_state.chunks_filename,
                "query": question,
                "top_k": 3
            }

            response = requests.get(
                f"{BACKEND_URL}/documents/ask",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                if data["status"] == "success":
                    st.success(data["message"])

                    st.write(f"**Question:** {data['query']}")
                    st.write(f"**Confidence:** {data['confidence']}")

                    st.subheader("Structured Answer")
                    st.write(data["answer"])

                    st.subheader("Why this answer was selected")
                    st.info(data["reason"])

                    st.subheader("Source Chunks")
                    if not data["source_chunks"]:
                        st.warning("No source chunks found.")
                    else:
                        for source in data["source_chunks"]:
                            with st.expander(
                                f"Source Chunk {source['chunk_id']} | Score: {source['score']}"
                            ):
                                st.write(source["text"])
                            st.subheader("Suggested Questions to Ask a Doctor")
                            for question_item in data["suggested_questions"]:
                                st.write(f"- {question_item}")    

                    st.warning(data["safety_note"])

                else:
                    st.error(data["message"])
            else:
                st.error(f"Backend returned status code: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Make sure FastAPI is running on port 8000.")

        except requests.exceptions.Timeout:
            st.error("Answer request timed out. Please try again.")

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