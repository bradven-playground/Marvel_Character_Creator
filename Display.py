import pandas as pd
from data_filter import *

def DisplayCharacterStats(st, rank, Ability,CalcStats):   

    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"#### Health: {CalcStats['Health']}")
        st.markdown(f"#### Focus: {CalcStats['Focus']}")
        st.markdown(f"#### Initative: {CalcStats['Initative Mod']}")

    with cols[1]:
        st.markdown(f"##### Health Dmg Reduction: {CalcStats['Health Dmg Reduction']}")
        st.markdown(f"##### Focus Dmg Reduction: {CalcStats['Focus Dmg Reduction']}")

    st.markdown("--------------------")

    df = pd.DataFrame({
        "##### Type": ["##### Melee", "##### Agility", "##### Resilience","##### Vigilance","##### Ego","##### Logic"],
        "##### Attack": [Ability['Melee'], Ability['Agility'], Ability['Resilience'], Ability['Vigilance'], Ability['Ego'], Ability['Logic']],        
        "##### Damage": [
                        "M x " + str(CalcStats['Melee Dmg Multiplier']+rank) + " + " + str(Ability['Melee']), 
                        "M x " + str(CalcStats['Agility Dmg Multiplier']+rank) + " + " + str(Ability['Agility']), 
                        "-", 
                        "-", 
                        "M x " + str(CalcStats['Ego Dmg Multiplier']+rank) + " + " + str(Ability['Ego']), 
                        "M x " + str(CalcStats['Logic Dmg Multiplier']+rank) + " + " + str(Ability['Logic']), 
                        ],
        "##### Defence": [CalcStats['Melee Defence Score'], CalcStats['Agility Defence Score'],CalcStats['Resilience Defence Score'],CalcStats['Vigilance Defence Score'],CalcStats['Ego Defence Score'],CalcStats['Logic Defence Score'],],                         
        "##### Out of Combat": [CalcStats['Melee Non-Combant Check'], CalcStats['Agility Non-Combant Check'],CalcStats['Resilience Non-Combant Check'],CalcStats['Vigilance Non-Combant Check'],CalcStats['Ego Non-Combant Check'],CalcStats['Logic Non-Combant Check'],],
                  
    })

    st.table(df)   
                
def DisplayMovmentStats(st, rank, Ability,CalcStats): 
    
    
    df = pd.DataFrame({
        "##### Momevement Type": ["##### Run Speed", "##### Jump Speed", "##### Flight Speed","##### Climb Speed","##### Swim Speed","##### Web Swing Speed","##### Glide Speed","##### Teleport Speed"],
        "##### In Combat": [CalcStats['Combat Run Speed'], CalcStats['Combat Jump Speed'],CalcStats['Combat Flight Speed'],CalcStats['Climb Speed'],CalcStats['Swim Speed'],CalcStats['Combat Web Swing Speed'],CalcStats['Combat Glide Speed'],CalcStats['Combat Teleport Speed']],            
        "##### Out of Combat": [CalcStats['Run Speed'], CalcStats['Jump Speed'],CalcStats['Flight Speed'],CalcStats['Climb Speed'],CalcStats['Swim Speed'],CalcStats['Web Swing Speed'],CalcStats['Glide Speed'],CalcStats['Teleport Speed']],                  
        })
    st.table(df) 
            

def DisplayTabularInfo(st,Info):

    if Info:        
        df = pd.DataFrame(list(Info.items()), columns=['Stat', 'Value'])
        st.dataframe(df)
        

def DisplayPowerInfo(st,powers):
    if powers:
        sorted_powers = sorted(powers, key=lambda p: p["name"].strip().lower())
        for power in sorted_powers:
            with st.expander(power["name"]):
                DisplayTabularInfo(st,power)
                #if it's not a prerequisit for another power, give the user the option to remove
                prereq = isPrerequisite(power,st.session_state.character["powers"])
                #print(prereq)
                if not prereq:
                    #print("isPrerequisite")
                    pressed = st.button("Remove Power",key = power['name'])
                    if pressed:
                        #print("pressed")
                        if power in st.session_state.character["powers"]:
                            st.session_state.character["powers"].remove(power)  
                else:
                    st.write("Power is a pre-requisite for another power and cannot be removed")


