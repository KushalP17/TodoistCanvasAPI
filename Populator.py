import xml.etree.ElementTree as ET
import os

# get file path
folder_path = os.getcwd()
folder_path = folder_path.replace('\\', '/')

userData = ET.parse(folder_path + "/UserData.xml")
userDataRoot = userData.getroot()

IDDict = {}

for userClass in userDataRoot:
        IDDict[userClass.attrib["Name"]] = [userClass.attrib["CanvasID"], userClass.attrib["TodoistID"]]

def XMLfriendlyName(name):
    name = name.replace(" ","")
    name = name.replace("&","")
    name = name.replace("#","")
    name = name.replace("(","")
    name = name.replace(")","")
    name = name.replace(",","")
    name = name.replace("?","")
    return name

def PopulateClasses():

    data = ET.Element('Classes')

    for canvasClass in IDDict.keys():
        ET.SubElement(data, XMLfriendlyName(canvasClass))

    newClassesStr = ET.tostring(data)

    with open("ClassData.xml", "wb") as file:
        file.write(newClassesStr)



PopulateClasses()