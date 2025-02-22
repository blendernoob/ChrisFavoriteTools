import pymel.core as pm
import maya.cmds as cmds

# basically a collection of my favorite tools in Maya all in a special window
# I want to style this in the look of the old IRIX toolchest

# TODOs
# - add more shapes for new nurbs control creation tool
#       - Arrows that go both ways
#           - up down
#           - left and right
#        - control pannel preset
#           - have text entry for a title of control panel
#           - make slider generator with a button
#               - have text entry for each of the sliders
#       - the the generator adds a number at their end of the name, even if I select just one thing, need to fix that
# - finish the ribbon rig creation tool
#       - DONE create a curve from edge selection
#       - Generate ribbon from a loft
# - finish merge curves tool
#       - find out how to select the shape node using the ls command, it seems like it only selects the transform?
#       - allow for the function to run just from selecting the shapes in the viewport. 
# - find out if I can make a button to isolate joints and meshes instead of having to click on the buttons at the top
# 
# FUN EXTRAS FOR MORE LEARNING
# - rewrite for QT instead of the rather clunky built in ui version
#       - could perhaps make my own style sheet and button graphics to look like motif, or IRIX
# - Find out how to have my script update after saving it in vim
# - THE BIG ONE = make a control preview mode so I can edit the nurbs shapes and such before applying and parenting to the joints
#       - upon clicking create nurbs controls, make a dummy control that is not parented, so we can rotate and scale the control offsets, perhaps even the curves themselves
#       - after hitting apply, create the controls with the appropriate colors and parented to the joints propery
#       - preview mode could be in a seperate window that is created to let the user know we are in preview mode (make this in QT so I can learn it)

def CreateCircleControl():

    name = pm.textFieldGrp('aName', q = True, text = True)
    boneName = pm.textFieldGrp('bName', q = True, text = True)
    selectedJoint = pm.ls(sl = 1, type = 'joint')
    
    boneSide = ""

    pm.select(cl = 1)

    #to use the info in the gui options
    #we must make a variable for the outputs and make sure they are quereyable (meaning q = True)
    whichSide = pm.optionMenu('sideMenu', q = True, v = True)
    ctrlColor = pm.optionMenu('colorObject', q = True, v = True)
    ctrlShape = pm.optionMenu('shapeOfObject', query = True, v = True)
    parentOrNot = pm.checkBox('parentIt', q = True, v = True)

    if whichSide == "Right":
        boneSide = "_R"
    elif whichSide == "Left":
        boneSide = "_L"
    elif whichSide == "Center":
        boneSide = ""

    #picks a joint and 
    if not selectedJoint:
        pm.error("please select a joint ya doof")
    else:
        jointNum = 1
        for i in selectedJoint:
            if len(selectedJoint) > 1:
                newCircle, newGroup = MakeShape(name, boneName, jointNum, boneSide, ctrlShape, ctrlColor)
            else:
                newCircle, newGroup = MakeShape(name, boneName, jointNum, boneSide, ctrlShape, ctrlColor)

            jointNum += 1
            
            print(newGroup)

            #here We create a new color for the shape node
            #remember that pm.circle() creates two new nodes each time we use it, a transform and a shape node
            pm.setAttr(newGroup + ".overrideEnabled", 1)

            if ctrlColor == "Yellow":
                pm.setAttr(newGroup + ".overrideColor", 17)
            elif ctrlColor == "Green":
                pm.setAttr(newGroup + ".overrideColor", 14)
            elif ctrlColor == "Red":
                pm.setAttr(newGroup + ".overrideColor", 13)
            elif ctrlColor == "Blue":
                pm.setAttr(newGroup + ".overrideColor", 6)
            elif ctrlColor == "Magenta":
                pm.setAttr(newGroup + ".overrideColor", 9)
            elif ctrlColor == "Tan":
                pm.setAttr(newGroup + ".overrideColor", 21)

            pm.matchTransform(newGroup, i)

            #do we want to parent the control to the joint?
            if parentOrNot == True:
                pm.parentConstraint(newCircle, i, mo = False)

            pm.select(cl = 1) 
        
