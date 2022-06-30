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


class PartBRepVisitor(cadex.ModelData_Model_VoidElementVisitor):
    def __init__(self):
        super().__init__()
        self.myNestingLevel = 0
        self.myShapeSet = set()

    def PrintUniqueShapesCount(self):
        print()
        print(f"Total unique shapes count: {len(self.myShapeSet)}")

    def VisitPart(self, thePart: cadex.ModelData_Part):
        aBRep = thePart.BRepRepresentation()
        if aBRep:
            self.ExploreBRep(aBRep)

    def ExploreBRep(self, theBRep: cadex.ModelData_BRepRepresentation):
        # Get() method retrieves bodies listed in B-Rep representation by calling data providers flushing
        # Flushing isn't an elementary process so it can take a significant time (seconds, minutes depending on a model structure)
        aBodyList = theBRep.Get()

        for i, aBody in enumerate(aBodyList):
            print("Body ", i, ": -type ", self.PrintBodyType(aBody))
            self.ExploreShape(aBody)


    # Recursive iterating over the Shape until reaching vertices
    def ExploreShape(self, theShape: cadex.ModelData_Shape):
        self.myShapeSet.add(theShape)
        self.myNestingLevel += 1
        for aShape in theShape.GetIterator():
            self.PrintShapeInfo(aShape)
            self.ExploreShape(aShape)

        self.myNestingLevel -= 1

    # Returns body type name
    def PrintBodyType(self, theBody: cadex.ModelData_Body) -> str:
        aType = theBody.BodyType()
        if aType == cadex.ModelData_BT_Solid:
            return "Solid"
        if aType ==  cadex.ModelData_BT_Sheet:
            return "Sheet"
        if aType == cadex.ModelData_BT_Wireframe:
            return "Wireframe"
        if aType == cadex.ModelData_BT_Acorn:
            return "Acorn"
        return "Undefined"

    # Prints shape type name and prints shape info in some cases
    def PrintShapeInfo(self, theShape: cadex.ModelData_Shape) -> str:
        self.PrintTabulation()

        aType = theShape.Type()
        if aType == cadex.ModelData_ST_Body:
            print("Body", end="")
        elif aType == cadex.ModelData_ST_Solid:
            print("Solid", end="")
        elif aType == cadex.ModelData_ST_Shell:
            print("Shell", end="")
        elif aType == cadex.ModelData_ST_Wire:
            print("Wire", end="")
            self.PrintWireInfo(cadex.ModelData_Wire.Cast(theShape))
        elif aType == cadex.ModelData_ST_Face:
            print("Face", end="")
            self.PrintFaceInfo(cadex.ModelData_Face.Cast(theShape))
        elif aType == cadex.ModelData_ST_Edge:
            print("Edge", end="")
            self.PrintEdgeInfo(cadex.ModelData_Edge.Cast(theShape))
        elif aType == cadex.ModelData_ST_Vertex:
            print("Vertex", end="")
            self.PrintVertexInfo(cadex.ModelData_Vertex.Cast(theShape))
        else:
            print("Undefined", end="")

        print()


    def PrintOrientationInfo(self, theShape: cadex.ModelData_Shape):
        print(". Orientation: ", end="")
        anOrientation = theShape.Orientation()
        if anOrientation == cadex.ModelData_SO_Forward:
            print("Forward", end="")
        elif anOrientation == cadex.ModelData_SO_Reversed:
            print("Reversed", end="")

    def PrintWireInfo(self, theWire: cadex.ModelData_Wire):
        self.myNestingLevel += 1
        self.PrintOrientationInfo(theWire)
        self.myNestingLevel -= 1

    def PrintFaceInfo(self, theFace: cadex.ModelData_Face):
        self.myNestingLevel += 1
        self.PrintOrientationInfo(theFace)
        print()
        aSurface = theFace.Surface()
        self.PrintTabulation()
        print(f"Surface: {self.PrintSurfaceType(aSurface)}", end="")
        self.myNestingLevel -= 1

    def PrintSurfaceType(self, theSurface: cadex.ModelData_Surface) -> str:
        aType = theSurface
        if aType == cadex.ModelData_ST_Plane:
            return "Plane"
        if aType == cadex.ModelData_ST_Cylinder:
            return "Cylinder"
        if aType == cadex.ModelData_ST_Cone:
            return "Cone"
        if aType == cadex.ModelData_ST_Sphere:
            return "Sphere"
        if aType == cadex.ModelData_ST_Torus:
            return "Torus"
        if aType == cadex.ModelData_ST_LinearExtrusion:
            return "LinearExtrusion"
        if aType == cadex.ModelData_ST_Revolution:
            return "Revolution"
        if aType == cadex.ModelData_ST_Bezier:
            return "Bezier"
        if aType == cadex.ModelData_ST_BSpline:
            return "BSpline"
        if aType == cadex.ModelData_ST_Offset:
            return "Offset"
        if aType == cadex.ModelData_ST_Trimmed:
            return "Trimmed"
        return "Undefined"

    def PrintEdgeInfo(self, theEdge: cadex.ModelData_Edge):
        self.myNestingLevel += 1
        if theEdge.IsDegenerated():
            print("(Degenerated)", end="")
        self.PrintOrientationInfo(theEdge)
        print(f". Tolerance {theEdge.Tolerance()}", end="")

        if not theEdge.IsDegenerated():
            print()
            aCurve, aParamFirst, aParamLast = theEdge.Curve()
            self.PrintTabulation()
            print(f"Curve: {self.PrintCurveType(aCurve)}", end="")

        self.myNestingLevel -= 1

    def PrintCurveType(self, theCurve: cadex.ModelData_Curve) -> str:
        aType = theCurve.Type()
        if aType == cadex.ModelData_CT_Line:
            return "Line"
        if aType == cadex.ModelData_CT_Circle:
            return "Circle"
        if aType == cadex.ModelData_CT_Ellipse:
            return "Ellipse"
        if aType == cadex.ModelData_CT_Hyperbola:
            return "Hyperbola"
        if aType == cadex.ModelData_CT_Parabola:
            return "Parabola"
        if aType == cadex.ModelData_CT_Bezier:
            return "Bezier"
        if aType == cadex.ModelData_CT_BSpline:
            return "BSpline"
        if aType == cadex.ModelData_CT_Offset:
            return "Offset"
        if aType == cadex.ModelData_CT_Trimmed:
            return "Trimmed"
        return "Undefined"

    def PrintVertexInfo(self, theVertex: cadex.ModelData_Vertex):
        self.PrintOrientationInfo(theVertex)
        print(f". Tolerance {theVertex.Tolerance()}", end="")

    def PrintTabulation(self):
        print("- " * self.myNestingLevel, end="")


def main(theSource:str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    # Explore B-Rep representation of model parts
    aVisitor = PartBRepVisitor()
    aModel.AcceptElementVisitor(aVisitor)

    aVisitor.PrintUniqueShapesCount()

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])
    sys.exit(main(aSource))