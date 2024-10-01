

def cleanDescription(taskDescription):
    desc = taskDescription
    newDesc = ""

    if desc is None:
        return
    
    while desc.find("<p>") != -1 or desc.find("<a ") != -1 or desc.find("<") != -1:
        prghIdx = desc.find("<p>")
        linkIdx = desc.find("<a ")
        htmlIdx = desc.find("<")
        firstChar = checkText(desc)

        diffIdx = prghIdx - linkIdx

        if(htmlIdx != -1 and not firstChar):
            if(htmlIdx < prghIdx and htmlIdx < linkIdx):
                desc, outputDesc = descHTML(desc)
            elif(diffIdx > 1 or diffIdx == -(linkIdx+1) and linkIdx != -1):
                desc, outputDesc = descLink(desc)
            elif(diffIdx < -1 or diffIdx == (prghIdx+1) and prghIdx != -1):
                desc, outputDesc = descParagraph(desc)
            else:
                desc, outputDesc = descHTML(desc)
        else:
            desc, outputDesc = descText(desc)

        newDesc += outputDesc


    
    newDesc += desc
    return newDesc
    

def checkText(desc: str):
    return (desc[0] != '<' and desc[0] != '>')


def descText(desc: str):
    # handle text
    nonTextIdx = desc.find('<')
    outputDesc = desc[:nonTextIdx]
    desc = desc[nonTextIdx:]
    return desc, outputDesc




def descLink(desc: str):
    # handle link html elements
    startLIdx = desc.find("<a ")
    desc = desc[startLIdx+3:]
    linkIdx = desc.find("href=")
    desc = desc[linkIdx+6:]
    endLIdx = desc.find("</a>")

    
    endLink = desc.find('"')
    link = desc[:endLink]

    startMidDesc = desc.find(">")
    middleDesc = desc[startMidDesc+1:endLIdx]

    desc = desc[endLIdx+4:]

    outputDesc = cleanDescription(middleDesc)

    outputDesc = f"[{outputDesc}]({link})"
    return desc, outputDesc
    




def descParagraph(desc: str):
    # handle paragraph html elements
    startPIdx = desc.find("<p>")
    endPIdx = desc.find("</p>")
    desc = desc[startPIdx+3:]
    middleDesc = desc[:endPIdx-3]
    desc = desc[endPIdx+1:]
    outputDesc = cleanDescription(middleDesc)
    return desc, outputDesc



def descHTML(desc: str):
    # handle misc html elements
    # startElemIdx = desc.find("<")
    endElemIdx = desc.find(">")
    if endElemIdx == -1:
        desc = ""
    else:
        desc = desc[endElemIdx+1:]
    return desc, ""
    # print("HTML parsed")


testDesc = '<a title="Semester Project Description" href="https://canvas.pitt.edu/courses/272410/pages/semester-project-description" data-course-type="wikiPages" data-published="true" data-api-endpoint="https://canvas.pitt.edu/api/v1/courses/272410/pages/semester-project-description" data-api-returntype="Page">Semester Project Description</a>'
print(cleanDescription(testDesc))

testDesc2 = '<link rel="stylesheet" href="https://instructure-uploads.s3.amazonaws.com/account_139970000000000001/attachments/14081134/canvas_global_PITT_6_6_app.css"><p><a href="https://classroom.github.com/a/Qc8APtQm" target="_blank">https://classroom.github.com/a/Qc8APtQm</a></p>\n<p>&nbsp;</p>\n<p>&nbsp;</p><script src="https://instructure-uploads.s3.amazonaws.com/account_139970000000000001/attachments/14081133/canvas_global_PITT_6_6_app.js"></script>'
print(cleanDescription(testDesc2))

testDesc3 = None
print(cleanDescription(testDesc3))

print(descHTML("</script"))
