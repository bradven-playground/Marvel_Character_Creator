import pandas as pd
from data_filter import *

def DisplayCharacterStats(st, rank, Ability,CalcStats):   

    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"#### Health: {CalcStats['Health']}")
        st.markdown(f"#### Focus: {CalcStats['Focus']}")
        st.markdown(f"#### Initative: {CalcStats['Initative Mod']}")
        st.markdown(f"#### Actions: {CalcStats['Actions']}")

    with cols[1]:
        st.markdown(f"##### Health Dmg Reduction: {CalcStats['Health Dmg Reduction']}")
        st.markdown(f"##### Focus Dmg Reduction: {CalcStats['Focus Dmg Reduction']}")
        st.markdown(f"##### ")
        st.markdown(f"#### Reactions: {CalcStats['Reactions']}")

    st.markdown("--------------------")
    
    df = pd.DataFrame({
        "##### Type": ["##### Melee", "##### Agility", "##### Resilience","##### Vigilance","##### Ego","##### Logic"],
        "##### Attack": [Ability['Melee'], Ability['Agility'], Ability['Resilience'], Ability['Vigilance'], Ability['Ego'], Ability['Logic']],        
        "##### Damage": [
                        "M x " + str(CalcStats['Melee Dmg Multiplier']+rank) + " + " + str(Ability['Melee']), 
                        "M x " + str(CalcStats['Agility Dmg Multiplier']+ rank) + " + " + str(Ability['Agility']), 
                        "-", 
                        "-", 
                        "M x " + str(CalcStats['Ego Dmg Multiplier']+rank) + " + " + str(Ability['Ego']), 
                        "M x " + str(CalcStats['Logic Dmg Multiplier']+rank) + " + " + str(Ability['Logic']), 
                        ],
        "##### Defence": [CalcStats['Melee Defence Score'], CalcStats['Agility Defence Score'],CalcStats['Resilience Defence Score'],CalcStats['Vigilance Defence Score'],CalcStats['Ego Defence Score'],CalcStats['Logic Defence Score'],],                         
        "##### Out of Combat": [CalcStats['Melee Non-Combant Check'], CalcStats['Agility Non-Combant Check'],CalcStats['Resilience Non-Combant Check'],CalcStats['Vigilance Non-Combant Check'],CalcStats['Ego Non-Combant Check'],CalcStats['Logic Non-Combant Check'],],
                  
    })

    st.table(df)   

    #df.style.set_properties(**{'text-align': 'center'}) 

    #st.dataframe(df)

    
                
def DisplayMovmentStats(st, rank, Ability,CalcStats): 
    
    
    df = pd.DataFrame({
        "##### Momevement Type": ["##### Run Speed", "##### Jump Speed", "##### Flight Speed","##### Climb Speed","##### Swim Speed","##### Web Swing Speed","##### Glide Speed","##### Teleport Speed"],
        "##### In Combat": [CalcStats['Combat Run Speed'], CalcStats['Combat Jump Speed'],CalcStats['Combat Flight Speed'],CalcStats['Climb Speed'],CalcStats['Swim Speed'],CalcStats['Combat Web Swing Speed'],CalcStats['Combat Glide Speed'],CalcStats['Combat Teleport Speed']],            
        "##### Out of Combat": [CalcStats['Run Speed'], CalcStats['Jump Speed'],CalcStats['Flight Speed'],CalcStats['Climb Speed'],CalcStats['Swim Speed'],CalcStats['Web Swing Speed'],CalcStats['Glide Speed'],CalcStats['Teleport Speed']],                  
        })
    
    st.table(df)   

    #styled = df.style.background_gradient(cmap="Blues").highlight_max(axis=0)
    #st.dataframe(styled)

    

def DisplayTabularInfo(st,Info):

    if Info:        
        df = pd.DataFrame(list(Info.items()), columns=['Stat', 'Value'])
        #st.dataframe(df)
        styled_df = df.style.set_properties(**{'text-align': 'left'})
        st.dataframe(styled_df)
        

def DisplayPowerInfo(st,powers):
    if powers:
        sorted_powers = sorted(powers, key=lambda p: p["name"].strip().lower())
        for power in sorted_powers:
            with st.expander(power["name"]):
                DisplayTabularInfo(st,power)
                #if it's not a prerequisit for another power, give the user the option to remove
                prereq = isPrerequisite(power,st.session_state.character["powers"])
                
                if not prereq:
                
                    pressed = st.button("Remove Power",key = power['name'] + " Remove")
                    if pressed:
                
                        if power in st.session_state.character["powers"]:
                            st.session_state.character["powers"].remove(power)  
                else:
                    st.write("Power is a pre-requisite for another power and cannot be removed")


def display_powers(st):
    st.header(f"**Powers**")
    showPowerCount(st)
    DisplayPowerInfo(st,st.session_state.character["powers"])
    
    

def showPowerCount(st):
    
    powers_left = calcPowerChoicesRemaining(st)
    traits_left = calcTraitChoicesRemaining(st)
    stats_left = calcAttributeChoicesRemaining(st)

    if traits_left < 0:
        powers_left += traits_left
    
    if stats_left < 0:
        powers_left += stats_left

    if powers_left < 0:
        st.error(f"You have too many powers! Reduce by {-powers_left}.")
    else:
        st.info(f"Powers left: {powers_left}")

