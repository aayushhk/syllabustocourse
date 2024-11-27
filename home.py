import streamlit as st
import PyPDF2
from io import StringIO
import asyncio
import json
from pydantic import BaseModel
from backend import ai
#from pages.result import generate_study_material
from openai import OpenAI

client=OpenAI(api_key=st.secrets["openai_apikey"])


st.set_page_config("Course Generator",layout="wide",initial_sidebar_state="collapsed",page_icon="📚")
hide_streamlit_style = ("""
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>

""")


st.markdown(hide_streamlit_style, unsafe_allow_html=True)
       

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
        st.title("Generate full course") 
        col2=st.container(border=True)
        
        with col2:
            st.subheader("⏳ Dont have time to chatGPT everything? Just enter the job tile, or a syllabus, or simply type something..")
            st.write("Just upload the PDF of your syllabus and see it all coming together in a course. ")
            tab1, tab2 = st.tabs(["For Job seekers", "For students"])
            with tab1:
                st.subheader("Enter Your job title here...")
                job_title = st.text_input("What position you are studying for",placeholder="Data Scientist")
                st.session_state['job_title'] = job_title
                get_table=st.button("Get Table of Content")
            if get_table:
                st.session_state['get_table'] = get_table
                system_prompt='''1. Take real jobs from indeed and linkedin for reference
                2. List tools and frameworks to learn
                3. Provide a Table of content.
                4.  Do not explain anything. Just the table of content.NO introduction, no conclusion  '''
                
                x=await ai(f"user: Give me a relevant syllabus of 2024 to get an high paying {job_title} jobs? system:{system_prompt}")
            else:
                 x=""   
                

            # File uploader
            with tab2:
                course_name="///Course Name///"
                course_name = st.text_input("Please enter the subject name")
                if course_name not in st.session_state:
                    st.session_state['course_name'] = course_name
                uploaded_file = st.file_uploader("Upload your syllabus PDF", type=["pdf"])
                if uploaded_file not in st.session_state:
                    st.session_state['uploaded_file'] = uploaded_file
           
            text=""
            if x : 
                text+=x
            if uploaded_file:
                    
                    pdf_content = await extract_text_from_pdf(uploaded_file)
                    text+=pdf_content
                    
            
            if text:
                if 'text' not in st.session_state:
                    st.session_state['text'] = text
            
                st.code(text)  
                st.toast("⚡ Fetching syllabus...")
                st.toast("🧐 Planning it out...")   
                toc_content=await toc(text)

                if 'toc_content' not in st.session_state:
                    st.session_state['toc_content'] = toc_content
                st.toast("✨ Taking you to the course...")
                st.switch_page("pages/result.py")
            
            else:
                st.info("No syllabus provided.")

                
            
            
         
            
                    



if __name__ == "__main__":
    asyncio.run(main())
