import streamlit as st
from PIL import Image

def main():

        testtab, avaatarTab = st.tabs(["Test","Avatar"])

        with testtab:
             st.header("Test Sheet")

        with avaatarTab:        
            st.header("Character Sheet")

            print("here")

            if "avatar_file" not in st.session_state:
                st.session_state.avatar_file = None

            if st.button("Upload Avatar"):                    
                uploaded_ava_file = st.file_uploader("Choose an avatar to upload", key="uploaded_avatar_file")
                if uploaded_ava_file is not None:
                    st.session_state.avatar_file = uploaded_ava_file   
            
            if "avatar_file" not in st.session_state:
                st.session_state.avatar_file = None

            print(st.session_state.avatar_file)
            if st.session_state.avatar_file is not None:
                print("oops")
                image = Image.open(st.session_state.avatar_file)
                st.image(image)       

if __name__ == "__main__":
    main()