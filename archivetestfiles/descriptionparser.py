import json
from todoist_api_python.api import TodoistAPI
import xml.etree.ElementTree as ET
import xmltojson
import html_form_to_dict

# api = TodoistAPI("541dcc565f0b489aba829275e6a2167d9097c665")

# checkTask = api.get_task(8370564604)
# print(checkTask.description)
# desc = '<link rel="stylesheet" href="https://instructure-uploads.s3.amazonaws.com/account_139970000000000001/attachments/14081134/canvas_global_PITT_6_6_app.css"><p><a href="https://classroom.github.com/a/tdy6BFPL" target="_blank">https://classroom.github.com/a/tdy6BFPL</a></p> <p>&nbsp;</p> <p>&nbsp;</p><script src="https://instructure-uploads.s3.amazonaws.com/account_139970000000000001/attachments/14081133/canvas_global_PITT_6_6_app.js"></script>'
# print(desc)

# linkelementIdx = desc.find("<p><a")

# # while foundIdx != -1:
# # print(linkelementIdx)
# desc = desc[linkelementIdx:-1]
# print(desc)

# linkIdx = desc.find("href=")
# print(linkIdx)

# desc = desc[linkIdx+6:-1]
# endLinkIdx = desc.find('"')
# linkStr = desc[0:endLinkIdx]
# print(linkStr)

# print(desc)
# linkTextIdx = desc.find(">")
# linkTextEndIdx = desc.find("<")
# linkText = desc[linkTextIdx+1:linkTextEndIdx]
# print(linkText)

# checkTask.description = None
# newDesc = f"[{linkText}]({linkStr})"

# api.update_task(8370564604, description=newDesc)

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

print(cleanDescription('<a title="Semester Project Description" href="https://canvas.pitt.edu/courses/272410/pages/semester-project-description" data-course-type="wikiPages" data-published="true" data-api-endpoint="https://canvas.pitt.edu/api/v1/courses/272410/pages/semester-project-description" data-api-returntype="Page">Semester Project Description</a>')
)

# '<a title="Semester Project Description" href="https://canvas.pitt.edu/courses/272410/pages/semester-project-description" data-course-type="wikiPages" data-published="true" data-api-endpoint="https://canvas.pitt.edu/api/v1/courses/272410/pages/semester-project-description" data-api-returntype="Page">Semester Project Description</a>'
# '<link rel="stylesheet" href="https://instructure-uploads.s3.amazonaws.com/account_139970000000000001/attachments/14081134/canvas_global_PITT_6_6_app.css"><p><a href="https://classroom.github.com/a/Qc8APtQm" target="_blank">https://classroom.github.com/a/Qc8APtQm</a></p>\n<p>&nbsp;</p>\n<p>&nbsp;</p><script src="https://instructure-uploads.s3.amazonaws.com/account_139970000000000001/attachments/14081133/canvas_global_PITT_6_6_app.js"></script>'

