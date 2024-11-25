import streamlit as st
from docx import Document

# Function to display the content of the Word file
def display_word_file(file_path):
    document = Document(file_path)
    for paragraph in document.paragraphs:
        st.write(paragraph.text)

# Streamlit app
def main():
    st.title("Word File Viewer")
    
    # Upload Word file
    uploaded_file = st.file_uploader("Upload a Word file (.docx)", type=["docx"])
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        display_word_file(uploaded_file)
    else:
        st.info("Please upload a .docx file to view its content.")

if __name__ == "__main__":
    main()
