#!/usr/bin/env python3

# $Id$

# Copyright (C) 2008-2014, Roman Lygin. All rights reserved.
# Copyright (C) 2014-2022, CADEX. All rights reserved.

# This file is part of the CAD Exchanger software.

# You may use this file under the terms of the BSD license as follows:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import sys
from pathlib import Path
import os

import cadexchanger.CadExCore as cadex

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license
import math

def MakeDirection(theVector: cadex.ModelData_Vector) -> cadex.ModelData_Direction:
    aVector = theVector.Normalized()
    return cadex.ModelData_Direction(aVector.X(), aVector.Y(), aVector.Z())

def MakeCircularFace(thePos: cadex.ModelData_Point,
                     theDir: cadex.ModelData_Direction,
                     theBoundary: cadex.ModelData_Edge) -> cadex.ModelData_Face:
    a3Axis = cadex.ModelData_Axis3Placement(thePos, theDir, cadex.ModelData_Direction.XDir())
    aPlane = cadex.ModelData_Plane(a3Axis)
    aFace = cadex.ModelData_Face(aPlane)
    aWire = cadex.ModelData_Wire(theBoundary)
    aFace.Append(aWire)
    return aFace

def MakeCircularFaceWithInnerWire(thePos: cadex.ModelData_Point,
                                  theDir: cadex.ModelData_Direction,
                                  theInner: cadex.ModelData_Edge,
                                  theOuter: cadex.ModelData_Edge) -> cadex.ModelData_Face:
    a3Axis = cadex.ModelData_Axis3Placement(thePos, theDir, cadex.ModelData_Direction.XDir())
    aPlane = cadex.ModelData_Plane(a3Axis)
    aFace = cadex.ModelData_Face(aPlane)

    anInner = cadex.ModelData_Wire(theInner)
    anOuter = cadex.ModelData_Wire(theOuter)
    aFace.Append(anInner)
    aFace.Append(anOuter)
    return aFace

def MakeCylindricalFace(thePos: cadex.ModelData_Point,
                        theDir: cadex.ModelData_Direction,
                        theRadius: cadex.ModelData_Direction,
                        theLength: float):
    a3Axis = cadex. ModelData_Axis3Placement(thePos, theDir, cadex.ModelData_Direction.XDir())
    aSurface = cadex.ModelData_CylindricalSurface(a3Axis, theRadius)
    aFace = cadex.ModelData_Face(aSurface, 0, math.pi * 2, 0, theLength)

    theTopEdge = None
    theBottomEdge = None
    # Get outer edges
    aWire = aFace.OuterWire()
    anIt = cadex.ModelData_Shape_Iterator(aWire, cadex.ModelData_ST_Edge)
    while anIt.HasNext():
        anEdge = cadex.ModelData_Edge.Cast(anIt.Next())
        aP1 = anEdge.EndVertex().Point()
        aP2 = anEdge.StartVertex().Point()
        if aP1.IsEqual(aP2, cadex.ModelData_Vertex(aP2).Tolerance()):
            # The edge is closed
            if aP1.Z() == (theLength * theDir.Z()):
                theTopEdge = anEdge
            else:
                theBottomEdge = anEdge

    return aFace, theTopEdge, theBottomEdge


def CreateNut(theRadius: float) -> cadex.ModelData_Part:
    aNutA = theRadius * 2
    aNutB = theRadius * 1.5
    aHeight = theRadius / 2

    anInitPosition = cadex.ModelData_Point(0.0, 0.0, -aHeight / 2)
    a2Axis = cadex.ModelData_Axis2Placement(anInitPosition, cadex.ModelData_Direction.ZDir(), cadex.ModelData_Direction.XDir())
    a3Axis = cadex.ModelData_Axis3Placement(a2Axis)

    aPlane = cadex.ModelData_Plane(a3Axis)
    aFace = cadex.ModelData_Face(aPlane, -aNutA, aNutA, -aNutB, aNutB)

    aCircle = cadex.ModelData_Circle(a2Axis, theRadius)
    anEdge = cadex.ModelData_Edge(aCircle)
    anInnerWire = cadex.ModelData_Wire(anEdge)
    aFace.Append(cadex.ModelData_Wire.Cast(anInnerWire.Reversed()))

    aNutShape = cadex.ModelAlgo_BRepFeatures.CreateExtrusion(aFace, cadex.ModelData_Vector(0.0, 0.0, aHeight))

    # Add red color
    aColor = cadex.ModelData_Color(255, 0, 0)
    anApp = cadex.ModelData_Appearance(aColor)

    aBRep = cadex.ModelData_BRepRepresentation(aNutShape)
    aBRep.SetAppearance(aNutShape, anApp)

    aNut = cadex.ModelData_Part(aBRep, cadex.Base_UTF16String("Nut"))
    return aNut

