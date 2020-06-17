# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:07:20 2019

@author: gauravi
"""

import vtk
from vtk.util.colors import permanent_red_violet, olive_green_dark, magenta

# Setting the background color as black for all ports
ColorBackground = [0.0, 0.0, 0.0]

# Reading Fuel Oil Heat Exchanger
Fohe = vtk.vtkBYUReader()
Fohe.SetGeometryFileName("fohe.g")
Fohe.Update()

# Retrieving the center and the bounds of fohe 
center = Fohe.GetOutput().GetCenter()
myBounds = Fohe.GetOutput().GetBounds()

normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(Fohe.GetOutputPort())

# Setting the center of the plane to align with the FOHE's center
plane = vtk.vtkPlane()
plane.SetOrigin(center)

# Setting the normal vector to the provided values
plane.SetNormal(0.866, 0.0,-0.5)


#################### Logic for Clipping Data #####################

clipper_obj = vtk.vtkClipPolyData()
clipper_obj.SetInputConnection(normals.GetOutputPort())
clipper_obj.SetClipFunction(plane)
clipper_obj.GenerateClipScalarsOn()
clipper_obj.GenerateClippedOutputOn()
clipper_obj.SetValue(0) # setting clipping value to zero
clip_mapper = vtk.vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper_obj.GetOutputPort())
clip_mapper.ScalarVisibilityOff()
backProp = vtk.vtkProperty()
backProp.SetDiffuseColor(olive_green_dark)
clip_part = vtk.vtkActor()
clip_part.SetMapper(clip_mapper)
clip_part.GetProperty().SetColor(olive_green_dark)
clip_part.SetBackfaceProperty(backProp)

################### End of Logic of Clipping Data #####################



############### Displaying the wireframe of the remaining part of the cut object ################

cutting_Entity = vtk.vtkCutter()
cutting_Entity.SetInputConnection(normals.GetOutputPort())
cutting_Entity.SetCutFunction(plane)
cutting_Entity.GenerateCutScalarsOn()
cutting_Entity.SetValue(0, 0)

cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutting_Entity.GetOutputPort())
cutStrips.Update()

cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

restMapper = vtk.vtkPolyDataMapper()
restMapper.SetInputData(clipper_obj.GetClippedOutput())
restMapper.ScalarVisibilityOff()

remaining_part = vtk.vtkActor()
remaining_part.SetMapper(restMapper)
remaining_part.GetProperty().SetRepresentationToWireframe()

############### End of logic for the remaining part of the cut object ################



############### Displaying the intersection between the plane and polygon data ############

cutting_Entity = vtk.vtkCutter()
cutting_Entity.SetInputConnection(normals.GetOutputPort())
cutting_Entity.SetCutFunction(plane)
cutting_Entity.GenerateCutScalarsOn()
cutting_Entity.SetValue(0, 0)

cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutting_Entity.GetOutputPort())
cutStrips.Update()

cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

triangle_entity = vtk.vtkTriangleFilter()
triangle_entity.SetInputData(cutPoly)

intersected_Mapper = vtk.vtkPolyDataMapper()
intersected_Mapper.SetInputData(cutPoly)
intersected_Mapper.SetInputConnection(triangle_entity.GetOutputPort())

intersected_Area = vtk.vtkActor()
intersected_Area.SetMapper(intersected_Mapper)
intersected_Area.GetProperty().SetColor(magenta)

############### End of logic of intersection between the plane and polygon data ############



############ Displaying the combined clipped out object, remaining section, intersection area and implicit plane ###############################

obj = vtk.vtkImplicitBoolean()
obj.SetOperationTypeToIntersection()
obj.AddFunction(plane)

sample_obj = vtk.vtkSampleFunction()
sample_obj.SetImplicitFunction(obj)
sample_obj.SetModelBounds(myBounds)

countour_obj = vtk.vtkContourFilter()
countour_obj.SetInputConnection(sample_obj.GetOutputPort())
countour_obj.SetValue(0, 0)

combined_Mapper = vtk.vtkPolyDataMapper()
combined_Mapper.SetInputConnection(countour_obj.GetOutputPort())

combined_object = vtk.vtkActor()
combined_object.SetMapper(combined_Mapper)
combined_object.GetProperty().SetColor(magenta)

plane1 = vtk.vtkPlaneSource()
planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(plane1.GetOutputPort())

planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.GetProperty().SetColor(permanent_red_violet)
planeActor.GetProperty().SetOpacity(0.2) # using opacity value 0.2 for rendering implicit plane

############### End of Logic for Displaying Combined Object ################



# View Port 1: Clipped Out Part
ren1 = vtk.vtkRenderer()
ren1.SetViewport(0, 0.5, 0.5, 1)
ren1.SetBackground(ColorBackground)
ren1.AddActor(clip_part) 

# View Port 2: Wireframe Representation of the Remaining Part of FOHE
ren3 = vtk.vtkRenderer()
ren3.SetViewport(0.5, 0.5, 1, 1)
ren3.SetBackground(ColorBackground)
ren3.AddActor(remaining_part) 

# View Port 3: Surface Representation of Intersected Area
ren2 = vtk.vtkRenderer()
ren2.SetViewport(0, 0, 0.5, 0.5)
ren2.SetBackground(ColorBackground)
ren2.AddActor(intersected_Area) 

# View Port 4: Combined Object
ren4 = vtk.vtkRenderer()
ren4.SetViewport(0.5, 0, 1, 0.5)
ren4.SetBackground(ColorBackground)
ren4.AddActor(clip_part)  
ren4.AddActor(intersected_Area) 
ren4.AddActor(remaining_part) 
ren4.AddActor(combined_object) 


# Creating the Render Window and specifying its size 
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1500, 700)


# Rendering all the the scenes in the rendering window
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.AddRenderer(ren3)
renWin.AddRenderer(ren4)
renWin.Render()


# Synchronizing all 4 viewports using camera so that all of them display the same view
ren1.GetActiveCamera().Zoom(1.1)
ren2.SetActiveCamera(ren1.GetActiveCamera())
ren3.SetActiveCamera(ren1.GetActiveCamera())
ren4.SetActiveCamera(ren1.GetActiveCamera())


iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# Exporting the rendered scene to a JPG ﬁle
w2i = vtk.vtkWindowToImageFilter()
w2i.SetInput(renWin)
w2i.Update()
writer = vtk.vtkJPEGWriter()
writer.SetInputConnection(w2i.GetOutputPort())
# Note: This file will be saved in the same location where you place the .py file
writer.SetFileName("JPG_of_Rendered_Scene.jpg")
renWin.Render()
writer.Write()

iren.Initialize()# Initalizing the interactor for the loop 
iren.Start() # Start the event loop


