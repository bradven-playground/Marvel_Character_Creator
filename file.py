import pickle
import streamlit as st
import io
from StatBlock import *

def save_session_state(st):
    if st.session_state.character['name']:
        fileName = (st.session_state.character['name']).strip() + ".pkl"
        print("Avatar before saving")
        print(st.session_state.character["avatar"])
        print(st.session_state.character['abilityStats']['Melee'])
        #with open(fileName, 'wb') as f:
        buffer = io.BytesIO()
        pickle.dump(st.session_state['character'], buffer)
        buffer.seek(0)

        # Provide a download button for the user
        st.download_button(
            label="Download session state",
            data=buffer,
            file_name=fileName,
            mime="application/octet-stream"
        )

    
def load_session_state(st):

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    uploaded_file = st.file_uploader("Choose a Character to load", type=["pkl"],key="uploaded_save_file")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file        
    


    
def checkForLoadFile(st):
    
    
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
        
    if st.session_state.uploaded_file is not None:
        
        print("Reload!")
        #print(st.session_state.uploaded_file)
        st.session_state.character.clear()
        st.session_state.uploaded_file.seek(0)
        st.session_state['character']= pickle.load(st.session_state.uploaded_file)

        #reset so it doesn't keep checking
        st.session_state.uploaded_file = None

    

def UploadHeroPic(st):
    
    uploaded_ava_file = st.file_uploader("Choose an avatar to upload", key="uploaded_avatar_file")
    #if uploaded_ava_file is not None:
    st.session_state.character["avatar"]= uploaded_ava_file   

    
        