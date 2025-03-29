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
        pm.makeIdentity(newCircle[0], apply = True) #makeIdentity = freeze transformations

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

# to merge all the curves we have selected
# this would be good if we were making say a control panel
# this part of the script is pretty much ripped off verbatum from Adrian Sochacki,
# hopefully I can expand on this for combining curves for more shapes in the future

def MergeCurves(*args):
    selectedShapes = cmds.ls(selection = True)

    # if the number of shapes is less than 2, then we will get an error 
    if len(selectedShapes) < 2:
        cmds.error("You selected less than 2 objects")

    # the reason for the bounding box is that we want to center the point of the combined curves.
    # it will be deleted later
    boundingBox = pm.exactWorldBoundingBox(selectedShapes)

    comboCurve = cmds.listRelatives(shapes = True, fullPath = True)
    group = cmds.group(empty = True, name = "Tribute Group")

    # apply transformations of all the shapes that are selected 
    for x in range (len(selectedShapes)):
        cmds.makeIdentity(selectedShapes[x], apply = True, rotate = True, scale = True, translate = True)

    boxedCurve = cmds.curve(degree = 1, point = [(boundingBox[0],boundingBox[1], boundingBox[2]), (boundingBox[3], boundingBox[4], boundingBox[5])])
    boxedCurveShapes = cmds.listRelatives(boxedCurve, shapes = True, fullPath = True)

    # we are now selecting the boxed curve shape and everything else we are trying to combine, including the group
    pm.select(boxedCurveShapes)

    for x in range (len(selectedShapes)):
        cmds.select(comboCurve[x], add = True)

    cmds.select(group, add = True)

    # now we are parenting all the 
    cmds.parent(relative = True, shape = True)
    cmds.select(group)
    cmds.xform(centerPivots = True)
    cmds.hide(cmds.listRelatives(shapes = True, fullPath = True)[0])

    cmds.rename(cmds.listRelatives(shapes = True, fullPath = True)[0], "frameCurve, do not delete me")

    cmds.delete(boxedCurve)

    print("we created a new combined curve")

    print(selectedShapes)

    return(selectedShapes)

# Creating a control panel for a character
# We want to create something like this
# ---------------------------------------
# | NAME OF CHARACTER                   |
# | ----  ------------  --------------  |   
# | |--|  || |       |  ||  |---->   |  |  
# | |--|  ------------  | |          |  |
# | |  |                | |          |  |
# | |  |                | \/         |  |
# | ----                --------------  |
# ---------------------------------------
#
# Name of the character on top of control panel
# sliders with names on them
# a xy panel where we can move the control up and down
# much like boot strap buckaroos control panels

# an idea on how to bring the name of the control panel to the top of the control panel
#   - make an empty group before scaling the control panel
#   - xform it to (-1, 1, 0)
#   - parent it to the newPanelInside object
#   - if the panel is scaled we can move it around 

