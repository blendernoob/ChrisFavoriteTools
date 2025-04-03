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
        newCircle = pm.circle(n = f"ctrl_{name}_{boneName}{str(jointNum)}_boneSide", nr = (0,0,1), c=(0,0,0))
        newGroup = pm.group(newCircle, n = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}_offset')

        return(newCircle, newGroup)

    elif ctrlShape == "Half Circle":
        newCircle = pm.circle(n = f"ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}", nr = (0,0,1), c=(0,0,0))
        pm.select(newCircle[0] + '.cv[3:7]')

        pm.scale(1, 1, 1e-05, relative = True, pivot = (0, 0, 0.5))

        pm.select(newCircle)
        pm.makeIdentity(newCircle[0], apply = True) #makeIdentity = freeze transformations

        newGroup = pm.group(empty = True,  n = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}_offset')

        pm.parent(newCircle, newGroup)

        return(newCircle, newGroup)
    
    elif ctrlShape == "Cube":
        newCircle = pm.curve(n = f"ctrl_{name}_{boneName}{str(jointNum)}_boneSide",  degree = 1, point = [(-1,0,1), (1,0,1), (1,0,-1), (-1, 0, -1), (-1, 0, 1), (-1, -2, 1), (1, -2 , 1), (1, 0, 1), (1, 0, -1),(1, -2,-1),  (-1, -2, -1), (-1, 0, -1), (-1, 0, 1), (-1, -2, 1),(-1, -2, -1),(1, -2, -1), (1, -2, 1)]) 
    
        pm.setAttr(newCircle + ".translate", 0, 1, 0)

        pm.makeIdentity(newCircle, apply = True) 
        pm.xform(newCircle, centerPivots = True)

        newGroup = pm.group(newCircle,  name = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}_offset') 

        return(newCircle, newGroup)

    elif ctrlShape == "3D Circle":
        # making the 3 circles and turning them into a 3D circle
        newCircle = pm.circle(name = f"ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}", nr = (0,0,1), c=(0,0,0))
        circle2 = pm.circle(name = f"{name}{boneName}Larry{str(jointNum)}{boneSide}")
        circle3 = pm.circle(name = f"{name}{boneName}Joe{str(jointNum)}{boneSide}")

        pm.select(circle2)
        pm.setAttr(circle2[0] +  ".rotate", 0, 90, 0)
        pm.makeIdentity(circle2[0], apply = True)

        pm.select(circle3)
        pm.setAttr(circle3[0] + ".rotate", 90, 0, 0)
        pm.makeIdentity(circle3[0], apply = True)

        pm.parent(f"{name}{boneName}Joe{str(jointNum)}{boneSide}Shape", f"{name}{boneName}Larry{str(jointNum)}{boneSide}Shape", newCircle, relative = True, shape = True)
        pm.delete(f"{name}{boneName}Joe{str(jointNum)}{boneSide}", f"{name}{boneName}Larry{str(jointNum)}{boneSide}")
        pm.select(newCircle)

        newGroup = pm.group(newCircle, name = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}_offset')

        return(newCircle, newGroup)
    
    elif ctrlShape == "Pyramid":
        newCircle  = cmds.curve(name = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}', degree = 1, point = [(2, 3, 2), (-2, 3, 2), (-2, 3, -2), (2, 3, -2), (0, 0, 0), (-2, 3, 2), (2, 3, 2), (0, 0, 0), (-2, 3, -2), (2, 3, -2), (2, 3, 2)])

        newGroup = cmds.group(empty = True, name = f'ctrl_{boneName}{str(jointNum)}_{boneSide}_offset')

        cmds.parent(newCircle, newGroup)

        return(newCircle, newGroup)

    elif ctrlShape == "Arrow Cross":
        newCircle = cmds.curve(name = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}', degree = 1, point = [(-1, 0, -1), (-1, 0, -3), (-2, 0, -3), (0, 0, -5), (2, 0, -3), (1, 0, -3), (1, 0, -1),(3, 0, -1), (3, 0, -2), (5, 0, 0), (3, 0, 2), (3, 0, 1), (1, 0, 1),(1, 0, 3), (2, 0, 3), (0, 0, 5), (-2, 0, 3), (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, 2), (-5, 0, 0), (-3, 0, -2), (-3, 0, -1), (-1, 0, -1)])

        newGroup = cmds.group(empty = True, name = f'ctrl_{boneName}{str(jointNum)}_{boneSide}_offset')

        cmds.parent(newCircle, newGroup)

        return(newCircle, newGroup)

    elif ctrlShape == "Root Arrows":
        newCircle = cmds.curve(name = f'ctrl_{name}_{boneName}{str(jointNum)}_{boneSide}', degree = 1, point = [(-4, 0, -1), (-3, 0, -3), (-1, 0, -4), (-1, 0, -6), (-2, 0, -6), (0, 0, -8), (2, 0, -6), (1, 0, -6), (1, 0, -6), (1, 0, -4), (3, 0, -3), (4, 0, -1), (6, 0, -1), (6, 0, -2), (8, 0, 0), (6, 0, 2), (6, 0, 1), (4, 0, 1), (3, 0, 3), (1, 0, 4), (1, 0, 6), (2, 0, 6), (0, 0, 8), (-2, 0, 6), (-1, 0, 6), (-1, 0, 4),(-3, 0, 3), (-4, 0, 1), (-6, 0, 1), (-6, 0, 2), (-8, 0, 0), (-6, 0, -2), (-6, 0, -1), (-4, 0, -1)])

        newGroup = cmds.group(newCircle, name = f'ctrl_{boneName}{str(jointNum)}_{boneSide}_offset')

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
    curPanel = cmds.textFieldGrp('curPanel', query = True, text = True)

    newPanel = cmds.curve(degree = 1, name = f'ctrl_{str(charName)}_panel', point = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)])
    newPanelInside = cmds.curve(degree = 1, name = f"ctrl_{str(charName)}_panel_Inside", point = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)])

    # moving the text point to the corner of the panel 
    # we are also making this text point unselectable, thus making the text unselectable as well.
    # that is unless we select them in the outliner
    textPoint = cmds.group(empty = True, name = f"ctrl_{str(charName)}_textPoint_ControlPanel")
    pm.setAttr(textPoint + ".overrideEnabled", 1)
    pm.setAttr(textPoint + ".overrideDisplayType", 2)
    cmds.xform(translation = (-1, 1, 0))
    cmds.parent(textPoint, newPanelInside)

    tributeGroup = cmds.group(newPanel, newPanelInside, name = f'ctrl_{str(charName)}_tribute_offset') 

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
    panelGroup = cmds.group(combinedPanel[0], name = f'ctrl_{str(charName)}_panel_offset')

    # adding the text
    if str(charName) != "":
        panelName = cmds.textCurves(font = "Liberation Mono", name = f'ctrl_{str(charName)}_panel_text', text = str(charName)) 
        pm.setAttr(panelName[0] + ".overrideEnabled", 1)
        pm.setAttr(panelName[0] + ".overrideDisplayType", 2)
        pm.matchTransform(panelName, textPoint) 

        pm.parent(panelName, textPoint)

        cmds.parent(textPoint, combinedPanel[0])

        print(panelName)

        # making the text shapes unselectable and only manipulatable via the empties
        # panelLetters = cmds.listRelatives(panelName, shapes = True, fullPath = True)

        # print(panelLetters)

