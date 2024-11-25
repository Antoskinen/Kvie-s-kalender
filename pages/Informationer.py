import streamlit as st
from docx import Document

def main():
    st.title("Informationer omkring ankomst/afgang")
    
    # File path
    file_path = "pages/Kvie Sø ankomst Vinter 2025.docx"

    # File download button
    st.download_button(
        label="Klik her og download guiden som fil for at se billederne",
        data=open(file_path, "rb").read(),
        file_name="Kvie Sø ankomst Vinter 2025.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    
    # Display file content (optional, requires the `python-docx` library)
    st.subheader("Dokumentets tekst:")
    try:
        from docx import Document
        document = Document(file_path)
        for paragraph in document.paragraphs:
            st.write(paragraph.text)
    except ImportError:
        st.warning("Install python-docx to display the document content.")

if __name__ == "__main__":
    main()
