
import xml.etree.ElementTree as ET
import streamlit as st


def get_child_text(parent, tag):
    element = parent.find(tag)
    return element.text if element is not None else ""

@st.cache_data
def load_powers_from_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    powers = []
    for power_elem in root.findall("Power"):
        powers.append({
            "name": get_child_text(power_elem, "name"),
            "description": get_child_text(power_elem, "Description"),
            "power_set": get_child_text(power_elem, "PowerSet"),
            "prerequisites": get_child_text(power_elem, "PreRequisites"),
            "duration": get_child_text(power_elem, "Duration"),
            "action": get_child_text(power_elem, "Action"),
            "trigger": get_child_text(power_elem, "Trigger"),
            "cost": get_child_text(power_elem, "Cost"),
            "range": get_child_text(power_elem, "Range"),            
            "effect": get_child_text(power_elem, "Effect"),
            "statAdjusts": get_child_text(power_elem, "statAdjust"),

        })
    return powers

@st.cache_data
def load_origins_from_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    origins = []
    for origins_elem in root.findall("Origin"):
        origins.append({
            "name": get_child_text(origins_elem, "name"),
            "description": get_child_text(origins_elem, "description"),
            "examples": get_child_text(origins_elem, "examples"),
            "tags": get_child_text(origins_elem, "tags"),
            "traits": get_child_text(origins_elem, "traits"),
            "powers": get_child_text(origins_elem, "powers"),
            "suggestedOccupation": get_child_text(origins_elem, "suggestedOccupation"),
            "preRequisites": get_child_text(origins_elem, "preRequisites"),
            "limitation": get_child_text(origins_elem, "limitation"),
        })
    return origins

@st.cache_data
def load_tags_from_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    tags = []
    for tag_elem in root.findall("tag"):
        tags.append({
            "name": get_child_text(tag_elem, "name"),
            "description": get_child_text(tag_elem, "description"),
            "restriction": get_child_text(tag_elem, "restriction"),                
        })        
    return tags

@st.cache_data
def load_traits_from_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    traits = []
    for traits_elem in root.findall("Trait"):        
        traits.append({
            "name": get_child_text(traits_elem, "Name"),
            "description": get_child_text(traits_elem, "Description"),
            "restriction": get_child_text(traits_elem, "Restrictions"),                
            "statAdjusts": get_child_text(traits_elem, "statAdjust"),                
        })
    return traits


@st.cache_data
def load_occupations_from_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    Occupations = []
    for Occupation_elem in root.findall("occupation"):
        Occupations.append({
            "name": get_child_text(Occupation_elem, "name"),
            "description": get_child_text(Occupation_elem, "description"),
            "tags": get_child_text(Occupation_elem, "tags"),                
            "traits": get_child_text(Occupation_elem, "traits"),                
        })
    return Occupations
