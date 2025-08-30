import streamlit as st
from StatBlock import *
from Display import *
from data_loader import *
from data_filter import *

def load_powers():
    return load_powers_from_xml('Powers_1.3.xml')
    
def load_origins():
    return load_origins_from_xml('Origins.xml')

def initialize_session_state(powers,origins):
    # Initialize character data in session state if not already present
    if "character" not in st.session_state:
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
            "avatar": None,
            "selected_rank":None,
            "add_power":False,
        }

    if "powerList" not in st.session_state:
        st.session_state.powerList = powers

    if "originList" not in st.session_state:
        st.session_state.originList = origins

def input_character_info():

    # Input fields for character name and rank selection
    st.session_state.character["name"] = st.text_input("Enter Character Name")    

    # Selectbox with dedicated session key
    st.session_state.character["rank"] = st.selectbox(
                                                    "Select Rank",
                                                    list(Rank),
                                                    format_func=lambda x: f"{x.name.title()} (Rank {x.value})",
                                                    key="selected_rank"
                                                    )

    
    
def allocate_stats():

    AdjustStatBlock(st, 
                    st.session_state.character["rank"].value,
                    st.session_state.character["abilityStats"]
                    )
    

    st.session_state.character["characterStats"] = calcStatBlocks(st, 
                                                                  st.session_state.character["rank"].value,
                                                                  st.session_state.character["abilityStats"],
                                                                  st.session_state.character["powers"]
                                                                  )
    

    


def add_powers(st):
    selected_powerSet = st.selectbox("Choose Power Set", options=getUniquePowerSets(st.session_state.powerList))
    #st.info(selected_powerSet)
    powerSetPowers = findPowersInPowerSet(st.session_state.powerList,selected_powerSet)

    availablePowers = findAvailablePowers(st,
                                          powerSetPowers,
                                          st.session_state.character["powers"],
                                          st.session_state.character["tags"],
                                          st.session_state.character["rank"].value
                                          )
    
    selected_power_name = st.selectbox("Choose Powers", options=availablePowers)
    
    selected_power = next(
        (power for power in st.session_state.powerList if power["name"].strip() == selected_power_name.split(":")[0].strip()),
         None
        )
       
    if selected_power:
        #st.info(selected_power)
        DisplayTabularInfo(st,selected_power)
#        
    #if "requires" not in selected_power_name.lower():
        #if st.button("Add Power - click twice"):
            #if selected_power not in st.session_state.character["powers"]:
                #st.session_state.character["powers"].append(selected_power) 
                        
        if "requires" not in selected_power_name.lower():
            pressed = st.button("Add Power")
            if pressed:
                if selected_power not in st.session_state.character["powers"]:
                    st.session_state.character["powers"].append(selected_power)     
                else:
                    print("remove button")
                    

def add_origins(st):
    
    origin_names = [origin["name"] for origin in st.session_state.originList]
    #st.info(origin_names)
    selected_origin_name = st.selectbox("Choose Origin", options=sorted(name.strip() for name in origin_names))   
    selected_origin = next(
        (origin for origin in st.session_state.originList if origin["name"].strip() == selected_origin_name),
         None
        )
    if selected_origin:
        DisplayTabularInfo(st,selected_origin)
    


def upload_avatar():
    # File uploader for avatar image and display preview
    pass

def display_character_summary():
    # Show assembled character info: name, rank, stats, powers, traits, avatar
    # Highlight validation errors if any
    pass

def export_character():
    # Option to export character data to JSON, PDF, or other formats
    pass

def main():
    powers = load_powers()
    origins = load_origins()

    initialize_session_state(powers,origins)
    
    st.title("Marvel Multiverse TTRPG Character Creator")

    characterTab, Origin_TraitTab,powerTab = st.tabs(["Character Sheet", "Origin/Traits","Powers List"])

    with characterTab:
        st.header("Character Sheet")
        st.button("Refresh", key='characterRefresh')
        # ... character info, stats, etc.

        input_character_info()

        if st.session_state.character["rank"]:
            allocate_stats()
            display_powers(st)
            display_stats(st)

    with Origin_TraitTab:
        st.header("Select an Origin Power")        
        # ... your entire power selection UI here ...
        add_origins(st)

    with powerTab:
        st.header("Select a Power")
        st.button("Refresh", key='powerRefresh')
        # ... your entire power selection UI here ...
        add_powers(st)
    
    
    
    upload_avatar()
    
    display_character_summary()
    
    export_character()

if __name__ == "__main__":
    main()