# create a slider
def CreateSlider():
    charName = cmds.textFieldGrp('aName', query = True, text = True)
    functionName = cmds.textFieldGrp('ctrlFunction', query = True, text = True)
    curPanel = cmds.textFieldGrp('curPanel', query = True, text = True)

    newSliderBorder = cmds.curve(degree = 1, name = f"ctrl_{str(charName)}_{str(functionName)}_slider_border", point = [(-0.5, 0.5, 0), (4, 0.5, 0), (4, -0.5, 0), (-0.5, -0.5, 0), (-0.5, 0.5, 0)])
    newSliderControl = cmds.curve(degree = 1, name = f"ctrl_{str(charName)}_{str(functionName)}_slider", point = [(-0.35, 0.35, 0), (0.35, 0.35, 0), (0.35, -0.35, 0,), (-0.35, -0.35, 0), (-0.35, 0.35, 0)])
    
    newSliderGroup = cmds.group(newSliderControl, newSliderBorder, name = f"ctrl_{str(charName)}_{str(functionName)}_slider_offset")
    newSliderControlGroup = cmds.group(newSliderControl, name = f'ctrl_{str(charName)}_{str(functionName)}_slider_control_offset')
    newSliderBorderGroup = cmds.group(empty = True, name = f'ctrl_{str(charName)}_{str(functionName)}_slider_border_offset')

    # move the border group to the corner of the slider so we can scale it from side to side
    # then we can parent it to the group and edit it further 
    cmds.select(newSliderBorderGroup)
    cmds.xform(translation = (-0.5, 0.5, 0))
    cmds.parent(newSliderBorder, newSliderBorderGroup)

    # make the border of the slider unselectable
    pm.setAttr(newSliderBorderGroup + ".overrideEnabled", 1)
    pm.setAttr(newSliderBorderGroup + ".overrideDisplayType", 2)

    # change the color of the slider to yellow
    pm.setAttr(newSliderControlGroup + ".overrideEnabled", 1)
    pm.setAttr(newSliderControlGroup + ".overrideColor", 17)
   
    # if there is a name for our slider, we can scale it up
    if functionName != "" :
        sliderNameText = cmds.textCurves(font = "Liberation Mono", name = f"ctrl_{str(charName)}_{str(functionName)}_slider_text", text = str(functionName))
        pm.setAttr(sliderNameText[0] + ".overrideEnabled", 1)
        pm.setAttr(sliderNameText[0] + ".overrideDisplayType", 2)
        pm.matchTransform(sliderNameText, newSliderBorderGroup)

        pm.parent(sliderNameText, newSliderGroup)

    # we can parent the slider control group to the new slider group
    cmds.parent(newSliderControlGroup, newSliderBorderGroup, newSliderGroup)

    print(curPanel)

    # if there is text in the curPanel, we wil match transform to the panel in curPanel
    if curPanel != "":
        pm.matchTransform(newSliderGroup, curPanel)
        pm.parent(newSliderGroup, curPanel)

