import streamlit as st
from StatBlock import *
from Display import *
from data_loader import *
from data_filter import *
from file import *

def load_powers():
    return load_powers_from_xml('Powers_1.3.xml')
    
def load_origins():
    return load_origins_from_xml('Origins.xml')

def load_tags():
    return load_tags_from_xml('Tags_1.0.0.xml')

def load_traits():
    return load_traits_from_xml('Traits_1.0.0.xml')

def load_occupations():
    return load_occupations_from_xml('Occupations_1.0.0.xml')

def initialize_session_state(powers,origins,tags,traits,occupations):
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
            "origin": [],
            "avatar": None,                     
        }

    if "powerList" not in st.session_state:
        st.session_state.powerList = powers

    if "originList" not in st.session_state:
        st.session_state.originList = origins

    if "tagList" not in st.session_state:
        st.session_state.tagList = tags

    if "traitList" not in st.session_state:
        st.session_state.traitList = traits

    if "occupationList" not in st.session_state:
        st.session_state.occupationList = occupations    

  
        

def input_character_info():

    # Input fields for character name and rank selection
    st.session_state.character["name"] = st.text_input("Enter Character Name", value=st.session_state.character["name"])    

    # Selectbox with dedicated session key
    if not st.session_state.character["rank"] is None:
        rankIndex = list(Rank).index(st.session_state.character["rank"])
    else:
        rankIndex = 0

    st.session_state.character["rank"] = st.selectbox(
                                                    "Select Rank",
                                                    list(Rank),
                                                    format_func=lambda x: f"{x.name.title()} (Rank {x.value})",
                                                    index = rankIndex
                                                    )

    
    
def allocate_stats():

    st.header(f"**Attributes**")


    AdjustStatBlock(st, 
                    st.session_state.character["rank"].value,
                    st.session_state.character["abilityStats"]
                    )
    

    st.session_state.character["characterStats"] = calcStatBlocks(st, 
                                                                  st.session_state.character["rank"].value,
                                                                  st.session_state.character["abilityStats"],
                                                                  st.session_state.character["powers"],
                                                                  st.session_state.character["traits"]
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
        DisplayTabularInfo(st,selected_power)
#                               
        if "requires" not in selected_power_name.lower():
            pressed = st.button("Add Power",key = selected_power['name'] + " Add")
            if pressed:
                if selected_power not in st.session_state.character["powers"]:
                    st.session_state.character["powers"].append(selected_power)     

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
    tags = load_tags()
    traits = load_traits()
    occupations = load_occupations()

    checkForLoadFile(st)

    initialize_session_state(powers,origins,tags,traits,occupations)
    
    st.title("Marvel Multiverse TTRPG Character Creator")

    InfoTab, characterTab ,statTab, Origin_TraitTab,powerTab = st.tabs(["How to use","Character Sheet", "Attributes","Origin/Occupation/Traits/Tags","Powers List"])

    with InfoTab:
        displayInfo(st)

    with characterTab:        
        st.header("Character Sheet")
        st.button("Refresh", key='characterRefresh')
               
        with st.expander("Save / Load"):

            cols = st.columns(3)
            with cols[0]:
                if st.button("Save"):
                    save_session_state(st)

            with cols[1]:
                if st.button("Load"):                    
                    load_session_state(st)
        
            with cols[2]:
                if st.button("Clear"):                    
                    clear_session_state(st)
        

        if st.session_state.character["rank"]:
            st.subheader("Name: " + st.session_state.character["name"])
            st.subheader(f"Rank:  {st.session_state.character["rank"].name.title()} (Rank {st.session_state.character["rank"].value})")
            
            with st.expander("Attributes"):
                display_abilities(st)
            with st.expander("Stats"):
                display_stats(st)
            with st.expander("Movement"):
                display_movement(st)    
            with st.expander("Powers"):
                display_powers(st)                        
            with st.expander("Origin"):
                display_origin(st)
            with st.expander("Occupation"):
                display_occupation(st)
            with st.expander("Traits"):
                display_traits(st)                                
            with st.expander("Tags"):
                display_tags(st)                                        

    with statTab:
        st.button("Refresh", key='statRefresh')
        input_character_info()
        allocate_stats()

    with Origin_TraitTab:        
        st.header("Select an Origin Power")        
        # ... your entire power selection UI here ...
        with st.expander("Origins"):
            add_origins(st)
        with st.expander("Occupations"):
            add_occupations(st)        
        with st.expander("Traits"):
            add_traits(st)
        with st.expander("Tags"):
            add_tags(st)        

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