# Implicit_Functions_and_Cropping


The aim of this short assignment is to use a plane to clip a polygonal data, and display the clipped out and remaining parts of the data. It also shows the plane and its intersection with the polygonal data in visualization toolkit.


## Getting Started


The following instructions shall ensure that the assignment is up and running on your local machine for
development and testing purposes. See ‘Running the tests’ section to know how to run the assignment.


## Prerequisites


Software Required: Python 2.7 (Anaconda3 2018.12 64 bit) for Windows 10 as IDE
Package Required : vtk 8.1.0
Fohe.g input file that has been provided


## Installation


* Follow the instructions in the documentation https://docs.anaconda.com/anaconda/install/windows/
for downloading Python version 2.7 for Anaconda 2018.12 for Windows Installer.
* After launching the Anaconda Navigator, create a new environment for running vtk programs
by referring to the following documentation:
https://docs.anaconda.com/anaconda/navigator/tutorials/manage-environments/#creating-a-new-environ
ment
* Import vtk, numpy and scipy packages into this newly created environment by following the
guidelines specified in:
https://docs.anaconda.com/anaconda/navigator/tutorials/manage-packages/#installing-a-package
* In the Anaconda Navigator, click ‘Home’ on the left panel, then choose the newly created
environment for running the vtk programs from the drop down provided under ‘Applications on’ located
on the top most section of the navigator.
* Click on the ‘Install’ button under Spyder. On completing the installation click the ‘Launch’ button
under it.


## Running the tests


Upon launching the spyder application, copy paste the code from assignment3_code.py file and save it
on your local machine. Now run the code by clicking the green play button provided in the title bar of the
application. Once you get the output pop-up use your mouse rotator to zoom-in and zoom out. Click on
any object and rotate it in different directions.


## Expected Successful Test Results: 

You would see a visualization pop up window with black background and four different view ports. 
The first viewport shall demonstrate an image after clipping out a part, second viewport will show 
the remaining part and the third view port will have just the
intersection part and the last one will have all objects from the first three viewports along with the
clipping plane. All 4 objects can be rotated in this window in such a way that they all move in a
synchronized orientation and face in the same direction because of camera calibration. A jpg file of the
rendered scene will also be saved in the same location as the python file.
You would see a 3D representation of the below scene in vtk on running my code.

Fig: Viewport 1 indicates clipped out part; Viewport 2 indicates remaining part; Viewport 3 indicates intersection
area and Viewport 4 indicates the combination of all the three ports with a clipping plane
Please note that I have commented and explained the entire code implementation in my source code
assignment3_code.py


## References


[1] https://vtk.org/doc/nightly/html/annotated.html
[2] https://github.com/Kitware/VTK