def CreateBolt(theRadius: float) -> cadex.ModelData_Part:
    aMajorRadius = theRadius * 1.3
    aLongLength = theRadius * 6
    aShortLength = theRadius / 2

    # Cylindrical faces and their edges

    aFace1, aTopEdge, aMiddleOuterEdge = MakeCylindricalFace(cadex.ModelData_Point(0.0, 0.0, 0.0), cadex.ModelData_Direction.ZDir(),
                                                    aMajorRadius, aShortLength)

    aFace2, aBottomEdge, aMiddleInnerEdge = MakeCylindricalFace(cadex.ModelData_Point(0.0, 0.0, 0.0), cadex.ModelData_Direction(0.0, 0.0, -1.0),
                                                    theRadius, aLongLength)

    # Top circle
    aFace3 = MakeCircularFace(cadex.ModelData_Point(0.0, 0.0, aShortLength), cadex.ModelData_Direction.ZDir(),
                                                cadex.ModelData_Edge.Cast(aTopEdge.Reversed()))

    # Face 4 with inner wire
    aFace4 = MakeCircularFaceWithInnerWire(cadex.ModelData_Point(0.0, 0.0, 0.0), cadex.ModelData_Direction(0.0, 0.0, -1.0),
                                                            cadex.ModelData_Edge.Cast(aMiddleInnerEdge.Reversed()),
                                                            cadex.ModelData_Edge.Cast(aMiddleOuterEdge.Reversed()))

    # Bottom circle
    aFace5 = MakeCircularFace(cadex.ModelData_Point(0.0, 0.0, -aLongLength), cadex.ModelData_Direction(0.0, 0.0, -1.0),
                                                cadex.ModelData_Edge.Cast(aBottomEdge.Reversed()))

    aShell = cadex.ModelData_Shell(aFace1)
    aShell.Append(aFace2)
    aShell.Append(aFace3)
    aShell.Append(aFace4)
    aShell.Append(aFace5)

    aSolid = cadex.ModelData_Solid(aShell)

    # Add blue color
    aColor = cadex.ModelData_Color(0, 0, 255)
    anApp = cadex.ModelData_Appearance(aColor)

    aBRep = cadex.ModelData_BRepRepresentation(aSolid)
    aBRep.SetAppearance(aSolid, anApp)

    aBolt = cadex.ModelData_Part(aBRep, cadex.Base_UTF16String("Bolt"))
    return aBolt

def CreateNutBoltAssembly(theNut: cadex.ModelData_Part,
                          theBolt: cadex.ModelData_Part,
                          theDistance: float) -> cadex.ModelData_Assembly:
    aNutTrsf = cadex.ModelData_Transformation(cadex.ModelData_Vector(0.0, 0.0, 0.0))
    aBoltTrsf = cadex.ModelData_Transformation(cadex.ModelData_Vector(0.0, 0.0, -theDistance))

    aNutBoltAssembly = cadex.ModelData_Assembly(cadex.Base_UTF16String("nut-bolt-assembly"))
    aNutBoltAssembly.AddInstance(theNut, aNutTrsf)
    aNutBoltAssembly.AddInstance(theBolt, aBoltTrsf)
    return aNutBoltAssembly


def main():
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    # Initial Parameters
    aRadius = 0.8

    aPos = [cadex.ModelData_Vector(aRadius * -2, aRadius * 1.5, 0.0),
            cadex.ModelData_Vector(aRadius * 2, aRadius * 1.5, 0.0),
            cadex.ModelData_Vector(aRadius * 0, aRadius * 4.5, 0.0)]

    # Create shapes
    aNut = CreateNut(aRadius)
    aBolt = CreateBolt(aRadius)

    # Create assemblies
    aNutBoltAssembly = CreateNutBoltAssembly(aNut, aBolt, -aRadius * 4.5)

    # Create a model and fill its roots
    aModel = cadex.ModelData_Model()

    # Transformations
    for i in range(len(aPos)):
        anAssemblyTrsf = cadex.ModelData_Transformation(aPos[i])
        anInstance = cadex.ModelData_Instance(aNutBoltAssembly, anAssemblyTrsf, cadex.Base_UTF16String("Nut-Bolt Assembly"))
        aModel.AddRoot(anInstance)

    aWriter = cadex.ModelData_ModelWriter()
    aWriter.Write(aModel, cadex.Base_UTF16String("out/assembly.xml"))

    print("Completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
