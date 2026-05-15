# import streamlit as st 
# from fetch_wikipedia import get_random_wiki_topic, get_wiki_topic_summary

# st.title('Speech Therapy')


# st.write('Welcome to the Speech Threrapy. This tool provides a fun way to help you improve your speaking skills.')
# st.write('A Random topic will be selected for you when you click on "Start" button.')
# st.write('Once the topic is selected of your choice you can click on "Next" button.')
# st.write('It will show the content to you about that topic which you can read for upto 2 mins and after that you will have to summarize the same topic in your words back to the agent which will help you identify gaps in your speaking skills.')



# random_topic = 'Random Topic'


# def update_session_step():
#     st.session_state.step += 1


# if "step" not in st.session_state:
#     st.session_state.step = 0



# if st.session_state.step == 0:
#     with st.container(border = 1,horizontal = True, vertical_alignment= 'center'):
#         with st.container(border = 1):
#             st.write('Click on Start Button to Select a Random Topic from Wikipedia')

#     if st.button(label = 'Start', on_click=update_session_step):
#         wiki_topic = get_random_wiki_topic()
#         st.write(wiki_topic)


# elif st.session_state.step == 1:
#     with st.container(border = 1,horizontal = True, vertical_alignment= 'center'):
#         with st.container(border = 1):
#             wiki_topic = get_random_wiki_topic()
#             st.write(wiki_topic)

#     if st.button(label = 'Rerun'):
#         st.rerun()



#     if st.button(label = 'Select Topic', icon_position='right', on_click = update_session_step):
#         extract = get_wiki_topic_summary(wiki_topic)
#         with st.container(border = 1, horizontal=True, vertical_alignment= 'center'):
#             st.header(wiki_topic)
#             st.write_stream(extract)


import streamlit as st
import time 
from datetime import datetime
import os 
from fetch_wikipedia import get_random_wiki_topic, get_wiki_topic_summary
from transcription import get_transcription
from llm_analyzer import get_analysis


st.title('Speech Therapy')

st.write('Welcome to Speech Therapy. This tool provides a fun way to help you improve your speaking skills.')
st.write('A Random topic will be selected for you when you click on the "Start" button.')
st.write('Once a topic of your choice is selected, you can click on the "Select Topic" button.')
st.write('It will show you content about that topic, which you can read for up to 2 mins. Afterward, you will summarize the same topic in your own words back to the agent, helping you identify gaps in your speaking skills.')


output_folder = "./audios/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# -----------------------------------------
# 1. INITIALIZE SESSION STATE
# -----------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "wiki_topic" not in st.session_state:
    st.session_state.wiki_topic = ""



# -----------------------------------------
# 2. DEFINE CALLBACK FUNCTIONS
# -----------------------------------------
def start_app():
    st.session_state.wiki_topic = get_random_wiki_topic()
    st.session_state.step = 1

def reroll_topic():
    st.session_state.wiki_topic = get_random_wiki_topic()

def move_to_summary():
    st.session_state.step = 2

def move_to_reading_mode():
    st.session_state.step = 3

def move_to_speaking_mode():
    st.session_state.step = 4

def move_to_analysis_mode():
    st.session_state.step = 5

# -----------------------------------------
# 3. UI RENDERING LOGIC (The State Machine)
# -----------------------------------------

# STEP 0: Start Screen
if st.session_state.step == 0:
    with st.container(border=1):
        st.write('Click on the Start Button to Select a Random Topic from Wikipedia')
    with st.container(horizontal=True):
        st.button(label='Start', on_click=start_app)


# STEP 1: Topic Selection
elif st.session_state.step == 1:
    with st.container(border=1):
        # We read from session_state so the topic doesn't change randomly on reruns!
        st.write(f"{st.session_state.wiki_topic}")

    with st.container(horizontal=True):
        st.button(label='Rerun (Get New Topic)', on_click=reroll_topic)
        st.button(label='Select Topic', icon_position='right', on_click=move_to_summary)


# STEP 2: Display Summary
elif st.session_state.step == 2:
    with st.container(border=1):
        st.header(st.session_state.wiki_topic)
        
        # Only fetch the summary once the user actually reaches Step 2
        paras = get_wiki_topic_summary(st.session_state.wiki_topic)
        
        # Assuming your get_wiki_topic_summary returns a generator (since you used write_stream)
        st.session_state.content = ""
        try:
            for para in paras:
                st.write(para)
                st.session_state.content =  st.session_state.content + para
        except TypeError:
            print("Something went Wrong. Please refresh the page and start again.")

        move_to_reading_mode()

        ph = st.empty()
        N = 2*60
        for secs in range(N,-1,-1):
            mm, ss = secs//60, secs%60
            ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        
        move_to_speaking_mode()
        st.rerun()


elif st.session_state.step == 4:
    with st.container(border=1):
        st.session_state.audio = st.audio_input(label= "Start Speaking about the topic in your own words for 2 min, do not press anything in between.", )

        if st.session_state.audio:
            

            # print(type(st.session_state.audio)) 

            # file_name = f"audio_file_{datetime.now().format('%Y_%m_%d_%h_%m_%s')}.wav"

            # output_path = os.path.join(output_folder, file_name)

            # with open(output_path, 'wb') as audio_file:
            #     audio_file.write(audio)

            
            st.session_state.transcript = get_transcription(st.session_state.audio, st.session_state.wiki_topic)


            st.session_state.analysis = get_analysis(st.session_state.content, st.session_state.transcript, st.session_state.wiki_topic) 

            st.button(label = "Next", on_click=move_to_analysis_mode)
            # print(st.session_state.analysis)

elif st.session_state.step == 5:
    with st.container(border=1):
        st.header(f"Topic: {st.session_state.wiki_topic}")
        col1, col2 = st.columns(2) 

        with col1:
            with st.container(border = True):
                st.subheader("Original Text")
                st.write(st.session_state.content)

        with col2:
            with st.container(border = True):
                st.subheader("Your Transcript")
                st.write(st.session_state.transcript)

        with st.container(border = 1, vertical_alignment= "bottom"):
            st.header("Analysis") 
            st.write(st.session_state.analysis)


    






 