#creating a ribbon rig in steps. The first function just creates a nurbs curve from an edge selection 
def CreateCurveFromEdge():
   pm.polyToCurve()
 
#going to refactor the creation of controls into this function. Right now the cube doesnt make anything nor does it print anything
#We gotta find out why
def MakeShape(name, boneName, jointNum, boneSide, ctrlShape, ctrlColor):

    if ctrlShape == "Full Circle":
        newCircle = pm.circle(n = "ctrl_" + name + boneName + str(jointNum) + boneSide, nr = (0,0,1), c=(0,0,0))
        newGroup = pm.group(newCircle, n = 'ctrl_' + name + boneName + str(jointNum) + boneSide + '_offset')

        return(newCircle, newGroup)

    elif ctrlShape == "Half Circle":
        newCircle = pm.circle(n = "ctrl_" + name + boneName + str(jointNum) + boneSide, nr = (0,0,1), c=(0,0,0))
        pm.select(newCircle[0] + '.cv[3:7]')

        pm.scale(1, 1, 1e-05, relative = True, pivot = (0, 0, 0.5))

        pm.select(newCircle)
        pm.makeIdentity(newCircle[0], apply = True)

        newGroup = pm.group(empty = True,  n = 'ctrl_' + name + boneName + str(jointNum) + boneSide + '_offset')

        pm.parent(newCircle, newGroup)

        return(newCircle, newGroup)
    
    elif ctrlShape == "Cube":
        newCircle = pm.curve(n = "ctrl_" + name + boneName + str(jointNum) + boneSide,  degree = 1, point = [(-1,0,1), (1,0,1), (1,0,-1), (-1, 0, -1), (-1, 0, 1), (-1, -2, 1), (1, -2 , 1), (1, 0, 1), (1, 0, -1),(1, -2,-1),  (-1, -2, -1), (-1, 0, -1), (-1, 0, 1), (-1, -2, 1),(-1, -2, -1),(1, -2, -1), (1, -2, 1)]) 
    
        pm.setAttr(newCircle + ".translate", 0, 1, 0)

        pm.makeIdentity(newCircle, apply = True) 
        pm.xform(newCircle, centerPivots = True)

        newGroup = pm.group(newCircle,  n = 'ctrl_' + name + boneName + str(jointNum) + boneSide + '_offset') 

        return(newCircle, newGroup)

    elif ctrlShape == "3D Circle":
        # making the 3 circles and turning them into a 3D circle
        newCircle = pm.circle(n = "ctrl_" + name + boneName + str(jointNum) + boneSide, nr = (0,0,1), c=(0,0,0))
        circle2 = pm.circle(name = name + boneName + "Larry" + str(jointNum) + boneSide)
        circle3 = pm.circle(name = name + boneName + "Joe" + str(jointNum) + boneSide)

        pm.select(circle2)
        pm.setAttr(circle2[0] +  ".rotate", 0, 90, 0)
        pm.makeIdentity(circle2[0], apply = True)

        pm.select(circle3)
        pm.setAttr(circle3[0] + ".rotate", 90, 0, 0)
        pm.makeIdentity(circle3[0], apply = True)

        pm.parent(name + boneName + "Joe" + str(jointNum) + boneSide +  "Shape", name + boneName +  "Larry" + str(jointNum) + boneSide + "Shape", newCircle, relative = True, shape = True)
        pm.delete(name + boneName +  "Joe" + str(jointNum) + boneSide, name + boneName + "Larry" + str(jointNum) +  boneSide)
        pm.select(newCircle)

        newGroup = pm.group(newCircle, name = 'ctrl_' + name + boneName + str(jointNum) + boneSide + '_offset')

        return(newCircle, newGroup)
    
    elif ctrlShape == "Pyramid":
        newCircle  = cmds.curve(name = 'ctrl_' + name + boneName + str(jointNum) + boneSide, degree = 1, point = [(2, 3, 2), (-2, 3, 2), (-2, 3, -2), (2, 3, -2), (0, 0, 0), (-2, 3, 2), (2, 3, 2), (0, 0, 0), (-2, 3, -2), (2, 3, -2), (2, 3, 2)])

        newGroup = cmds.group(empty = True, name = 'ctrl_' + boneName + str(jointNum) + boneSide + '_offset')

        cmds.parent(newCircle, newGroup)

        return(newCircle, newGroup)

    elif ctrlShape == "Arrow Cross":
        newCircle = cmds.curve(name = 'ctrl_' + name + boneName + str(jointNum) + boneSide, degree = 1, point = [(-1, 0, -1), (-1, 0, -3), (-2, 0, -3), (0, 0, -5), (2, 0, -3), (1, 0, -3), (1, 0, -1),(3, 0, -1), (3, 0, -2), (5, 0, 0), (3, 0, 2), (3, 0, 1), (1, 0, 1),(1, 0, 3), (2, 0, 3), (0, 0, 5), (-2, 0, 3), (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, 2), (-5, 0, 0), (-3, 0, -2), (-3, 0, -1), (-1, 0, -1)])

        newGroup = cmds.group(empty = True, name = 'ctrl_' + boneName + str(jointNum) + boneSide + '_offset')

        cmds.parent(newCircle, newGroup)

        return(newCircle, newGroup)

    elif ctrlShape == "Root Arrows":
        newCircle = cmds.curve(n = 'ctrl_' + name + boneName + str(jointNum) + boneSide, degree = 1, point = [(-4, 0, -1), (-3, 0, -3), (-1, 0, -4), (-1, 0, -6), (-2, 0, -6), (0, 0, -8), (2, 0, -6), (1, 0, -6), (1, 0, -6), (1, 0, -4), (3, 0, -3), (4, 0, -1), (6, 0, -1), (6, 0, -2), (8, 0, 0), (6, 0, 2), (6, 0, 1), (4, 0, 1), (3, 0, 3), (1, 0, 4), (1, 0, 6), (2, 0, 6), (0, 0, 8), (-2, 0, 6), (-1, 0, 6), (-1, 0, 4),(-3, 0, 3), (-4, 0, 1), (-6, 0, 1), (-6, 0, 2), (-8, 0, 0), (-6, 0, -2), (-6, 0, -1), (-4, 0, -1)])

        newGroup = cmds.group(newCircle, name = 'ctrl_' + boneName + str(jointNum) + boneSide + '_offset')

        return(newCircle, newGroup)

