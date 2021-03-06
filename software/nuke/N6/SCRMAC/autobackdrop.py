# autobackdrop.py
# Conversion to Python by michael@yawpitchroll.com
# Derived from a TCL original by frank@beingfrank.info [last modified 10.01.2006]
# Creates a backdrop node that automatically encompasses all selected nodes and has a random color
# Python version last midified 03.04.2008

"""
AutoBackDrop for Nuke:
Creates a Backdrop node that automatically encompasses all selected nodes
and assigns a random color to the Backdrop.
"""

import nuke
import nukescripts
from random import randint

def AutoBackDrop():
    """
    Creates a backdrop node with a random color between minCol and maxCol.
    Allows some customization to the border around the selected nodes by
    modification of some in-file variables.  Also allows the user to set
    a boolean to decide if they want the Backdrop non-stick (allows backdrop
    to be repositioned without moving nodes, will have to click on the DAG
    to 'stick' nodes to backdrop) or sticky (backdrop automatically de-
    selected, nodes 'stuck' to backdrop (similar to using the Group
    command in Shake as an organization Backdrop).
    """

# -----> BEGIN USER CUSTOMIZATION <-----
# minCol and maxCol restrict color range
# 1 (full black) to 109951162776 (full white)

    minCol = 1
    maxCol = 1099511627776

# leftBord, rightBord, topBord, and bottomBord define the border width of the backdrop from
# the left-most, right-most, top-most, and bottom-most nodes (respectively).  Positive integers
# will expand the border from default, while negative integers will shrink it.

    leftBord = 0
    rightBord = 0
    topBord = 0
    bottomBord = 0

# nonStick defines the "sticky" behavior of the encompassed nodes when
# the backdrop is built.  If 'true' the nodes will not be 'sticky' and
# user will have to click on elsewhere on the DAG to 'activate' the backdrop
# (same as normal Backdrop behavior).  If 'false' the nodes will 'stick' as
# soon as the AutoBackDrop is created.  Default is 'false'

    nonStick = False

# -----> END USER CUSTOMIZATION <-----


#Check for selected nodes, create simple backdrop if empty, else create autobackdrop
    selection = nuke.selectedNode()

    if selection is None:
        bd = nuke.createNode("BackdropNode")
        bd.knob("tile_color").setValue(randint(minCol, maxCol))
        bd.knob("selected").setValue(True)
        return
    
    selection = nuke.selectedNodes()

    #Find the extreme X and Y positions of the selected nodes
    curX = set([i.knob("xpos").value() for i in selection if i.Class()!="BackdropNode"])
    curY = set([i.knob("ypos").value() for i in selection if i.Class()!="BackdropNode"])

    bdropX = set([i.knob("xpos").value() for i in selection if i.Class()=="BackdropNode"])
    bdropY = set([i.knob("ypos").value() for i in selection if i.Class()=="BackdropNode"])
    bdropW = set([(i.knob("bdwidth").value() + i.knob("xpos").value()) for i in selection if i.Class()=="BackdropNode"])
    bdropT = set([(i.knob("bdheight").value() + i.knob("ypos").value()) for i in selection if i.Class()=="BackdropNode"])
            
    minX = min(curX|bdropX)
    minY = min(curY|bdropY)

    curX = set([(i+120) for i in curX])
    bdropW = set([(i + 40) for i in bdropW])
    
    maxX = max(curX|bdropW)

    curY = set([(i+120) for i in curY])
    bdropT = set([(i + 56) for i in bdropT])
    
    maxY = max(curY|bdropT)
    
#Create BackDrop encompassing all selected nodes and assign random color to Backdrop
    bd = nuke.createNode("BackdropNode")
    bd.knob("xpos").setValue(minX-(20+leftBord))
    bd.knob("ypos").setValue(minY-(30+topBord))
    bd.knob("bdwidth").setValue((maxX-minX)+(rightBord))
    bd.knob("bdheight").setValue((maxY-minY)+(bottomBord))
    bd.knob("selected").setValue(nonStick)
    bd.knob("note_font_size").setValue(20)
    bd.knob("note_font").setValue("Verdana Bold Bold Bold Bold Bold Bold Bold Bold Bold")
    