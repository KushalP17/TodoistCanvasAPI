import pycurl
from io import BytesIO
import json
from todoist_api_python.api import TodoistAPI
import xml.etree.ElementTree as ET
import xmltodict

api = TodoistAPI("541dcc565f0b489aba829275e6a2167d9097c665")


client = pycurl.Curl()
# client.setopt(client.URL, 'https://api.todoist.com/rest/v2/projects')
# client.setopt(pycurl.CUSTOMREQUEST, 'GET https://api.todoist.com/rest/v2/projects')
# print(client.getinfo())

# BigDataAlgo = 272330
# client.setopt(client.URL, "https://canvas.pitt.edu/api/v1/courses/" + str(BigDataAlgo) + "/assignments/")
# # client.setopt(pycurl.HTTPGET, '/api/v1/users/139970000000123737/courses/272330/assignments')
# client.setopt(client.WRITEFUNCTION, buffer.write)
# client.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer 13997~hcHTs5cUw9w8ezvidfNG6XSmjdOvFEZ9Y9XLd1Z5lr1US90kKTjciP23CcUn7gKO'])
# client.perform()

# body = json.loads((buffer.getvalue()).decode())

# taskName = "Test Task"
# taskLabel = "DSA2"
# taskDate = body[0]["due_at"]
# taskDescription = body[0]["description"]

# newTask = api.add_task(
#             content=taskName,
#             description=taskDescription,
#             project_id="2326003909",
#             labels=[taskLabel],
#             priority="4",
#             due_date=taskDate

#         )

# client.setopt(client.URL, 'https://api.todoist.com/rest/v2/tasks')
# client.setopt(pycurl.HTTPPOST, [("content", "Test Task"), ("description",body[0]["description"]), ("project_id", "2326003909") , ("due", {"datetime", body[0]["due_at"]}   ) ])
# client.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer 541dcc565f0b489aba829275e6a2167d9097c665'])
# client.perform()



# Canvas API URL
API_URL = "https://canvas.pitt.edu"
# Canvas API key
#canvas token = 13997~hcHTs5cUw9w8ezvidfNG6XSmjdOvFEZ9Y9XLd1Z5lr1US90kKTjciP23CcUn7gKO
API_KEY = "13997~hcHTs5cUw9w8ezvidfNG6XSmjdOvFEZ9Y9XLd1Z5lr1US90kKTjciP23CcUn7gKO"


# Initialize a new TodoistAPI object
# api = TodoistAPI("541dcc565f0b489aba829275e6a2167d9097c665")

# ID dict structure {Name: [canvas id, todoist id]}
# To get IDs - in canvas class home page links, and then deo api.get_projects() to find project, then api.get_tasks(project_id=...) to find and match tasks
# IDDict = {"Discrete Math": [241291, 7584605372], "Cyber Phys": [239973, 7584604462], "Circuit Lab": [239978, 7584603813], "Emag": [239988, 7584605720], "Linear Controls": [240005, 7584604132]}
IDDict = {"Computer Vision": [272410, 8338739178], "Assembly & Arch":[273509, 8338739661], "DSA2":[273700, 8338745986], "Big Data Algorithms":[272330, 8338747347], "Electric Machinery":[272447, 8338746578], "Space Class":[287661, 8338746940]}


dataFile = "C:/Users/parek/Desktop/Projects/TodoistCanvasAPI/ClassDataTest.xml"

tree = ET.parse(dataFile)
root = tree.getroot()

# #imminent tasks project id = 2326003909
# project = api.get_project(project_id="2326003909")
# # print(project)

# #Linear Controls task id = 7584604132
# LC = api.get_task(task_id="7584604132")
# # print(LC)

# #Emag task id = 7584605720
# EM = api.get_task(task_id="7584605720")
# # print(EM)

# #Cyber Phys task id = 7584604462
# CP = api.get_task(task_id="7584604462")
# # print(CP)

# #Discrete Math task id = 7584605372
# DM = api.get_task(task_id="7584605372")
# # print(DM)

# #Circuit Lab task id = 7584603813
# CL = api.get_task(task_id="7584603813")
# # print(CL)

