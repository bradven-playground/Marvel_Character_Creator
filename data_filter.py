import re

def getUniquePowerSets(powers):
    #unique_values = list(set(power['power_set'] for power in powers)) 
    result = []
    for item in (power['power_set'] for power in powers):
        if ',' in item:
            # Split by comma and extend the result list
            result.extend(item.split(','))
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
        print(entryKey)
        if selected_entry[entryKey]:  
            print (selected_entry[entryKey])
            entriesToAdd = selected_entry[entryKey].split(",")

            for entryToAdd in entriesToAdd:
                print (entryToAdd)
                entry = findInDict(entryToAdd.strip(), 'name',dictToAddFrom)
                print (entry)
                if entry:
                    if entry not in dictToAddTo:
                        print (entry)
                        dictToAddTo.append(entry)