def CreateUpDownSlider():
    print("work in progress") 

# create a XY Panel
def CreateXYPanel():
    charName = cmds.textFieldGrp('aName', query = True, text = True)
    functionName = cmds.textFieldGrp('ctrlFunction', query = True, text = True)

    newXYPanelBorder = cmds.curve(degree = 1, name = f"ctrl_{str(charName)}_{str(functionName)}_XYPanel_Border", point = [(-2, 2, 0), (2, 2, 0), (2, -2, 0), (-2, -2, 0), (-2, 2, 0)])
    newXYPanelControl = cmds.curve(degree = 1, name = f"ctrl_{str(charName)}_{str(functionName)}_XYPanel_Control", point = [(-0.35, 0.35, 0), (0.35, 0.35, 0), (0.35, -0.35, 0), (-0.35, -0.35, 0), (-0.35, 0.35, 0)]) 

    newXYPanelGroup = cmds.group(newXYPanelBorder, newXYPanelControl, name = f"ctrl_{str(charName)}_{str(functionName)}_XYPanel_offset")
    newXYPanelBorderGroup = cmds.group(empty = True, name = f"ctrl_{str(charName)}_{str(functionName)}_XYPanel_Border_osffet")
    newXYPanelControlGroup = cmds.group(newXYPanelControl, name = f'ctrl_{str(charName)}_{str(functionName)}_slider_XYPanel_offset')

    cmds.select(newXYPanelBorderGroup)
    cmds.xform(translation = (-2, 2, 0))
    cmds.parent(newXYPanelBorder, newXYPanelBorderGroup)

    # make the border unselectable
    pm.setAttr(newXYPanelBorderGroup + ".overrideEnabled", 1)
    pm.setAttr(newXYPanelBorderGroup + ".overrideDisplayType", 2)

    # change the color of the xy panel to Yellow
    pm.setAttr(newXYPanelControlGroup + ".overrideEnabled", 1)
    pm.setAttr(newXYPanelControlGroup + ".overrideColor", 17)

    # add the name of the function to the top of the XY Panel
    if functionName != "":
        xYPanelText = cmds.textCurves(font = "Liberation Mono", name = f"ctrl_{str(charName)}_{str(functionName)}_XYPanel_Text", text = str(functionName))
        pm.setAttr(xYPanelText[0] + ".overrideEnabled", 1)
        pm.setAttr(xYPanelText[0] + ".overrideDisplayType", 2)
        pm.xform(scale = (0.6, 0.6, 0.6))
        pm.matchTransform(xYPanelText, newXYPanelBorderGroup)

        pm.parent(xYPanelText, newXYPanelBorderGroup)

    cmds.parent(newXYPanelBorderGroup, newXYPanelControlGroup, newXYPanelGroup)

