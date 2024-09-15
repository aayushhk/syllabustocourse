import streamlit as st
import PyPDF2
from io import StringIO
import asyncio
from streamlit_extras.bottom_container import bottom
import json
from pydantic import BaseModel
from backend import ai
#from pages.result import generate_study_material
from openai import OpenAI


client=OpenAI(api_key="sk-5_hm4_IUIUCJDVZQ_1zCm8kaurMRPcD9Iso3-2yAGAT3BlbkFJYcex7sktCKiblB5sngBFI1SWdXqoH1L6EiaTITECwA")

st.set_page_config("Study Material",layout="wide",initial_sidebar_state="collapsed",page_icon="📚")
with bottom():
        footer=st.container(border=True)
        footer.write("🎯App by <b> <a href='https://www.linkedin.com/in/aayush-kumar-pandey/'>Aayush Kumar</a></b>",unsafe_allow_html=True)

# Function to extract text from PDF using PyPDF2
async def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

class toc_format(BaseModel):
    unit_title:str
    subtopics: list[str]

class toc_full(BaseModel):
     course_content: list[toc_format]


async def toc(text):
        completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an helpful assistance"},
            {"role": "user", "content": f"Extract unit's titles and subtopics from given syllabus {text}"},
            ],response_format=(toc_full))
                   
        index = completion.choices[0].message.parsed.course_content
        return index



# Streamlit app
async def main():
        
        col1,coll2=st.columns([1,1],gap="medium")
        col2=coll2.container(border=True)
        with col1:
             st.title("Last day prepararation just got easier!")  
             st.image("logo.png")
             
             
             st.write("<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>",unsafe_allow_html=True)
        with col2:
            st.subheader("⏳ Exam Tomorrow?")
            st.write("Just upload the PDF of your syllabus and see it all coming together in a course. ")
            
            # File uploader
            course_name = st.text_input("Please enter your course name")
            if course_name not in st.session_state:
                st.session_state['course_name'] = course_name
            uploaded_file = st.file_uploader("Upload your syllabus PDF", type=["pdf"])
            if uploaded_file not in st.session_state:
                st.session_state['uploaded_file'] = uploaded_file
            start=st.button("Get Study Materials")
            # Generate study material button
            
            if course_name and uploaded_file and start :
                # Extract text from PDF
                text = await extract_text_from_pdf(uploaded_file)
                
                if text:
                    st.subheader("Extracted Text:")
                    st.text_area("Text extracted from PDF:", text, height=300)
                    
                toc_content=await toc(text)

                if 'toc_content' not in st.session_state:
                    st.session_state['toc_content'] = toc_content
                    
                    
                
            
                
                st.switch_page("pages/result.py")
                st.balloons()
            
            
         
            
                    



if __name__ == "__main__":
    asyncio.run(main())