def display_powers(st):
    st.header(f"**Powers**")
    DisplayPowerInfo(st,st.session_state.character["powers"])
    
    total_powers = len(st.session_state.character["powers"])
    points_left = (st.session_state.character["rank"].value *5) - total_powers

    if points_left < 0:
        st.error(f"You have too many powers! Reduce by {-points_left}.")
    else:
        st.info(f"Powers left: {points_left}")

def display_stats(st):

    
    DisplayCharacterStats(st,
                          st.session_state.character["rank"].value,
                          st.session_state.character["abilityStats"],
                          st.session_state.character["characterStats"]
                          )
def display_movement(st):
    st.header(f"**Movement**")
    DisplayMovmentStats(st,
                          st.session_state.character["rank"].value,
                          st.session_state.character["abilityStats"],
                          st.session_state.character["characterStats"]
                          )
    
def add_origins(st):
    
    selected_origin = getDictEntryFromSelect(st,"Choose Origin", 'name',st.session_state.originList)
    if selected_origin:
        DisplayTabularInfo(st,selected_origin)
        pressed = st.button("Add Origin",key = selected_origin['name'])
        if pressed:            
            st.session_state.character["origin"] = selected_origin
            addRelated(st,selected_origin)
           

def display_origin(st):
     DisplayTabularInfo(st,st.session_state.character["origin"])

def display_occupation(st):    
    DisplayTabularInfo(st,st.session_state.character["occupation"])
                
def display_traits(st):

    total_traits = len(st.session_state.character["traits"])
    traits_left = (st.session_state.character["rank"].value *4) - total_traits

    if traits_left < 0:
        st.error(f"You have too many traits! Reduce by {-traits_left}.")
    else:
        st.info(f"Powers traits: {traits_left}")

    for traitItem in st.session_state.character["traits"]:
        with st.expander(traitItem["name"]):   
            DisplayTabularInfo(st,traitItem)
                
def display_tags(st):
     for tagItem in st.session_state.character["tags"]:
        with st.expander(tagItem["name"]):   
            DisplayTabularInfo(st,tagItem)

def add_occupations(st):

    selected_occupation = getDictEntryFromSelect(st,"Choose Occupation", 'name',st.session_state.occupationList)

    if selected_occupation:
        DisplayTabularInfo(st,selected_occupation)
        pressed = st.button("Add Occupation",key = selected_occupation['name'])
        if pressed:            
            st.session_state.character["occupation"] = selected_occupation
            addRelated(st,selected_occupation)
        
def add_traits(st):

    selected_trait = getDictEntryFromSelect(st,"Choose Trait", 'name',st.session_state.traitList)

    if selected_trait:
        DisplayTabularInfo(st,selected_trait)
        pressed = st.button("Add Trait",key = selected_trait['name'])
        if pressed:       
            st.session_state.character["traits"].append(selected_trait)
            addRelated(st,selected_trait)


def add_tags(st):
    selected_tag = getDictEntryFromSelect(st,"Choose Tag", 'name',st.session_state.tagList)

    if selected_tag:
        DisplayTabularInfo(st,selected_tag)
        pressed = st.button("Add Tag",key = selected_tag['name'])
        if pressed:
            st.session_state.character["tags"].append(selected_tag)
            addRelated(st,selected_tag)

def getDictEntryFromSelect(st, selectBoxText, keyName, dictList):

    getAllKeyValues = [KeyValues[keyName] for KeyValues in dictList]
    
    selected_KeyValues = st.selectbox(selectBoxText, options=sorted(key.strip() for key in getAllKeyValues))   
    
    selected_dictEntry = next(
                            (KeyValue for KeyValue in dictList if KeyValue[keyName].strip() == selected_KeyValues),
                            None
                            )
    if selected_dictEntry:
        return selected_dictEntry