def CreateControlPanel():
    charName = cmds.textFieldGrp('aName', query = True, text = True) 

    ctrlPanelSizeX = cmds.textFieldGrp('panelX', query = True, text = True)
    ctrlPanelSizeY = cmds.textFieldGrp('panelY', query = True, text = True) 

    newPanel = cmds.curve(degree = 1, name = 'ctrl_' + str(charName) + '_panel', point = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)])
    newPanelInside = cmds.curve(degree = 1, name = 'ctrl_' + str(charName) + '_panel_Inside', point = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)])

    # moving the text point to the corner of the panel 
    textPoint = cmds.group(empty = True, name = str(charName) + '_textPoint_ControlPanel')
    cmds.xform(translation = (-1, 1, 0))
    cmds.parent(textPoint, newPanelInside)

    tributeGroup = cmds.group(newPanel, newPanelInside, name = 'ctrl_' + str(charName) + '_offset') 

    # scale the innerPanel to the size we pass it
    cmds.select(newPanelInside)

    # if the panelSizeX or Y is nothing we will have a default scale here
    if ctrlPanelSizeX == "" or ctrlPanelSizeY == "":
        cmds.xform(scale = (0.75, 0.75, 1.0))
    else:
        cmds.xform(scale = (float(ctrlPanelSizeX) - 0.25, float(ctrlPanelSizeY) - 0.25, 1))
        
    cmds.makeIdentity(apply = True, translate = True, rotate = True, scale = True)

    # scale the normal panel and apply the size
    cmds.select(newPanel)

    if ctrlPanelSizeX == "" or ctrlPanelSizeY == "":
        cmds.xform(scale = (1, 1, 1))
    else:
        cmds.xform(scale = (float(ctrlPanelSizeX), float(ctrlPanelSizeY), 1))

    cmds.makeIdentity(apply = True, translate = True, rotate = True, scale = True)

    # unparent objects so we can combine them next
    cmds.parent( newPanel, newPanelInside, textPoint, world = True)
    cmds.select(newPanel, newPanelInside)
    combinedPanel = MergeCurves()

    #clean up and renaming objects
    cmds.delete(tributeGroup)
    cmds.delete(newPanel)
    cmds.delete(newPanelInside)

    cmds.rename('ctrl_' + str(charName) + '_panel')
    panelGroup = cmds.group(combinedPanel[0], name = 'ctrl_' + str(charName) + '_panel_offset')

    # adding the text
    if str(charName) != "":
        panelName = cmds.textCurves(font = "Liberation Mono", name = 'ctrl_' + str(charName) + '_panel_text', text = str(charName)) 
        pm.matchTransform(panelName, textPoint) 

        cmds.parent(panelName, textPoint)

        cmds.parent(textPoint, combinedPanel[0])

        print(panelName)

        #combining the text into one curve



# create a slider
def CreateSlider():
    charName = cmds.textFieldGrp('aName', query = True, text = True)
    functionName = cmds.textFieldGrp('ctrlFunction', query = True, text = True)

    newSliderBorder = cmds.curve(degree = 1, name = "ctrl_" + str(charName) + str(functionName) + '_slider_border', point = [(-0.5, 0.5, 0), (4, 0.5, 0), (4, -0.5, 0), (-0.5, -0.5, 0), (-0.5, 0.5, 0)])
    newSliderControl = cmds.curve(degree = 1, name = "ctrl_" + str(charName) + str(functionName) + 'slider', point = [(-0.35, 0.35, 0), (0.35, 0.35, 0), (0.35, -0.35, 0,), (-0.35, -0.35, 0), (-0.35, 0.35, 0)])
    
    cmds.group(newSliderControl, newSliderBorder, name = 'ctrl_' + str(charName) + str(functionName) + 'slider_offset')
    newSliderControlGroup = cmds.group(newSliderControl, name = 'ctrl_' + str(charName) + str(functionName) + 'slider_control_offset')

    # change the color of the slider to yellow
    pm.setAttr(newSliderControlGroup + ".overrideEnabled", 1)
    pm.setAttr(newSliderControlGroup + ".overrideColor", 17)

    # add the name of the function to the top of the slider

def CreateUpDownSlider():
    pass

# create a XY Panel
def CreateXYPanel():
    charName = cmds.textFieldGrp('aName', query = True, text = True)
    functionName = cmds.textFieldGrp('ctrlFunction', query = True, text = True)

    newXYPanelBorder = cmds.curve(degree = 1, name = "ctrl_" + str(charName) + str(functionName) + "XYPanel_Border", point = [(-2, 2, 0), (2, 2, 0), (2, -2, 0), (-2, -2, 0), (-2, 2, 0)])
    newXYPanelControl = cmds.curve(degree = 1, name = "ctrl_" + str(charName) + str(functionName) + "XYPanel_Control", point = [(-0.35, 0.35, 0), (0.35, 0.35, 0), (0.35, -0.35, 0), (-0.35, -0.35, 0), (-0.35, 0.35, 0)]) 

    cmds.group(newXYPanelBorder, newXYPanelControl, name = "ctrl_" + str(charName) + "XYPanel_offset")
    newXYPanelControlGroup = cmds.group(newXYPanelControl, name = 'ctrl_' + str(charName) +  str(functionName) + 'slider_XYPanel_offset')

    # change the color of the xy panel to Yellow
    pm.setAttr(newXYPanelControlGroup + ".overrideEnabled", 1)
    pm.setAttr(newXYPanelControlGroup + ".overrideColor", 17)

    # add the name of the function to the top of the XY Panel

