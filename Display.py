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
                print(prereq)
                if not prereq:
                    print("isPrerequisite")
                    pressed = st.button("Remove Power",key = power['name'])
                    if pressed:
                        print("pressed")
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
    
    origin_names = [origin["name"] for origin in st.session_state.originList]
    #st.info(origin_names)
    selected_origin_name = st.selectbox("Choose Origin", options=sorted(name.strip() for name in origin_names))   
    selected_origin = next(
        (origin for origin in st.session_state.originList if origin["name"].strip() == selected_origin_name),
         None
        )
    if selected_origin:
        DisplayTabularInfo(st,selected_origin)
        pressed = st.button("Add Origin",key = selected_origin['name'])
        if pressed:            
            st.session_state.character["origin"] = selected_origin
            
            tagsToAdd = selected_origin['tags'].split(",")
            for tagToAdd in tagsToAdd:
                st.session_state.character["tags"] = findInDict(tagToAdd, 'name',)
            #broken here, need to iterate on each of the tags/traits/powers in the origin, find the tag in the appropriate list,  and add to the character

            #if not "none" in selected_origin["tags"]:
                
                #add_tags(aselected_origin["tags"].append(findInDict() st.session_state.character["tags"] = selected_origin["tags"]
                #findInDict

            #if not "none" in selected_origin["traits"]:
                #st.session_state.character["traits"] = selected_origin["traits"]

            #if not "none" in selected_origin["powers"]:
                #st.session_state.character["trapowersits"] = selected_origin["powers"]

def display_origin(st):
     DisplayTabularInfo(st,st.session_state.character["origin"])

def display_occupation(st):
    DisplayTabularInfo(st,st.session_state.character["occupation"])
                
def display_traits(st):
    DisplayTabularInfo(st,st.session_state.character["traits"])
                
def display_tags(st):
    DisplayTabularInfo(st,st.session_state.character["tags"])

def add_occupations(st):
    occupation_names = [occupation["name"] for occupation in st.session_state.occupationList]
    #st.info(origin_names)
    selected_occupation_name = st.selectbox("Choose Occupation", options=sorted(name.strip() for name in occupation_names))   
    selected_occupation = next(
        (occupation for occupation in st.session_state.occupationList if occupation["name"].strip() == selected_occupation_name),
         None
        )
    if selected_occupation_name:
        DisplayTabularInfo(st,selected_occupation)
        #pressed = st.button("Add Origin",key = selected_origin['name'])
        #if pressed:            
            #st.session_state.character["origin"] = selected_origin
    pass
        
def add_traits(st):
    #trait_names = [trait["name"] for trait in st.session_state.traitList]
    ##st.info(origin_names)
    #selected_trait_name = st.selectbox("Choose Trait", options=sorted(name.strip() for name in trait_names))   
    #selected_trait = next(
        #(trait for trait in st.session_state.traitList if trait["name"].strip() == selected_trait_name),
#         None
        #)
    selected_trait = getDictEntryFromSelect(st,"Choose Trait", 'name',st.session_state.traitList)
    print (selected_trait)
    if selected_trait:
        DisplayTabularInfo(st,selected_trait)
        #pressed = st.button("Add Origin",key = selected_origin['name'])
        #if pressed:            
            #st.session_state.character["origin"] = selected_origin    

def add_tags(st):
    selected_trait = getDictEntryFromSelect(st,"Choose Tag", 'name',st.session_state.tagList)
    print (selected_trait)
    if selected_trait:
        DisplayTabularInfo(st,selected_trait)

def getDictEntryFromSelect(st, selectBoxText, keyName, dictList):

    getAllKeyValues = [KeyValues[keyName] for KeyValues in dictList]
    
    selected_KeyValues = st.selectbox(selectBoxText, options=sorted(key.strip() for key in getAllKeyValues))   
    
    selected_dictEntry = next(
                            (KeyValue for KeyValue in dictList if KeyValue[keyName].strip() == selected_KeyValues),
                            None
                            )
    if selected_dictEntry:
        return selected_dictEntry

