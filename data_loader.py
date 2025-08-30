
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


