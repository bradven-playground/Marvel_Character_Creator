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
             "Initative Mod",
             "Health Dmg Reduction",
             "Focus Dmg Reduction",
             "Melee Dmg Multiplier", 
             "Agility Dmg Multiplier", 
             "Ego Dmg Multiplier",
             "Logic Dmg Multiplier",
             "Health",
             "Focus",
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
        key = f"stat_{stat}"        
        if key not in st.session_state:
            st.session_state[key] = 0    
    # --- The stat block ---
    cols = st.columns(len(Stats)//2) # split into 2 columns for readability
    for idx, stat in enumerate(Stats):
        with cols[idx % (len(Stats)//2)]:
            key = f"stat_{stat}"            
            st.number_input(
                label=stat, 
                min_value=0, 
                max_value=MaxValue, 
                #value=st.session_state[key],  # Use the pre-set value
                key=key
            )

    # Calculate points allocated and remaining
    current_total = sum(st.session_state[f"stat_{stat}"] for stat in Stats)    
    points_left = MaxPoints - current_total

    if points_left < 0:
        st.error(f"You have allocated too many points! Reduce by {-points_left}.")
    else:
        st.info(f"Points left to spend: {points_left}")

    for stat in abilityBlock:
        Stats[stat] = st.session_state[f"stat_{stat}"]
    

def calcStatBlocks(st, rank, Stats, powers):                       
    CalcStats = calculate_stats(rank, Stats, powers)
    return CalcStats
   

def calculate_stats(rank, Stats, powers):
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
        #Ability Calcs
        "Health": max(Stats['Resilience'] * 30, 10),
        "Focus": max(Stats['Vigilance'] * 30, 10),
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
        "Initative Mod": 0,
        "Health Dmg Reduction": 0,
        "Focus Dmg Reduction": 0,        
        "Melee Dmg Multiplier": 0,
        "Agility Dmg Multiplier": 0,
        "Ego Dmg Multiplier": 0,
        "Logic Dmg Multiplier": 0
    }
    

    if powers:
        for power in powers:  

            #only run if there are stast to adjust
            if not("none" in power['statAdjusts'].lower()):
                
                statAdjust = power['statAdjusts'].split(",")
                
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
                            CalcStats[statToAdjust] = max(CalcStats[statToAdjust],int(adjustParam))
                        else:
                            CalcStats[statToAdjust] = max(CalcStats[statToAdjust],CalcStats[adjustParam])

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
            
    return CalcStats
