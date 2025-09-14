import re

def getUniquePowerSets(powers):
    #unique_values = list(set(power['power_set'] for power in powers)) 
    result = []
    for item in (power['power_set'] for power in powers):
        if ',' in item:
            # Split by comma and extend the result list
            # in theory, for powers that appear in two power sets, just add the first as it throws off when counting 
            #     the number of powerset a character has (as the one power will count as two)
            
            #result.extend(item.split(','))
            result.append(item.split(',')[0])
        else:
            # Just add the non-comma string
            result.append(item)

    result.append("All") #If the user wants to see all the powers

    return sorted(set(item.strip() for item in result))

def findPowersInPowerSet(powerList,selected_powerSet):
    result = []
    for power in powerList:
       #see if it matchs the power set
       if selected_powerSet in power['power_set'] or selected_powerSet == "All":
            result.append(power)            

    #return sorted(set(item.strip() for item in result))
    return sorted(result, key=lambda p: p["name"].strip().lower())

def findAvailablePowers(st,powerList,characterPowers, characterTags,Rank):
    result = []
    for power in powerList:

        eligible, reason = checkPrerequisites(power, characterPowers,characterTags,Rank)        

        if eligible:
            result.append(power['name'])
        else:            
            result.append(power['name'] + " : " + reason)        
        
    return sorted(set(item.strip() for item in result))

def findInDict(name, keyName, dictionary):
    for entry in dictionary:
        if entry[keyName] == name:
            return entry

def checkPrerequisites(power, characterPowers,characterTags,Rank):
    
    reason = []
    if not ("None" in power['prerequisites']):                

        prereqs = power['prerequisites'].split(",")

        #check the pre-requisites
        for prereq in prereqs:

            prereqDetails = prereq.split(":")    
            #checks rank requirement                
            if ("Rank" in prereqDetails[0]):
                preReqRank = int(prereqDetails[1])
                if (int(Rank) < int(preReqRank)):
                    reason.append("(Requires Rank: " + str(int(preReqRank)) + " )")
                    eligible  = False  
                     
            #checks if the hero has the pre-requisite powers
            elif ("Power" in prereqDetails[0]):
                if not any(power['name'] == prereqDetails[1] for power in characterPowers):
                    reason.append("(Requires Power: " + prereqDetails[1] + " )")
                    eligible = False

            elif ("Tag" in prereqDetails[0]):

                if not any(tags['name'] == prereqDetails[1] for tags in characterTags):
                    reason.append("(Requires Tag: " + prereqDetails[1] + " )")
                    eligible = False

    eligible = len(reason) == 0
    reason_str = ", ".join(reason)  # Combine reasons into one string
    return eligible, reason_str

def isPrerequisite(power,powerList):

    isPrereq = False
    for charPower in powerList:
        prereqs = charPower['prerequisites'].split(",")

        #check the pre-requisites
        for prereq in prereqs:
            #print("power: " + power['name'] + " prereq: " + prereq)
            if power['name'] in prereq:
                #print ("is prereq")
                isPrereq = True
            
    return isPrereq

def addRelated(st,selected_entry):

    addRelatedField(st,selected_entry, "tags", st.session_state.tagList,st.session_state.character["tags"])
    addRelatedField(st,selected_entry, 'traits', st.session_state.traitList,st.session_state.character["traits"])
    addRelatedField(st,selected_entry, 'occupation', st.session_state.occupationList,st.session_state.character["occupation"])
    addRelatedField(st,selected_entry, 'powers', st.session_state.powerList,st.session_state.character["powers"])
   

def addRelatedField(st,selected_entry, entryKey, dictToAddFrom, dictToAddTo):
     
     if(entryKey in selected_entry):
        
        if selected_entry[entryKey]:  
        
            entriesToAdd = selected_entry[entryKey].split(",")

            for entryToAdd in entriesToAdd:
        
                entry = findInDict(entryToAdd.strip(), 'name',dictToAddFrom)
        
                if entry:
                    if entry not in dictToAddTo:
        
                        dictToAddTo.append(entry)



def calcPowerChoicesRemaining(st):

    #The sysem rewards heros that stick to a few power sets, such that you can get extra power
    # the math is totalPower = 5 x Rank + (Rank - Total Power Set (and 'basic doesn't count))

    powerSetsInUse = getUniquePowerSets(st.session_state.character["powers"])
    
    NumberOfCharacterPowerSet = len(powerSetsInUse)
    
    if "All" in powerSetsInUse:    
        NumberOfCharacterPowerSet -= 1 #remove one for the 'all' category        
        
    if "Basic" in powerSetsInUse:    
        NumberOfCharacterPowerSet -= 1 #remove one for the 'Basic' category
            
    Rank = int(st.session_state.character["rank"].value)

    total_powers = len(st.session_state.character["powers"])

    return ((Rank * 4) + (max(0,Rank - NumberOfCharacterPowerSet)) - total_powers)

def calcAttributeChoicesRemaining(st):
    
    MaxPoints = st.session_state.character["rank"].value * 5
    current_total = sum(st.session_state.character["abilityStats"].get(stat, 0) for stat in st.session_state.character["abilityStats"])   
    
    return MaxPoints - current_total

def calcTraitChoicesRemaining(st):
    total_traits = len(st.session_state.character["traits"])
    traits_left = (st.session_state.character["rank"].value) - total_traits      
    return traits_left 

def getDictEntryFromSelect(st, selectBoxText, keyName, dictList):

    getAllKeyValues = [KeyValues[keyName] for KeyValues in dictList]
    
    selected_KeyValues = st.selectbox(selectBoxText, options=sorted(key.strip() for key in getAllKeyValues))   
    
    selected_dictEntry = next(
                            (KeyValue for KeyValue in dictList if KeyValue[keyName].strip() == selected_KeyValues),
                            None
                            )
    if selected_dictEntry:
        return selected_dictEntry