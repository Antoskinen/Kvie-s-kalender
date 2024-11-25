import streamlit as st
from docx import Document

def main():
    st.title("Document Viewer and Downloader")
    
    # File path
    file_path = "Kvie Sø ankomst Vinter 2025.docx"
    
    # Display file content (optional, requires the `python-docx` library)
    st.subheader("Document Content:")
    try:
        from docx import Document
        document = Document(file_path)
        for paragraph in document.paragraphs:
            st.write(paragraph.text)
    except ImportError:
        st.warning("Install python-docx to display the document content.")

    # File download button
    st.download_button(
        label="Download the Word Document",
        data=open(file_path, "rb").read(),
        file_name="Kvie Sø ankomst Vinter 2025.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

if __name__ == "__main__":
    main()