#to merge all the curves we have selected
#this would be good if we were making say a control panel
def MergeCurves():
    selectedShapes = pm.ls(selection = True)

    print(selectedShapes)

#building the window
def CreateWindow():

    WindowID = "ChrisFavoriteTools"

    if pm.window(WindowID, exists = True):
        pm.deleteUI(WindowID)
    
    pm.window(WindowID, title = "Toolchest", w = 50, h = 200, mnb = 0, mxb = 0) 
   
    mainLayout = pm.formLayout(nd = 100)

#The Control Creation Tool
    title1 = pm.text(l = "Nurbs Control Creation Tool", fn = 'obliqueLabelFont')
    
    #layout of the UI
    sep1 = pm.separator(h = 5)
    aName = pm.textFieldGrp('aName', l = 'Character Name = ')
    bName = pm.textFieldGrp('bName', l = 'Bone Names = ')
    pm.separator(h = 10)

    #Determining left or right side
    sep2 = pm.separator(h = 5)
    sideMenu = pm.optionMenu("sideMenu", l = "Which side?", h = 20, ann = "Left Or Right?")
    pm.menuItem(l = "Left")
    pm.menuItem(l = "Center")
    pm.menuItem(l = "Right")

    colorMenu = pm.optionMenu("colorObject", l = "Color of Control", h = 20, ann = "What Color do we want the new Control to be")
    pm.menuItem(l = "Yellow")
    pm.menuItem(l = "Green")
    pm.menuItem(l = "Red")
    pm.menuItem(l = "Blue")
    pm.menuItem(l = "Magenta")
    pm.menuItem(l = "Tan")

    shapeMenu = pm.optionMenu("shapeOfObject", label = "Shape of control", height = 20, annotation = "What shape do we want the control to be")
    pm.menuItem(label = "Full Circle")
    pm.menuItem(label = "Half Circle")
    pm.menuItem(label = "3D Circle")
    pm.menuItem(label = "Cube")
    pm.menuItem(label = "Pyramid")
    pm.menuItem(label = "Arrow Cross")
    pm.menuItem(label = "Root Arrows")
    pm.menuItem(label = "Up and Down Arrows")

    #should we parent the control to the bone right away?
    parentControl = pm.checkBox("parentIt", l = "Parent Control", h = 20, ann = "Parent the Control we are creating?", v = 1)

    sep3 = pm.separator(h = 5)

    makeNCircle = pm.button(l = 'Make Nurbs Controls', c='CreateCircleControl()')