# building the window
def CreateWindow():
    WindowID = "ChrisFavoriteTools"

    if pm.window(WindowID, exists = True):
        pm.deleteUI(WindowID)
    
    pm.window(WindowID, title = "Toolchest", w = 100, h = 200, mnb = 0, mxb = 0) 
   
    mainLayout = pm.formLayout(nd = 100)

    #The Control Creation Tool
    title1 = pm.text(l = "Nurbs Control Creation Tool", fn = 'obliqueLabelFont')
    
    #layout of the UI
    sep1 = pm.separator(h = 5)
    aName = pm.textFieldGrp('aName', l = 'Character Name = ', width = 5)
    bName = pm.textFieldGrp('bName', l = 'Bone Names = ', width = 5)
    pm.separator(h = 10)

    #Determining left or right side
    sep2 = pm.separator(h = 5)
    sideMenu = pm.optionMenu("sideMenu", l = "Which side?", h = 20, ann = "Left Or Right?")
    pm.menuItem(l = "Center")
    pm.menuItem(l = "Left")
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

    # Control Panel Creation Tool
    panelX = cmds.textFieldGrp("panelX", label = "Panel Size X = " )
    panelY = cmds.textFieldGrp("panelY", label = "Panel Size Y = " )

    createControlPanelButton = pm.button(label = "Create Control Panel Template", command = 'CreateControlPanel()')

    mergeButton = pm.button(l = 'Merge selected curves', c = 'MergeCurves()')

    sep7 = cmds.separator(height = 5)

    functionName = cmds.textFieldGrp("ctrlFunction", label = "Slider / XY Panel Name = ")

    slider = pm.button(label = "Create Left Right Slider", command = 'CreateSlider()')
    sliderUpDown = pm.button(label = "Create Up Down Slider", command = "CreateUpDownSlider()")
    xYPanel = pm.button(label = "Create XY Panel", command = 'CreateXYPanel()')

    #formating the UI
    pm.formLayout(mainLayout, e = 1, attachForm = [
       (title1, 'top', 5), (title1, 'left', 5),
       (aName, 'left', 5), (aName, 'right', 5),
       (bName, 'left', 5), (bName, 'right', 5), 
       (sep1, 'left', 5), (sep1, 'right', 5),
        (sideMenu, 'left', 5), (parentControl, 'right', 5), 
        (colorMenu, 'left', 5), (colorMenu, 'right', 5), 
        (shapeMenu, 'left', 5), (shapeMenu, 'right', 5),
        (sep2, 'left', 5), (sep2, 'right', 5),
        (makeNCircle, 'left', 5),(makeNCircle, 'right', 5),
        (sep3, 'left', 5), (sep3, 'right', 5),
        (title2, 'left', 5),
        (sep4, 'top', 5),
        (makeCurveFromEdge, 'left', 5), (makeCurveFromEdge, 'right', 5),
        (sep5, 'left',5), (sep5, 'right', 5),
        (title3, 'left', 5),
        (sep6, 'left', 5), (sep6, 'right', 5),
        (createControlPanelButton, 'left', 5), (createControlPanelButton, 'right', 5),
        (panelX, 'left', 5), (panelY, 'right', 5),
        (mergeButton, 'left', 5), (mergeButton, 'right', 5),
        (functionName, 'left', 5), (functionName, 'right', 5), 
        (slider, 'left', 5), (slider, 'right', 5), 
        (xYPanel, 'left', 5), (xYPanel, 'right', 5),
        (sliderUpDown, 'left', 5), (sliderUpDown, 'right', 5)
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
                    (title3, 'top', 5, sep5),
                    (sep6, 'top', 5, title3),
                    (panelX, 'top', 5, sep6),
                    (panelY, 'top', 5, sep6),
                    (createControlPanelButton, 'top', 5, panelY ),
                    (mergeButton, 'top', 5, createControlPanelButton),
                    (functionName, 'top', 5, mergeButton),
                    (slider, 'top', 5, functionName),
                    (sliderUpDown, 'top', 5, slider),
                    (xYPanel, 'top', 5, sliderUpDown)
    ])

    pm.showWindow("ChrisFavoriteTools")

CreateWindow()
