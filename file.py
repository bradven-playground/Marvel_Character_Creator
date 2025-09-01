import pickle
import streamlit as st
import io
from StatBlock import *

def save_session_state(st):
    if st.session_state.character['name']:
        fileName = (st.session_state.character['name']).strip() + ".pkl"
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
    uploaded_file = st.file_uploader("Choose a saved session state file", type=["pkl"],key="uploaded_file")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
    
def clear_session_state(st):
    if "character" in st.session_state:
        st.session_state.character = {
            "name": "",
            "rank": None,
            "abilityStats": {stat: 0 for stat in abilityBlock},          # e.g., {"Might": 0, "Agility": 0, ...}               
            "characterStats": {stat: 0 for stat in statBlock},          # e.g., {"Run Speed": 0, "Agility Dmg Multiplier": 0, ...}               
            "powers": [],
            "tags": [],
            "traits": [],
            "tags": [],
            "occupation": [],
            "origin": [],
            "avatar": None,                     
        }
    
def checkForLoadFile(st):
    
    
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    if st.session_state.uploaded_file is not None:

        st.session_state.character.clear()
        st.session_state.uploaded_file.seek(0)
        st.session_state['character']= pickle.load(st.session_state.uploaded_file)

        #reset to it doesn't keep checking
        st.session_state.uploaded_file = None