def XMLfriendlyName(name):
    name = name.replace(" ","")
    name = name.replace("&","")
    name = name.replace("#","")
    name = name.replace("(","")
    name = name.replace(")","")
    name = name.replace(",","")
    name = name.replace("?","")
    return name

def cleanDescription(taskDescription):
    desc = taskDescription
    newDesc = ""

    while desc.find("<p>") != -1:
        linkelementIdx = desc.find("<p><a")
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
        else:
            textElementIdx = desc.find("<p>")
            desc = desc[textElementIdx+3:]
            endTextIdx = desc.find("</p>")
            textStr = desc[0:endTextIdx]
            desc = desc[endTextIdx:]
            newDesc = newDesc + textStr



    return newDesc


def updateDateAndDesc(todoistID, taskDate, taskDescription):
    taskDescription = cleanDescription(taskDescription)
    api.update_task(todoistID, due = taskDate, description=taskDescription)


def searchDuplicateTask( className, taskName, taskID, taskDate, taskDescription):
    className = XMLfriendlyName(className)
    taskName = XMLfriendlyName(taskName)
    
    classBranch = root.find(className)
    taskElement = classBranch.find(taskName)
    if taskElement == None:
        return False
    

    if taskElement.get("CanvasID") != taskID:
        return False
    
    # search xml file for duplicate assignment
    updateDateAndDesc(taskElement.get("TodoistID"), taskDate, taskDescription)
    return True

def documentTask(className, taskName, taskID, todoistID):
    className = XMLfriendlyName(className)
    taskName = XMLfriendlyName(taskName)

    
    classBranch = root.find(className)
    newTaskElement = ET.SubElement(classBranch, taskName)
    newTaskElement.set("CanvasID", taskID)
    newTaskElement.set("TodoistID", todoistID)
    # add task to xml file under correct class

def createTask(className = None, taskName = None, taskDate = None, taskDescription = None, taskID=None, taskLabel=None):
    
    if not searchDuplicateTask(className, taskName, taskID, taskDate, taskDescription):
        taskDescription = cleanDescription(taskDescription)
        newTask = api.add_task(
            content=taskName,
            description=taskDescription,
            project_id="2326003909",
            parent_id=IDDict[className][1],
            labels=[taskLabel],
            priority="4",
            due_date=taskDate

        )

        todoistID = newTask.id

        documentTask(className, taskName, taskID, todoistID)


def updateAssignments():
    # counter = 0


    for canvasClass in IDDict.keys():
        buffer = BytesIO()
        client.setopt(client.URL, "https://canvas.pitt.edu/api/v1/courses/" + str(IDDict[canvasClass][0]) + "/assignments/")
        client.setopt(client.WRITEFUNCTION, buffer.write)
        client.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer 13997~hcHTs5cUw9w8ezvidfNG6XSmjdOvFEZ9Y9XLd1Z5lr1US90kKTjciP23CcUn7gKO'])
        client.perform()
        # print(counter)
        # counter = counter + 1
        bufGV = buffer.getvalue()
        bufDC = bufGV.decode()
        bufDC = bufDC.replace("][", "],[")
        if(bufDC.find("],[") != -1): 
            bufDC = "{" + bufDC + "}"
        # print(bufDC)
        body = json.loads(bufDC)
        # body = json.loads((buffer.getvalue()).decode())
        for assignment in range(len(body)):
            createTask(canvasClass, body[assignment]["name"], body[assignment]["due_at"], body[assignment]["description"], str(body[assignment]["id"]), canvasClass)
        buffer.close()
        


    # formatTree = ET.indent(tree)
    # treeString = ET.tostring(root)

    # tree = ET.ElementTree(root)
    # ET.indent(tree, space="\t", level=0)
    # open(dataFile, "wb")
    # tree.write(dataFile, encoding="utf-8")

    ET.indent(root, space="\t", level=0)
    treeString = ET.tostring(root)

    with open(dataFile, "wb") as file:
        file.write(treeString)
    

    # with open(dataFile, "wb") as file:
    #     file.write(treeString)

updateAssignments()