# a new feature I want to make
# a control preview mode where we can interactivley rotate and scale our contorls before we spawn them into the world. 
# can be done for multiple controls at once
# upon create a control
#   - make a shape we can transform about
#   - a window pops up that has a simple okay and cancel button with text saying EDIT MODE
#       - write this window in QT as a means to learn it
#       - matter of fact, just lean QT reguardless
#   - if cancel is selected, then the proxy shape is deleted and the EDIT MODE window disapears
#   - after we position our shape, we hit the okay button
#   - the shape then is parented to the joint we want or is positioned in the place we want
# - ideas as to how to achieve this
#   - a proxy shape or proxy shapes are spawned and we can move about
#   - we dont even need an offset group
#   - after clicking okay
#       - the proxy shape is duplicated and history is deleted and transforms applied
#       - an empty group is spawned and it inherits the transform values of the proxy shape maybe except for scale
#       - the shape is parented to the empty group  
#       - repeat for each of the controls
#       - after completing the okay button disapears
def ShapePreviewMode():
    pass

# building the window
def CreateWindow():
    WindowID = "ChrisFavoriteTools"

    if cmds.window(WindowID, exists = True):
        cmds.deleteUI(WindowID)
    
    cmds.window(WindowID, title = "Toolchest", width = 100, height = 200, minimizeButton = False, maximizeButton = False) 
   
    mainLayout = cmds.formLayout(numberOfDivisions = 100)

    #The Control Creation Tool
    title1 = cmds.text(label = "Nurbs Control Creation Tool", font = 'obliqueLabelFont')
    
    #layout of the UI
    sep1 = cmds.separator(height = 5)
    aName = cmds.textFieldGrp('aName',label = 'Character Name = ', width = 5)
    bName = cmds.textFieldGrp('bName',label = 'Bone Names = ', width = 5)
    cmds.separator(height = 10)

    #Determining left or right side
    sep2 = pm.separator(h = 5)
    sideMenu = pm.optionMenu("sideMenu", label = "Which side?", height = 20, annotation = "Left Or Right?")
    cmds.menuItem(label = "Center")
    cmds.menuItem(label = "Left")
    cmds.menuItem(label = "Right")

    colorMenu = cmds.optionMenu("colorObject", label = "Color of Control", height = 20, annotation = "What Color do we want the new Control to be")
    cmds.menuItem(label = "Yellow")
    cmds.menuItem(label = "Green")
    cmds.menuItem(label = "Red")
    cmds.menuItem(label = "Blue")
    cmds.menuItem(label = "Magenta")
    cmds.menuItem(label = "Tan")

    shapeMenu = cmds.optionMenu("shapeOfObject", label = "Shape of control", height = 20, annotation = "What shape do we want the control to be")
    cmds.menuItem(label = "Full Circle")
    cmds.menuItem(label = "Half Circle")
    cmds.menuItem(label = "3D Circle")
    cmds.menuItem(label = "Cube")
    cmds.menuItem(label = "Pyramid")
    cmds.menuItem(label = "Arrow Cross")
    cmds.menuItem(label = "Root Arrows")
    cmds.menuItem(label = "Up and Down Arrows")

    #should we parent the control to the bone right away?
    parentControl = cmds.checkBox("parentIt", label = "Parent Control", height = 20, annotation = "Parent the Control we are creating?", value = True)

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
    currentPanel = cmds.textFieldGrp("curPanel", label = "Add control to this panel = " )

    slider = pm.button(label = "Create Left Right Slider", command = 'CreateSlider()')
    sliderUpDown = pm.button(label = "Create Up Down Slider", command = "CreateUpDownSlider()")
    xYPanel = pm.button(label = "Create XY Panel", command = 'CreateXYPanel()')

    #formating the UI
    cmds.formLayout(mainLayout, edit = 1, attachForm = [
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
        (functionName, 'left', 5), (currentPanel, 'right', 5), 
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
                    (functionName, 'top', 5, mergeButton), (currentPanel, 'top', 5, mergeButton),
                    (slider, 'top', 5, functionName),
                    (sliderUpDown, 'top', 5, slider),
                    (xYPanel, 'top', 5, sliderUpDown)
    ])

    pm.showWindow("ChrisFavoriteTools")

CreateWindow()
