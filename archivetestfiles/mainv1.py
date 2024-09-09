from todoist_api_python.api import TodoistAPI
from canvasapi import Canvas
import xml.etree.ElementTree as ET

# Canvas API URL
API_URL = "https://canvas.pitt.edu"
# Canvas API key
#canvas token = 13997~hcHTs5cUw9w8ezvidfNG6XSmjdOvFEZ9Y9XLd1Z5lr1US90kKTjciP23CcUn7gKO
API_KEY = "13997~hcHTs5cUw9w8ezvidfNG6XSmjdOvFEZ9Y9XLd1Z5lr1US90kKTjciP23CcUn7gKO"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Initialize a new TodoistAPI object
api = TodoistAPI("541dcc565f0b489aba829275e6a2167d9097c665")

# ID dict structure {Name: [canvas id, todoist id]}
# To get IDs - in canvas class home page links, and then deo api.get_projects() to find project, then api.get_tasks(project_id=...) to find and match tasks
# IDDict = {"Discrete Math": [241291, 7584605372], "Cyber Phys": [239973, 7584604462], "Circuit Lab": [239978, 7584603813], "Emag": [239988, 7584605720], "Linear Controls": [240005, 7584604132]}
IDDict = {"Computer Vision": [272410, 8338739178], "Assembly & Arch":[273509, 8338739661], "DSA2":[273700, 8338745986], "Big Data Algorithms":[272330, 8338747347], "Electric Machinery":[272447, 8338746578], "Space Class":[287661, 8338746940]}


dataFile = "C:/Users/parek/Desktop/Projects/TodoistCanvasAPI/ClassData.xml"

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


def searchDuplicateTask( className, taskName, taskID):
    className = className.replace(" ","")
    className = className.replace("&", "")
    taskName = taskName.replace(" ","")
    taskName = taskName.replace("#","")
    taskName = taskName.replace("(","")
    taskName = taskName.replace(")","")
    taskName = taskName.replace(",","")
    taskName = taskName.replace("?","")
    
    classBranch = root.find(className)
    taskElement = classBranch.find(taskName)
    if taskElement == None:
        return False
    

    if taskElement.get("ID") != taskID:
        return False
    
    # search xml file for duplicate assignment
    return True

def documentTask(className, taskName, taskID):
    className = className.replace(" ","")
    className = className.replace("&", "")
    taskName = taskName.replace(" ","")
    taskName = taskName.replace("#","")
    taskName = taskName.replace("(","")
    taskName = taskName.replace(")","")
    taskName = taskName.replace(",","")
    taskName = taskName.replace("?","")

    
    classBranch = root.find(className)
    newTaskElement = ET.SubElement(classBranch, taskName)
    newTaskElement.set("ID", taskID)
    # add task to xml file under correct class

def createTask(className = None, taskName = None, taskDate = None, taskDescription = None, taskID=None, taskLabel=None):
    
    if not searchDuplicateTask(className, taskName, taskID):
        newTask = api.add_task(
            content=taskName,
            description=taskDescription,
            project_id="2326003909",
            parent_id=IDDict[className][1],
            labels=[taskLabel],
            priority="4",
            due_date=taskDate

        )

        documentTask(className, taskName, taskID)


def updateAssignments():
    for canvasClass in IDDict.keys():
        course = canvas.get_course(IDDict[canvasClass][0])
        for assignment in course.get_assignments():
            createTask(canvasClass, str(assignment)[0:-10], None, None, str(assignment)[-8:-1], canvasClass)

    # formatTree = ET.indent(tree)
    treeString = ET.tostring(root)

    with open(dataFile, "wb") as file:
        file.write(treeString)

updateAssignments()