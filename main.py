import pycurl
from io import BytesIO
import os
import json
from todoist_api_python.api import TodoistAPI
import xml.etree.ElementTree as ET
from datetime import datetime


# Clean Names of Assignments & Courses to not cause XML errors
def XMLfriendlyName(name):
    name = name.replace(" ","")
    name = name.replace("&","")
    name = name.replace("#","")
    name = name.replace("(","")
    name = name.replace(")","")
    name = name.replace(",","")
    name = name.replace("?","")
    return name

# Description Parse
# Canvas spits out HTML of its descriptions 
# which cannot be properly parsed so we parse out text and links
def cleanDescription(taskDescription):
    desc = taskDescription
    newDesc = ""

    if desc is not None:
        while desc.find("<p>") != -1 or desc.find("<a ") != -1:
            linkelementIdx = desc.find("<p><a")
            paragraphElementIdx = desc.find("<p>")
            soleLinkElementIdx = desc.find("<a ")
            if linkelementIdx != -1:
                desc = desc[linkelementIdx:]
                linkIdx = desc.find("href=")
                desc = desc[linkIdx+6:]
                endLinkIdx = desc.find('"')
                linkStr = desc[0:endLinkIdx]
                linkTextIdx = desc.find(">")
                linkTextEndIdx = desc.find("<")
                linkText = desc[linkTextIdx+1:linkTextEndIdx]
                desc = desc[linkTextEndIdx:]
                newDesc = newDesc + f"[{linkText}]({linkStr})\n"
            elif paragraphElementIdx != -1:
                textElementIdx = desc.find("<p>")
                desc = desc[textElementIdx+3:]
                endTextIdx = desc.find("</p>")
                textStr = desc[0:endTextIdx]
                desc = desc[endTextIdx:]
                newDesc = newDesc + textStr
            elif soleLinkElementIdx != -1:
                desc = desc[soleLinkElementIdx:]
                linkIdx = desc.find("href=")
                desc = desc[linkIdx+6:]
                endLinkIdx = desc.find('"')
                linkStr = desc[0:endLinkIdx]
                linkTextIdx = desc.find(">")
                linkTextEndIdx = desc.find("</a>")
                linkText = desc[linkTextIdx+1:linkTextEndIdx]
                desc = desc[linkTextEndIdx:]
                newDesc = newDesc + f"[{linkText}]({linkStr})\n"


    return newDesc

# Update Date and Description
def updateDateAndDesc(todoistID, taskDate, taskDescription):
    taskDescription = cleanDescription(taskDescription)
    tdAPI.update_task(todoistID, due = taskDate, description=taskDescription)

# Don't add tasks twice using Canvas ID to check
def searchDuplicateTask( className, taskName, canvasID, taskDate, taskDescription):
    #clean names
    className = XMLfriendlyName(className)
    taskName = XMLfriendlyName(taskName)
    
    # find task
    classBranch = root.find(className)
    taskElement = classBranch.find(taskName)
    if taskElement == None:
        return False
    

    if taskElement.get("CanvasID") != canvasID:
        return False
    
    # update Due Date & Description of preexisting tasks
    updateDateAndDesc(taskElement.get("TodoistID"), taskDate, taskDescription)
    return True

# Record task in XML tree for duplication tracking, debugging, & testing
def documentTask(className, taskName, canvasID, todoistID):
    className = XMLfriendlyName(className)
    taskName = XMLfriendlyName(taskName)

    
    classBranch = root.find(className)
    newTaskElement = ET.SubElement(classBranch, taskName)
    newTaskElement.set("CanvasID", canvasID)
    newTaskElement.set("TodoistID", todoistID)
    # add task to xml file under correct class

def createTask(className = None, taskName = None, taskDate = None, taskDescription = None, taskID=None, taskLabel=None):
    
    if not searchDuplicateTask(className, taskName, taskID, taskDate, taskDescription):
        taskDescription = cleanDescription(taskDescription)
        
        newTask = tdAPI.add_task(
            
            content=taskName,
            description=taskDescription,
            project_id=int(TDProj_ID),
            parent_id=IDDict[className][1],
            labels=[taskLabel],
            priority="4",
            due_date=taskDate

        )

        todoistID = newTask.id

        documentTask(className, taskName, taskID, todoistID)


def updateAssignments():

    for canvasClass in IDDict.keys():
        # Make a buffer, retrieve Canvas assignment info per course and put it in the buffer
        buffer = BytesIO()
        client.setopt(client.URL, "https://canvas.pitt.edu/api/v1/courses/" + str(IDDict[canvasClass][0]) + "/assignments/")
        client.setopt(client.WRITEFUNCTION, buffer.write)
        client.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer ' + Canvas_API_KEY])
        client.perform()

        # Turn Buffer into Python string in Json Format
        bufGV = buffer.getvalue()
        bufDC = bufGV.decode()
        bufDC = bufDC.replace("][", "],[") # These 3 lines of code ensure the json format is followed
        if(bufDC.find("],[") != -1): 
            bufDC = "{" + bufDC + "}"

        body = json.loads(bufDC)
        print(body)

        for assignment in range(len(body)):
            createTask(canvasClass, body[assignment]["name"], body[assignment]["due_at"], body[assignment]["description"], str(body[assignment]["id"]), canvasClass)
        buffer.close()

    # Make the data XML file pretty/readable
    ET.indent(root, space="\t", level=0)
    treeString = ET.tostring(root)

    with open(dataFile, "wb") as file:
        file.write(treeString)
    
try:

    # get file path
    folder_path = os.getcwd()
    folder_path = folder_path.replace('\\', '/')
    # print(folder_path)

    # Initialize PyCurl client
    client = pycurl.Curl()

    # Look at UserData and get User API Keys
    userData = ET.parse(folder_path + "/UserData.xml")
    userDataRoot = userData.getroot()
    Canvas_API_KEY = userDataRoot.attrib["CanvasAPIKEY"]
    Todoist_API_KEY = userDataRoot.attrib["TodoistAPIKEY"]
    TDProj_ID = userDataRoot.attrib["TodoistProjectID"]
    # print(Canvas_API_KEY)
    # print(Todoist_API_KEY)

    # Initialize TodoistAPI Helper Library
    tdAPI = TodoistAPI(Todoist_API_KEY)

    # Assemble ID Dictionary for proper assignment retrieval/task placement
    IDDict = {}
    for userClass in userDataRoot:
        IDDict[userClass.attrib["Name"]] = [userClass.attrib["CanvasID"], userClass.attrib["TodoistID"]]


    #Data
    dataFile = folder_path + "/ClassData.xml"
    # print(dataFile)

    # Record assignments to catch duplicates
    tree = ET.parse(dataFile)
    root = tree.getroot()

    updateAssignments()

    with open("ErrorLogger.txt", 'a') as file:
        file.write(f"{datetime.now()}: Ran Successfully\n")

except Exception as error:
    with open("ErrorLogger.txt", 'a') as file:
        file.write(f"{datetime.now()}: {error}\n")

