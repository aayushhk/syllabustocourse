import streamlit as st
import asyncio
from backend import ai,web
from openai import BaseModel, OpenAI
client=OpenAI(api_key="Osk-5_hm4_IUIUCJDVZQ_1zCm8kaurMRPcD9Iso3-2yAGAT3BlbkFJYcex7sktCKiblB5sngBFI1SWdXqoH1L6EiaTITECwA")
import time




from duckduckgo_search import AsyncDDGS, DDGS

st.set_page_config("Study Material",layout="wide",initial_sidebar_state="expanded",page_icon="💡")


s=st.container(border=True)
r=st.empty()


        



course_content_response="WELCOME"
explainers="welcome"


system_prompt="""

You are an online course professor specializing in the given topics and subtopic. Today is the last day of preparation before the final exam. Your task is to provide a comprehensive review that covers all the essential topics and concepts from the given topic, chapter. Your responses should be clear, concise, and high-quality, ensuring that no important topics are missed. Provide study material, key points, and any tips or tricks that will help students excel in their exam.

Instructions:

Do not provide headings
enclose any maths for latex katex formula in '${formula}$'
Summarize Key Concepts: Provide a brief summary of each topic, highlighting the most important points.
Important Formulas/Theorems: List any crucial formulas, theorems, or principles that students need to remember.
Examples: Provide one example for each formula/theorem
Common Mistakes: Point out common mistakes students should avoid.
Practice Questions: Include a few practice questions or problems for each topic to help students test their understanding.
Study Tips: Offer any additional study tips or strategies that could help students during their last-minute revision.



"""

async def course_content(course_name, current_topic, current_subtopic):
    
    index= await ai(f"{system_prompt}. Topic: {current_subtopic} chapter: {current_subtopic} in {current_topic}, subject: {course_name}")
    #videos= await web({current_topic},{current_subtopic})
    
    return index
async def current_video(current_topic, current_subtopic):
    videos = DDGS().videos(f"{current_topic} {current_subtopic}", max_results=4)
    print(videos)
    print("================================================")
    
    return videos



if 'toc_content' in st.session_state:
    
    r.info("✨Select a topic to get started")
    with st.sidebar:
        st.title("📃 INDEX")

    # Iterate over the TOC entries and display them
    for toc_entry in st.session_state['toc_content']:
        unit_title = toc_entry.unit_title  # First element of the first tuple (list containing unit title)
        
        subtopics = toc_entry.subtopics  # Second element of the tuple (list of subtopics)
        
       
        # Create expanders for each unit title and corresponding buttons for each subtopic
        
        with st.sidebar.expander(unit_title):
            
            for subtopic in subtopics:
               #selection=st.button(subtopic, on_click=lambda subtopic=subtopic: st.session_state.update({'current_topic': unit_title, 'current_subtopic': subtopic}))#
                selection=st.button(subtopic,key=f"{unit_title}_{subtopic}",use_container_width=True)
                if selection:
                    st.session_state.update({'current_topic': unit_title, 'current_subtopic': subtopic})
                    s.header(f"{st.session_state.current_topic}")
                    s.success(f" {st.session_state.current_subtopic}") 
                    notes,revision,videos=r.tabs(["📒 Notes","🗒️ Quick revision","🎥 Videos"])
                    
                    st.toast('📒 Generating Notes')
                    time.sleep(20)

                    course_content_response = asyncio.run(course_content(st.session_state.course_name,st.session_state.current_topic, st.session_state.current_subtopic))
                    notes.subheader("📒 Notes")
                    notes.write(course_content_response)
                    st.toast('✅ Study material updated successfully')
                    time.sleep(.5)
                    st.toast('🗒️ Summerizing content for quick revision')
                    time.sleep(.5)
                    
                    explainers=asyncio.run(ai(f"Summerize the given content in 10 points for quick revision. Do not output anything else. Output a list without heading{course_content_response}" ))
                    revision.subheader("🗒️ Quick revision")
    
                    revision.markdown(explainers)
                    st.toast('✅ Quick revision updated successfully')
                    time.sleep(.5)
                    vids=asyncio.run(current_video(st.session_state.current_topic, st.session_state.current_subtopic))
                    st.toast('🎥 Searching for videos')
                    time.sleep(.5)
                    videos.subheader("🎥 Videos")
                    

                    
                    st.toast('✅ Videos updated successfully')
                    time.sleep(.5)
                
                    for vid in vids:

                        v4=videos.container(border=True)
                        v1,v2=v4.columns([1,1],vertical_alignment="top") 
                        v1.video(vid['content'])
                        v2.subheader(vid['title'])
                        v2.info(f"By {vid['uploader']}")
                        v2.write(vid['description'])
                                

                   
    
    
       
    #st.divider()
    
    
    
    #st.divider()
    
    #st.divider()
    


   
        
else:
    st.error("Please Upload your syllabus first")

