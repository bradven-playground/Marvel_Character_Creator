from enum import Enum
import pandas as pd

abilityBlock = ["Melee", 
             "Agility", 
             "Resilience", 
             "Vigilance", 
             "Ego", 
             "Logic"
             ]

statBlock = ["Run Speed",
             "Combat Run Speed", 
             "Jump Speed",
             "Combat Jump Speed",
             "Climb Speed",
             "Flight Speed", 
             "Combat Flight Speed",
             "Swim Speed",
             "Combat Swim Speed",
             "Web Swing Speed",
             "Combat Web Swing Speed",
             "Glide Speed",
             "Combat Glide Speed",
             "Combat Teleport Speed",
             "Teleport Speed",
             "Initative Mod",
             "Health Dmg Reduction",
             "Focus Dmg Reduction",
             "Melee Dmg Multiplier", 
             "Agility Dmg Multiplier", 
             "Ego Dmg Multiplier",
             "Logic Dmg Multiplier",
             "Health",
             "Focus",
             "Actions",
             "Reactions",
             "Melee Defence Score",
             "Melee Non-Combant Check",
             "Agility Defence Score",
             "Agility Non-Combant Check",
             "Resilience Defence Score",
             "Resilience Non-Combant Check",
             "Vigilance Defence Score",
             "Vigilance Non-Combant Check",
             "Ego Defence Score",
             "Ego Non-Combant Check",
             "Logic Defence Score",
             "Logic Non-Combant Check"
            ]

class Rank(Enum):
    ROOKIE = 1
    PROTECTOR = 2
    CHAMPION = 3
    LEGEND = 4
    MYTHIC = 5
    COSMIC = 6
    
