#Author-Jenna Knudsen
#Description-Creates a box with locking lid based on 

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

# All units in cm
defaultBoxName = 'BoxWithLid'
defaultLidThickness = 0.25
defaultWallWidth = .4
defaultFloorThickness = 0.2
defaultTolerance = .04
defaultBoxLength = 5
defaultBoxWidth = 4
defaultBoxHeight = 3
defaultTabLength = 0.3
defaultTabDistance = 0.2
defaultTabDepth = 0.1
defaultSlotWidth = 0.1
defaultSlotPosition = 0.2 

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

newComp = None

def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component

class BoxCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs

            boxWithLid = BoxWithLid()
            for input in inputs:
                if input.id == 'boxName':
                    boxWithLid.boxName = input.value
                elif input.id == 'lidThickness':
                    boxWithLid.lidThickness = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'wallWidth':
                    boxWithLid.wallWidth = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'floorThickness':
                    boxWithLid.floorThickness = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'tolerance':
                    boxWithLid.tolerance = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'boxLength':
                    boxWithLid.boxLength = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'boxWidth':
                    boxWithLid.boxWidth = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'boxHeight':
                    boxWithLid.boxHeight = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'tabLength':
                    boxWithLid.tabLength = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'tabDistance':
                    boxWithLid.tabDistance = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'tabDepth':
                    boxWithLid.tabDepth = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'slotWidth':
                    boxWithLid.slotWidth = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'slotPosition':
                    boxWithLid.slotPosition = unitsMgr.evaluateExpression(input.expression, "mm")

            boxWithLid.buildBox();
            args.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class BoxCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class BoxCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self):
        super().__init__()        
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = BoxCommandExecuteHandler()
            cmd.execute.add(onExecute)
            onExecutePreview = BoxCommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            onDestroy = BoxCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onExecutePreview)
            handlers.append(onDestroy)

            #define the inputs
            inputs = cmd.commandInputs
            inputs.addStringValueInput('boxName', 'Box Name', defaultBoxName)

            initLidThickness = adsk.core.ValueInput.createByReal(defaultLidThickness)
            inputs.addValueInput('lidThickness', 'Lid Thickness', 'mm', initLidThickness)

            initWallWidth = adsk.core.ValueInput.createByReal(defaultWallWidth)
            inputs.addValueInput('wallWidth', 'Wall Width', 'mm', initWallWidth)

            initFloorThickness = adsk.core.ValueInput.createByReal(defaultFloorThickness)
            inputs.addValueInput('floorThickness', 'Floor Thickness', 'mm', initFloorThickness)

            initTolerance = adsk.core.ValueInput.createByReal(defaultTolerance)
            inputs.addValueInput('tolerance', 'Tolerance', 'mm', initTolerance)

            initBoxLength = adsk.core.ValueInput.createByReal(defaultBoxLength)
            inputs.addValueInput('boxLength', 'Box Length', 'mm', initBoxLength)

            initBoxWidth = adsk.core.ValueInput.createByReal(defaultBoxWidth)
            inputs.addValueInput('boxWidth', 'Box Width', 'mm', initBoxWidth)

            initBoxHeight = adsk.core.ValueInput.createByReal(defaultBoxHeight)
            inputs.addValueInput('boxHeight', 'Box Height', 'mm', initBoxHeight)

            initTabLength = adsk.core.ValueInput.createByReal(defaultTabLength)
            inputs.addValueInput('tabLength', 'Tab Length', 'mm', initTabLength)

            initTabDistance = adsk.core.ValueInput.createByReal(defaultTabDistance)
            inputs.addValueInput('tabDistance', 'Tab Distance', 'mm', initTabDistance)

            initTabDepth = adsk.core.ValueInput.createByReal(defaultTabDepth)
            inputs.addValueInput('tabDepth', 'Tab Depth', 'mm', initTabDepth)

            initSlotWidth = adsk.core.ValueInput.createByReal(defaultSlotWidth)
            inputs.addValueInput('slotWidth', 'Slot Width', 'mm', initSlotWidth)

            initSlotPosition = adsk.core.ValueInput.createByReal(defaultSlotPosition)
            inputs.addValueInput('slotPosition', 'Slot Position', 'mm', initSlotPosition)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class BoxWithLid:
    def __init__(self):
        self._boxName = defaultBoxName
        self._lidThickness = defaultLidThickness
        self._wallWidth = defaultWallWidth
        self._floorThickness = defaultFloorThickness
        self._tolerance = defaultTolerance
        self._boxLength = defaultBoxLength
        self._boxWidth = defaultBoxWidth
        self._boxHeight = defaultBoxHeight
        self._tabLength = defaultTabLength
        self._tabDistance = defaultTabDistance
        self._tabDepth = defaultTabDepth
        self._slotWidth = defaultSlotWidth
        self._slotPosition = defaultSlotPosition

    #properties
    @property
    def boxName(self):
        return self._boxName
    @boxName.setter
    def boxName(self, value):
        self._boxName = value

    @property
    def lidThickness(self):
        return self._lidThickness
    @lidThickness.setter
    def lidThickness(self, value):
        self._lidThickness = value

    @property
    def wallWidth(self):
        return self._wallWidth
    @wallWidth.setter
    def wallWidth(self, value):
        self._wallWidth = value

    @property
    def floorThickness(self):
        return self._floorThickness
    @floorThickness.setter
    def floorThickness(self, value):
        self._floorThickness = value

    @property
    def tolerance(self):
        return self._tolerance
    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = value

    @property
    def boxLength(self):
        return self._boxLength
    @boxLength.setter
    def boxLength(self, value):
        self._boxLength = value

    @property
    def boxWidth(self):
        return self._boxWidth
    @boxWidth.setter
    def boxWidth(self, value):
        self._boxWidth = value

    @property
    def boxHeight(self):
        return self._boxHeight
    @boxHeight.setter
    def boxHeight(self, value):
        self._boxHeight = value

    @property
    def tabLength(self):
        return self._tabLength
    @tabLength.setter
    def tabLength(self, value):
        self._tabLength = value

    @property
    def tabDistance(self):
        return self._tabDistance
    @tabDistance.setter
    def tabDistance(self, value):
        self._tabDistance = value

    @property
    def tabDepth(self):
        return self._tabDepth
    @tabDepth.setter
    def tabDepth(self, value):
        self._tabDepth = value

    @property
    def slotWidth(self):
        return self._slotWidth
    @slotWidth.setter
    def slotWidth(self, value):
        self._slotWidth = value

    @property
    def slotPosition(self):
        return self._slotPosition
    @slotPosition.setter
    def slotPosition(self, value):
        self._slotPosition = value
        
    def buildBox(self):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create', 'New Component Failed')
                return

            # Create a new sketch.
            sketches = newComp.sketches
            xyPlane = newComp.xYConstructionPlane
            xzPlane = newComp.xZConstructionPlane
            baseSketch = sketches.add(xyPlane)
            center = adsk.core.Point3D.create(0, 0, 0)

            # create base of box
            corner1 = adsk.core.Point3D.create(-self.boxWidth / 2, -self.boxLength / 2)
            corner2 = adsk.core.Point3D.create(self.boxWidth / 2, self.boxLength / 2)
            box = baseSketch.sketchCurves.sketchLines.addTwoPointRectangle(corner1, corner2)

            # extrude it to base height
            extrudes = newComp.features.extrudeFeatures
            prof = baseSketch.profiles[0]
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distance = adsk.core.ValueInput.createByReal(self.floorThickness)
            extInput.setDistanceExtent(False, distance)
            baseExt = extrudes.add(extInput)

            # get the top face of this and create a new sketch on it
            # this sketch will create the walls
            topFace = newComp.findBRepUsingPoint(adsk.core.Point3D.create(0, 0, self.floorThickness), adsk.fusion.BRepEntityTypes.BRepFaceEntityType)[0]
            #baseExt.body.name = self.boxName
            topSketch = sketches.add(topFace)

            '''
            leftLine = getLineFromCoordinates(topSketch, -self.boxWidth / 2, self.boxLength / 2, self.wallWidth, -self.boxWidth / 2, -self.boxLength / 2, self.wallWidth)
            rightLine = getLineFromCoordinates(topSketch, self.boxWidth / 2, self.boxLength / 2, self.wallWidth, self.boxWidth / 2, -self.boxLength / 2, self.wallWidth)
            topLine = getLineFromCoordinates(topSketch, -self.boxWidth / 2, self.boxLength / 2, self.wallWidth, self.boxWidth / 2, self.boxLength / 2, self.wallWidth)
            bottomLine = getLineFromCoordinates(topSketch, -self.boxWidth / 2, -self.boxLength / 2, self.wallWidth, self.boxWidth / 2, -self.boxLength / 2, self.wallWidth)
            '''

            box = topSketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(-0.1, -0.1, 0),
                adsk.core.Point3D.create(0.1, 0.1, 0) 
            )

            topSketch.sketchDimensions.addDistanceDimension(pointAt(topSketch, -self.boxWidth / 2, self.boxLength / 2, 0), pointAt(topSketch, -0.1, -0.1, 0), 
                                                            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, 
                                                            adsk.core.Point3D.create(-self.boxWidth / 2, self.boxLength /2 , 0)).value = self.wallWidth

            topSketch.sketchDimensions.addDistanceDimension(pointAt(topSketch, -self.boxWidth / 2, self.boxLength / 2, 0), pointAt(topSketch, -self.boxWidth / 2 + self.wallWidth, 0.1, 0), 
                                                            adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, 
                                                            adsk.core.Point3D.create(-self.boxWidth / 2, self.boxLength /2 , 0)).value = self.wallWidth           

        except Exception as e:
            if ui:
                pass
                #ui.messageBox(f'Failed to complete the box. This is most likely because the input values define an invalid box. Error: {e}')

