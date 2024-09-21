import streamlit as st
import asyncio
from backend import ai,web
from openai import BaseModel, OpenAI
client=OpenAI(api_key=st.secrets["openai_apikey"])
import time
import os



from duckduckgo_search import AsyncDDGS, DDGS

st.set_page_config("Study Material",layout="wide",initial_sidebar_state="expanded",page_icon="💡")
hide_streamlit_style = ("""
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>

""")

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


s=st.container(border=True)
r=st.empty()



        



course_content_response="WELCOME"
explainers="welcome"


system_prompt="""

You are an online course professor specializing in the given topics and subtopic. Today is the last day of preparation before the final exam. Your task is to provide content type that covers all the essential topics and concepts from the given topic, chapter. Your responses should be clear, concise, and high-quality, ensuring that no important topics are missed. Explain like students are newbie who get 0 marks. 

Instructions:
1. Do NOT Provide headings. Instead provide subheadings with emojis
2. enclose any maths for latex katex formula in '${formula}$'. This is very important!
3. Generate a high quality material fot the given 'content type' for the given topic and subtopic:
4. Always return well-formated document with clean UI. Use tables where possible
5. Do not explain anything else other than the content type asked for
"""
summerize_key_concepts="Summarize Key Concepts: Provide a brief summary of each topic, highlighting the most important points."
formulas="Important Formulas/Theorems: List any crucial formulas, theorems, or principles that students need to remember in a table"
examples="Examples: Provide different example for each formula/theorem in a table, highlighting important ones"
mistakes="Common Mistakes: Point out 5 common mistakes students should avoid in table with Wrong and Right columns  "
practice_p="Practice Questions: Respond only with 5 common practice questions or problems for each topic with solutions"


async def course_content(course_name, current_topic, current_subtopic,content_type):
    
    index= await ai(f"{system_prompt} Content type: {content_type}. Topic: {current_subtopic} chapter: {current_subtopic} in {current_topic}, subject: {course_name}")
    #videos= await web({current_topic},{current_subtopic})
    
    return index

async def current_video(current_topic, current_subtopic):
    videos = DDGS().videos(f"{current_topic} {current_subtopic}", max_results=4)
    print(videos)
    print("================================================")
    
    return videos

async def current_diagram(current_topic, current_subtopic):
    diagrams = DDGS().images(f"{current_topic} {current_subtopic}", max_results=6)
    print(diagrams)
    print("================================================")
    
    return diagrams



if 'toc_content' in st.session_state:
    
    
    r.info("✨ Select a topic to get started...")
    

    with st.sidebar:
        st.subheader("📃 INDEX")

    # Iterate over the TOC entries and display them
    for toc_entry in st.session_state['toc_content']:
        unit_title = toc_entry.unit_title  # First element of the first tuple (list containing unit title)
        
        subtopics = toc_entry.subtopics  # Second element of the tuple (list of subtopics)
        
        
        # Create expanders for each unit title and corresponding buttons for each subtopic
        
        with st.sidebar.expander(unit_title):
            
            for subtopic in subtopics:
               #selection=st.button(subtopic, on_click=lambda subtopic=subtopic: st.session_state.update({'current_topic': unit_title, 'current_subtopic': subtopic}))#
                selection=st.button(subtopic.capitalize(),key=f"{unit_title}_{subtopic}",use_container_width=True)
                
                if selection:
                    st.session_state.update({'current_topic': unit_title, 'current_subtopic': subtopic})
                    s.caption(st.session_state.course_name.upper())
                    s.header(f"{st.session_state.current_topic}")
                    s.success(f" {st.session_state.current_subtopic.capitalize()}") 
                    notes,diagrams,revision,videos,problems_t=r.tabs(["📒 Notes","🖼️ Diagrams","🗒️ Quick revision","🎥 Videos","❓ Problems"])
                    problems=problems_t.container()
                    
                    
                    

                    notes.subheader("📒 Notes")
                    st.toast('📒 Generating Notes')
                    summary = asyncio.run(course_content(st.session_state.course_name,st.session_state.current_topic, st.session_state.current_subtopic,summerize_key_concepts))
                    notes.write(summary)
                    formula = asyncio.run(course_content(st.session_state.course_name,st.session_state.current_topic, st.session_state.current_subtopic,formulas))
                    notes.write(formula)
                    example = asyncio.run(course_content(st.session_state.course_name,st.session_state.current_topic, st.session_state.current_subtopic,examples))
                    notes.write(example)
                    mistake = asyncio.run(course_content(st.session_state.course_name,st.session_state.current_topic, st.session_state.current_subtopic,mistakes))
                    notes.write(mistake)
                    practice = asyncio.run(course_content(st.session_state.course_name,st.session_state.current_topic, st.session_state.current_subtopic,practice_p))
                    notes.write(practice)
                    
                    
                    
                    
                    
                    
                    
                    
                    diagrams.subheader("🖼️ Diagrams")
                    diags=asyncio.run(current_diagram(f"Scientific Diagrams of ", f"{st.session_state.current_subtopic} in {st.session_state.current_topic}" ))

                    st.toast('🖼️ Getting Diagrams')
                    time.sleep(.2)

                    for img in diags:
                        
                        img_c=diagrams.container(border=True)
                        img_c.image(img['image'],use_column_width=True,caption=img["title"])
                        
                    
                    
                    st.toast('✅ Study material updated')
                    
                    
                    if revision:
                        st.toast('🗒️ Summerizing content for quick revision')
                        time.sleep(.5)
                        explainers=asyncio.run(ai(f"Provide study materials of given topic of the given chapter in 10 points for quick revision. Do not output anything else. Output a list without heading topic: {st.session_state.current_subtopic}, Chapter: {st.session_state.current_topic}" ))
                        revision.subheader("🗒️ Quick revision")
                        revision.markdown(explainers)
                        st.toast('✅ Quick revision updated')
                        
                    
                    
                    
                    
                        st.toast('❓ Designing problems')
                        
                        problem=asyncio.run(ai(f"Generate two sections of questions - First, A list of 5 long-answer type questions. Second, 20 multiple-choice questions with 4 options next line from these given topics: -- {explainers} --. Instructions: Act like a strict phd professor who set tough question papers. Do not explain anything , NO HEADINGS. Make sure the questions cover each topic, theorem and formula. " ))      
                        problems.markdown(problem)
                        if problem not in st.session_state:
                            st.session_state['problem']=problem
                        solutions=problems.expander("View solutions",False)
                        solutions.error("👿 Solve the problems before viewing the solution")
                        
                        with solutions:
                            solution= asyncio.run(ai(f"Solve these problems.Return very short-answers for Long-answer problems. Return correct options for the mutiple-choise problems. Problems: {problem} "))
                            st.markdown(solution)
                

                    vids=asyncio.run(current_video(st.session_state.current_topic, st.session_state.current_subtopic))
                    st.toast('🎥 Searching for videos')
                   
                    videos.subheader("🎥 Videos")
                    

                    
                    
                    
                
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