def AdjustStatBlock(st, Rank,Stats):
    MaxPoints = Rank * 5
    MaxValue = 3 + Rank


    # --- Initialize session_state values ONLY if not already set ---
    for stat in Stats:
        if stat not in st.session_state.character["abilityStats"]:
            st.session_state.character["abilityStats"][stat] = 0   
            
    # --- The stat block ---
    cols = st.columns(len(Stats) // 2)  # split into 2 columns for readability

    for idx, stat in enumerate(Stats):
        with cols[idx % (len(Stats) // 2)]:
            # Get the current value from the dictionary, default to 0 if missing
            current_value = min(st.session_state.character["abilityStats"].get(stat, 0),MaxValue)
            
            # Display number input and capture new value
            new_value = st.number_input(
                label=stat,
                min_value=0,
                max_value=MaxValue,                
                key=f"input_{stat}",  # use unique keys for Streamlit widgets
            )

        # Update the dictionary with the new value
        st.session_state.character["abilityStats"][stat] = new_value

    # Calculate points allocated and remaining
    current_total = sum(st.session_state.character["abilityStats"].get(stat, 0) for stat in Stats)
    points_left = MaxPoints - current_total

    if points_left < 0:
        st.error(f"You have allocated too many points! Reduce by {-points_left}.")
    else:
        st.info(f"Points left to spend: {points_left}")
    

def calcStatBlocks(st, rank, Stats, powers,traits):                       
    CalcStats = calculate_stats(rank, Stats, powers,traits)
    return CalcStats
   

def calculate_stats(rank, Stats, powers,traits):
    # Calculates and returns a dict of derived stats
    CalcStats = {
        #Movement Calcs
        "Run Speed": (Stats['Agility']//5 +5),    
        "Combat Run Speed": (Stats['Agility']//5 +5),        
        "Jump Speed":  (Stats['Agility']//5 +5)//2,
        "Combat Jump Speed": (Stats['Agility']//5 +5)//2,
        "Climb Speed": (Stats['Agility']//5 +5)//2,
        "Flight Speed": 0,       
        "Combat Flight Speed": 0,        
        "Swim Speed": ((Stats['Agility']//5 +5)//2),
        "Combat "
        "Swim Speed": ((Stats['Agility']//5 +5)//2),
        "Web Swing Speed": 0,
        "Combat Web Swing Speed": 0,
        "Glide Speed": 0,
        "Combat Glide Speed": 0,
        "Combat Teleport Speed": 0,
        "Teleport Speed": 0,
        #Ability Calcs
        "Health": max(Stats['Resilience'] * 30, 10),
        "Focus": max(Stats['Vigilance'] * 30, 10),
        "Actions":1,
        "Reactions":1,
        "Melee Defence Score": Stats['Melee'] + 10,
        "Melee Non-Combant Check": Stats['Melee'],        
        "Agility Defence Score": Stats['Agility'] +10,
        "Agility Non-Combant Check": Stats['Agility'],        
        "Resilience Defence Score": Stats['Resilience'] +10,
        "Resilience Non-Combant Check": Stats['Resilience'],
        "Vigilance Defence Score": Stats['Vigilance'] +10,
        "Vigilance Non-Combant Check": Stats['Vigilance'],
        "Ego Defence Score": Stats['Ego'] +10,
        "Ego Non-Combant Check": Stats['Ego'],
        "Logic Defence Score": Stats['Logic'] +10,
        "Logic Non-Combant Check": Stats['Logic'],     
        #Modifier Calcs
        "Initative Mod": Stats['Vigilance'],
        "Health Dmg Reduction": 0,
        "Focus Dmg Reduction": 0,        
        "Melee Dmg Multiplier": 0,
        "Agility Dmg Multiplier": 0,
        "Ego Dmg Multiplier": 0,
        "Logic Dmg Multiplier": 0
    }
    

    if powers:
        for power in powers:  
            adjustStats(power['statAdjusts'],rank, CalcStats)

    if traits:
        for trait in traits:  
            adjustStats(trait['statAdjusts'],rank, CalcStats)

    return CalcStats

def adjustStats(adjustEntry,rank, CalcStats):
        
    #only run if there are stast to adjust
    if not("none" in adjustEntry.lower()):
        
        statAdjust = adjustEntry.split(",")
        
        #Make each adjust            
        for statChanges in statAdjust:            

            #split type from calculation
            statAdjustDetails = statChanges.split(":")

            modifyType = statAdjustDetails[0].lower()                    
            statAdjustParams = statAdjustDetails[1].split(";")

            #split stat to modidy from the actual calculation            
            statToAdjust = statAdjustParams[0].strip()
            adjustParam = statAdjustParams[1].strip()
            
            #replace the stat with the one listed - take the higher of two
            if ("replace" in modifyType):
                
                if (adjustParam.isnumeric()):                
                    CalcStats[statToAdjust] = max(int(CalcStats[statToAdjust]),int(adjustParam))
                    
                elif ("rank" in adjustParam.lower()):
                    CalcStats[statToAdjust] = max(int(CalcStats[statToAdjust]),int(rank))
                    
                else:                    
                    CalcStats[statToAdjust] = max(int(CalcStats[statToAdjust]),int(CalcStats[adjustParam]))

            #Add the modifier to the base stat
            if ("add" in modifyType):                        
                CalcStats[statToAdjust] += int(adjustParam)

            #calculate the modifier
            if ("calc" in modifyType):   
                        
                #THis assumes all 'calc' are multipliers
                statAdjustCalcs = adjustParam.split("x")
                multipliers=[]                        

                #This lets there be multiple multipliers (Y x N x D) etc
                #supports:
                #  a raw number (2,3,4)
                #  'rank' - uses the characters current rank
                #   or assumes the string is an existing stat to be used
                
                for statAdjustCalc in statAdjustCalcs:     
                    if (statAdjustCalc.strip().isnumeric()):
                        multipliers.append(int(statAdjustCalc.strip()))
                    elif ("rank" in statAdjustCalc.strip().lower()):
                        multipliers.append(rank)
                    else:
                        multipliers.append(CalcStats[statAdjustCalc.strip()])

                total = 1
                #multiply them together!
                for multiplier in multipliers:
                    total *= multiplier
                                        
                CalcStats[statToAdjust] = total
            
    