def run(context):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('A Fusion design must be active when running this script.')
            return
        commandDefinitions = ui.commandDefinitions
        #check the command exists or not
        cmdDef = commandDefinitions.itemById('BoxWithLid')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('BoxWithLid',
                    'Create Box with Lid',
                    'Create a box with lid.')

        onCommandCreated = BoxCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

'''
def getLineFromCoordinates(sketch, x1, y1, z1, x2, y2, z2):
    retVal = ((l for l in sketch.sketchCurves.sketchLines if (
        l.startSketchPoint.geometry.x == x1 and 
        l.startSketchPoint.geometry.y == y1 and 
        l.startSketchPoint.geometry.z == z1 and 
        l.endSketchPoint.geometry.x == x2 and 
        l.endSketchPoint.geometry.x == y2 and 
        l.endSketchPoint.geometry.x == z2 
    ) or (
        l.endSketchPoint.geometry.x == x1 and 
        l.endSketchPoint.geometry.y == y1 and 
        l.endSketchPoint.geometry.z == z1 and 
        l.startSketchPoint.geometry.x == x2 and 
        l.startSketchPoint.geometry.x == y2 and 
        l.startSketchPoint.geometry.x == z2
    )), None)
    if retVal == None:
        ui.messageBox('No valid line found!')
    return retVal
'''

def pointAt(sketch, x, y, z):
    retVal = next((l for l in sketch.sketchPoints if 
        l.geometry.x == x and 
        l.geometry.y == y and 
        l.geometry.z == z
    ), None)

    if retVal == None:
        ui.messageBox('No valid point found!')
    # else:
    #     ui.messageBox(f'Point found at: ({retVal.geometry.x}, {retVal.geometry.y}, {retVal.geometry.z})')
    return retVal
