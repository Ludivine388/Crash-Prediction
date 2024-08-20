import xml.etree.ElementTree as ET

def get_root(file):
    # Load and parse the XML file
    tree = ET.parse(file)
    root = tree.getroot() 
    return root

def get_values(element, dict):
    # Extract values
    for child in element:
        # print(child.tag, child.attrib) // to check output
        dict[child.tag] = child.attrib
        get_values(child, dict)
    return dict

