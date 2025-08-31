import pickle
import streamlit as st
import os

def save_session_state(st):
    if st.session_state.character['name']:
        fileName = (st.session_state.character['name']).strip() + ".pkl"
        with open(fileName, 'wb') as f:
            pickle.dump(dict(st.session_state), f)
            print ("saved")


def load_session_state(st):
       st.session_state.uploaded_file = st.file_uploader("Choose a saved session state file", type=["pkl"])

    
def checkForLoadFile(st):
    
    
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if st.session_state.uploaded_file is not None:
        print ("load start")
        loaded_state = pickle.load(st.session_state.uploaded_file)

        # Clear current session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Update with loaded state
        st.session_state.update(loaded_state)

        print ("loaded")