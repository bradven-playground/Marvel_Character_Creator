import pickle
import streamlit as st
import os

def save_session_state(st):
    if st.session_state.character['name']:
        fileName = (st.session_state.character['name']).strip() + ".pkl"
        with open(fileName, 'wb') as f:
            pickle.dump(st.session_state['character'], f)
    
def load_session_state(st):
    uploaded_file = st.file_uploader("Choose a saved session state file", type=["pkl"],key="uploaded_file")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
    
    
def checkForLoadFile(st):
    
    
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    if st.session_state.uploaded_file is not None:

        st.session_state.character.clear()
        st.session_state.uploaded_file.seek(0)
        st.session_state['character']= pickle.load(st.session_state.uploaded_file)

        #reset to it doesn't keep checking
        st.session_state.uploaded_file = None