def display_abilities(st):
     
    cols = st.columns(2) # split into 2 columns for readability
    
    for idx, (stat,value) in enumerate(st.session_state.character["abilityStats"].items()):
        with cols[idx % 2]:            
            st.markdown(f"{stat}: {value}")
                

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

    #since powers can be used for traits
    traits_left = calcTraitChoicesRemaining(st)
    powers_left = calcPowerChoicesRemaining(st)    
    stats_left = calcAttributeChoicesRemaining(st)

    traits_left += powers_left
    
    if stats_left < 0:
        traits_left += stats_left

    #traits_left = calcTraitChoicesRemaining(st) + calcPowerChoicesRemaining(st)

    if traits_left < 0:
        st.error(f"You have too many traits! Reduce by {-traits_left}.")
    else:
        st.info(f"Traits Choices Left: {traits_left}")

    traitItems=st.session_state.character["traits"]
    for traitItem in traitItems:
        with st.expander(traitItem["name"]):   
            DisplayTabularInfo(st,traitItem)

            #if it's not a prerequisit for another power, give the user the option to remove
            prereq = isPrerequisite(traitItem,st.session_state.character["powers"])
            
            if not prereq:
            
                pressed = st.button("Remove Trait",key = traitItem['name'] + " Remove")
                if pressed:
            
                    if traitItem in st.session_state.character["traits"]:
                        st.session_state.character["traits"].remove(traitItem)  
            else:
                st.write("Power is a pre-requisite for another power and cannot be removed")


                
def display_tags(st):

    tagItems = st.session_state.character["tags"]
    for tagItem in tagItems:
        with st.expander(tagItem["name"]):   

            DisplayTabularInfo(st,tagItem)

            pressed = st.button("Remove Trait",key = tagItem['name'] + " Remove")
            if pressed:
                
                if tagItem in st.session_state.character["tags"]:
                    st.session_state.character["tags"].remove(tagItem)  

def add_occupations(st):

    selected_occupation = getDictEntryFromSelect(st,"Choose Occupation", 'name',st.session_state.occupationList)

    if selected_occupation:
        DisplayTabularInfo(st,selected_occupation)
        pressed = st.button("Add Occupation",key = selected_occupation['name'] + " Add")
        if pressed:            
            st.session_state.character["occupation"] = selected_occupation
            addRelated(st,selected_occupation)
        
def add_traits(st):

    selected_trait = getDictEntryFromSelect(st,"Choose Trait", 'name',st.session_state.traitList)

    if selected_trait:
        DisplayTabularInfo(st,selected_trait)
        pressed = st.button("Add Trait",key = selected_trait['name'] + " Add")
        if pressed:       
            st.session_state.character["traits"].append(selected_trait)
            addRelated(st,selected_trait)


def add_tags(st):
    selected_tag = getDictEntryFromSelect(st,"Choose Tag", 'name',st.session_state.tagList)

    if selected_tag:
        DisplayTabularInfo(st,selected_tag)
        
        pressed = st.button("Add Tag",key = selected_tag['name'] + " Add")
        if pressed:
            st.session_state.character["tags"].append(selected_tag)
            addRelated(st,selected_tag)



def setBackgroundColour(st):
    st.markdown(
    """
    <style>
    .stApp {
        background-color: #C00616; /* Replace with your desired color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def displayInfo(st):
    st.title("Information")

    st.header("Character Sheet Tab")
    st.markdown("The Character Sheet tab displays the information for your Hero based on what you've " \
    "selected on the other tabs.  You can remove powers,traits, and tags from here.  If you'd like" \
    "to update anything else, please use the appropriate tab.\n\n" \
    "You may need to click the 'Refresh' button at the top of the page if you don't see anything added/adjust from the other tabs")

    st.header("Attributes Tab")
    st.markdown("The attributes tab lets you adjust the hero's name,rank,and stats/attributes\n\n" \
    "Note: Changing Rank/Attributes doesn't allways stick, you may have to select it a second time.")

    st.header("Origin/Occupation/Traits/Tags Tab")
    st.markdown("The Origin/Occupation/Traits/Tags tab lets you select the heroes Origin, Occupation, Traits, and Tags" \
    ". They will be displayed on the Character Sheet.")

    st.header("Powers List Tab")
    st.markdown("The Powers List is where you can select power to add to your hero. Select the power set you want to choose from," \
    " then the power you'd like to add.  Any power missing the pre-requisite uisite should show what you're missing and won't be addable unless" \
    " those pre-requisites are met.\n\nYou will likely need to click the 'Refresh' button to see change to the pre-requisites" \
    "after adding a new power")
    
    st.header("Save/Load Tab")
    st.markdown("This is where you can upload and save heroes, including upload a picture for their avatar" \
    " For some reason, the load isn't working on mobile./n/nIF you want to edit a character you've loaded, you'll need to click the" \
    " 'x' to 'unload' the character in the load box, or it will revert any edit you try to do.")

def loadBanner(st):
    st.image("banner.png")