#The Ribbon Rig Creation Tool
    title2 = pm.text(l = "Ribbon Rig Creation Tool", fn = 'obliqueLabelFont')

    sep4 = pm.separator(h = 5)
    makeCurveFromEdge = pm.button(l = 'Create Nurbs from Edge', c='CreateCurveFromEdge()')

    sep5 = pm.separator(h = 5)

    title3 = pm.text(label = "Control Panel Shape Creation Tool", fn = 'obliqueLabelFont')

    sep6 = pm.separator(h = 5)

    mergeButton = pm.button(l = 'Merge selected curves', c = 'MergeCurves()')

    #formating the UI
    pm.formLayout(mainLayout, e = 1, attachForm = [
       (title1, 'top', 10), (title1, 'left', 5), 
       (aName, 'left', 5), (aName, 'right', 5),
       (bName, 'left', 5), (bName, 'right', 5), 
       (sep1, "left", 5), (sep1, "right", 5),
        (sideMenu, 'left', 5), (parentControl, 'right', 5), 
        (colorMenu, 'left', 5), (colorMenu, 'right', 5), 
        (shapeMenu, 'left', 5), (shapeMenu, 'right', 5),
        (sep2, "left", 5), (sep2, "right", 5),
        (makeNCircle, 'left', 5),(makeNCircle, 'right', 5),
        (sep3, "left", 5), (sep3, "right", 5),
        (title2, 'left', 5),
        (sep4, 'top', 5),
        (makeCurveFromEdge, 'left', 5), (makeCurveFromEdge, 'right', 5),
        (sep5, 'top',5),
        (title3, 'left', 5),
        (sep6, 'top', 5),
        (mergeButton, 'left', 5), (mergeButton, 'right', 5)
    ],

    attachControl = [
                    (sep1, 'top', 5, title1),
                    (aName, 'top', 5, sep1),
                    (bName, 'top', 5, aName),
                    (sideMenu, 'top', 5, bName), (parentControl, 'top', 5, bName),
                    (colorMenu, 'top', 5, sideMenu),
                    (shapeMenu, 'top', 5, colorMenu),
                    (makeNCircle, 'top', 5, shapeMenu),
                    (sep2, 'top', 5, makeNCircle),
                    (title2, 'top', 5, sep2),
                    (sep3, 'top', 5, title2),
                    (makeCurveFromEdge, 'top', 5, title2),
                    (sep5, 'top', 5, makeCurveFromEdge),
                    (title3, 'top', 5, makeCurveFromEdge),
                    (sep6, 'top', 5, title3),
                    (mergeButton, 'top', 5, title3)
    ])

    pm.showWindow("ChrisFavoriteTools")

CreateWindow()
