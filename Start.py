from PyQt6.QtCore import Qt
import pycurl
from io import BytesIO
import json
from todoist_api_python.api import TodoistAPI
import xml.etree.ElementTree as ET
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QFormLayout, QGridLayout, QDialogButtonBox, QRadioButton


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


class WindowAPIs(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Todoist Canvas Setup")
        self.setGeometry(100, 100, 512, 150)

        self.CanvasAPILineEdit = QLineEdit(parent = self)
        self.TodoistAPILineEdit = QLineEdit(parent = self)

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.clicked.connect(self.close)

        layout = QFormLayout()
        layout.addRow("Canvas API Key: ", self.CanvasAPILineEdit)
        layout.addRow("Todoist API Key: ", self.TodoistAPILineEdit)
        layout.addWidget(buttons)
        self.setLayout(layout)


class WindowTodoistProjects(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Todoist Canvas Setup")
        self.setGeometry(100, 100, 512, 150)
        self.ProjectOptions = []
        layout = QGridLayout()
        idx = 0

        projects = TDapi.get_projects()
        print((projects))
        for project in projects:
            tempRadio = QRadioButton(project.name)
            self.ProjectOptions.append([project, tempRadio])
            layout.addWidget(tempRadio, idx, 0)
            idx = idx + 1

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.clicked.connect(self.close)

        layout.addWidget(buttons)

        self.setLayout(layout)



class WindowCourses(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Todoist Canvas Setup")
        self.setGeometry(100, 100, 512, 150)

        numCourses = 10


        self.Courses = []
        self.CourseCodes = []
        for x in range(numCourses):
            self.Courses.append(QLineEdit(parent = self))
            self.CourseCodes.append(QLineEdit(parent = self))


        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.clicked.connect(self.close)

        layout = QGridLayout()

        for y in range(numCourses):
            layout.addWidget(QLabel(f"Course {y} Nickname:", parent=self), y, 0)
            layout.addWidget(self.Courses[y], y, 1)
            layout.addWidget(QLabel(f"Course {y} Code:", parent=self), y, 2)
            layout.addWidget(self.CourseCodes[y], y, 3)

        layout.addWidget(buttons, 10, 2)


        self.setLayout(layout)



app = QApplication([])
window = WindowAPIs()
window.show()
app.exec()

TDapi = TodoistAPI(window.TodoistAPILineEdit.text())

app1 = QApplication([])
window1 = WindowTodoistProjects()
window1.show()
app1.exec()

for radioIdx in window1.ProjectOptions:
    if radioIdx[1].isChecked():
        projID = radioIdx[0].id

app2 = QApplication([])
window2 = WindowCourses()
window2.show()
app2.exec()

personalData = ET.Element("User")
personalData.set("CanvasAPIKEY", window.CanvasAPILineEdit.text())
personalData.set("TodoistAPIKEY", window.TodoistAPILineEdit.text())
personalData.set("TodoistProjectID", str(projID))

# TDapi = TodoistAPI(window.TodoistAPILineEdit.text())


for classNum in range(len(window2.Courses)):
    if len(window2.Courses[classNum].text()) != 0:
        if len(window2.CourseCodes[classNum].text()) != 0:
            canvasName = window2.Courses[classNum].text()
            canvasCode = window2.CourseCodes[classNum].text()

            # print(projID)
            # print(len(canvasName))
            # print(len(canvasCode))

            try:
                classTask = TDapi.add_task(
                    content=canvasName,
                    project_id=str(projID),
                    labels=[canvasName],
                    priority="4"
                )

                tdid = classTask.id

            except:
                tdid = ""

            finally:
                course = ET.SubElement(personalData, XMLfriendlyName(canvasName))
                course.set("CanvasID", canvasCode)
                course.set("TodoistID", tdid)
                course.set("Name", canvasName)

ET.indent(personalData, space="\t", level=0)
treeString = ET.tostring(personalData)

with open("UserData.xml", "wb") as file:
    file.write(treeString)

# print(window.CanvasAPILineEdit.text())




