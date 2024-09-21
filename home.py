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

client=OpenAI(api_key=st.secrets["openai_apikey"])


st.set_page_config("Study Material",layout="wide",initial_sidebar_state="collapsed",page_icon="📚")
hide_streamlit_style = ("""
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>

""")

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
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
            {"role": "user", "content": f"Extract unit's titles and subtopics from given syllabus {text}. Make sure no topics or subtopics are repreated"},
            ],response_format=(toc_full))
                   
        index = completion.choices[0].message.parsed.course_content
        return index



# Streamlit app
async def main():
        st.title("Last day prepararation just got easier!") 
        col2=st.container(border=True)
        
        with col2:
            st.subheader("⏳ Exam Today?")
            st.write("Just upload the PDF of your syllabus and see it all coming together in a course. ")
            
            
            # File uploader
            course_name="///Course Name///"
            course_name = st.text_input("Please enter the subject name")
            if course_name not in st.session_state:
                st.session_state['course_name'] = course_name
            uploaded_file = st.file_uploader("Upload your syllabus PDF", type=["pdf"])
            if uploaded_file not in st.session_state:
                st.session_state['uploaded_file'] = uploaded_file
            syllabus=""
            text=""
            syllabus=st.text_area("Paste your syllabus here / Add more topics to your PDF syllabus",placeholder="ctrl+V your syllabus here")
            start=st.button("Get Study Materials")
            # Generate study material button
            
            if start :
                # Extract text from PDF
                if uploaded_file:
                    text = await extract_text_from_pdf(uploaded_file)
                text+=syllabus
                
                if text:
                    st.toast("⚡ Fetching syllabus...")
                    st.code(text)
                    st.toast("🧐 Planning it out...")   
                    toc_content=await toc(text)

                    if 'toc_content' not in st.session_state:
                        st.session_state['toc_content'] = toc_content
                    st.toast("✨ Taking you to the course...")
                    st.switch_page("pages/result.py")
                
                else:
                     st.error("No syllabus provided. Failed to fetch syllabus")

                
            
            
         
            
                    



if __name__ == "__main__":
    asyncio.run(main())
