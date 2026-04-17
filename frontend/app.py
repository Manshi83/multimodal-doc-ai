import streamlit as st
import requests

st.set_page_config(page_title="PDF Chatbot", layout="centered")

st.title("📄 PDF Chatbot")
st.write("Upload a PDF and ask questions about it.")

API_URL = "http://127.0.0.1:8000"

# ---------- Upload PDF ----------
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    if st.button("Process PDF"):
        with st.spinner("Processing PDF..."):
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
            }

            response = requests.post(
                f"{API_URL}/upload-pdf/",
                files=files
            )

            # ✅ SUCCESS
            if response.status_code == 200:
                data = response.json()
                st.success("✅ PDF processed successfully!")
                st.subheader("Summary:")
                st.write(data["summary"])
                st.session_state["ready"] = True

            # ❗ DEBUG ERROR HERE
            else:
                st.error("❌ Failed to process PDF")
                st.write("Status Code:", response.status_code)
                st.write("Error:", response.text)

# ---------- Chat Section ----------
if "ready" in st.session_state and st.session_state["ready"]:

    st.subheader("💬 Chat with your PDF")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask a question:")

    if st.button("Ask"):
        if user_input:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_URL}/chat/",
                    params={"query": user_input}
                )

                if response.status_code == 200:
                    answer = response.json()["answer"]

                    # Save chat
                    st.session_state.chat_history.append(
                        {"q": user_input, "a": answer}
                    )
                else:
                    st.error("❌ Chat failed")

    # Display chat history
    for chat in st.session_state.chat_history[::-1]:
        st.markdown(f"**You:** {chat['q']}")
        st.markdown(f"**Bot:** {chat['a']}")