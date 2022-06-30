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


import cadexchanger.CadExCore as cadex
from base_explorer import BaseExplorer
from surface_explorer import SurfaceExplorer
from curve_explorer import CurveExplorer
from pcurve_explorer import PCurveExplorer

class ShapeExplorer(cadex.ModelData_Model_VoidElementVisitor, BaseExplorer):
    def __init__(self):
        BaseExplorer.__init__(self)
        cadex.ModelData_Model_VoidElementVisitor.__init__(self)

    def VisitPart(self, thePart: cadex.ModelData_Part):
        aBRep = thePart.BRepRepresentation()
        if aBRep:
            print(f"Part = \"{thePart.Name()}\"")
            self.ExploreBRep(aBRep)

    def ExploreBRep(self, theBRep: cadex.ModelData_BRepRepresentation):
        # Get() method retrieves bodies listed in B-Rep representation by calling data providers flushing
        # Flushing isn't an elementary process so it can take a significant time(seconds, minutes depending on a model structure)
        aBodyList = theBRep.Get()

        # Iterate over bodies
        for i, aBody in enumerate(aBodyList):
            print(f"Body {i}: {self.BodyType(aBody)}")
            self.ExploreShape(aBody)


    # Recursive iterating over the Shape until reaching vertices
    def ExploreShape(self, theShape: cadex.ModelData_Shape):
        if theShape.Type() == cadex.ModelData_ST_Face:
            self.myCurrentFace = cadex.ModelData_Face.Cast(theShape)
        self.myNestingLevel += 1
        for aShape in cadex.ModelData_Shape_Iterator(theShape):
            self.PrintShape(aShape)
            self.ExploreShape(aShape)

        if theShape.Type() == cadex.ModelData_ST_Face:
            self.myCurrentFace = None

        self.myNestingLevel -= 1

    # Returns body type name
    def BodyType(self, theBody: cadex.ModelData_Body) -> str:
        if theBody.BodyType() == cadex.ModelData_BT_Solid:
            return "Solid"
        if theBody.BodyType() == cadex.ModelData_BT_Sheet:
            return "Sheet"
        if theBody.BodyType() == cadex.ModelData_BT_Wireframe:
            return "Wireframe"
        if theBody.BodyType() == cadex.ModelData_BT_Acorn:
            return "Acorn"
        return "Undefined"

    # Returns shape type name and prints shape info in some cases
    def PrintShape(self, theShape: cadex.ModelData_Shape):
        self.PrintTabulation()

        if theShape.Type() == cadex.ModelData_ST_Solid:
            print("Solid", end="")
        elif theShape.Type() == cadex.ModelData_ST_Shell:
            self.PrintShell(cadex.ModelData_Shell.Cast(theShape))
        elif theShape.Type() == cadex.ModelData_ST_Wire:
            self.PrintWire(cadex.ModelData_Wire.Cast(theShape))
        elif theShape.Type() == cadex.ModelData_ST_Face:
            self.PrintFace(cadex.ModelData_Face.Cast(theShape))
        elif theShape.Type() == cadex.ModelData_ST_Edge:
            self.PrintEdge(cadex.ModelData_Edge.Cast(theShape))
        elif theShape.Type() == cadex.ModelData_ST_Vertex:
            self.PrintVertex(cadex.ModelData_Vertex.Cast(theShape))
        else:
            print("Undefined", end="")

        print()

    def PrintShell(self, theShell: cadex.ModelData_Shell):
        self.PrintName("Shell")
        self.myNestingLevel += 1
        self.PrintOrientation(theShell.Orientation())
        self.myNestingLevel -= 1

    def PrintWire(self, theWire: cadex.ModelData_Wire):
        self.PrintName("Wire")
        self.myNestingLevel += 1
        self.PrintOrientation(theWire.Orientation())
        self.myNestingLevel -= 1

    def PrintFace(self, theFace: cadex.ModelData_Face):
        self.PrintName("Face")
        self.myNestingLevel += 1
        self.PrintOrientation(theFace.Orientation())
        print()
        aSurface = theFace.Surface()
        self.PrintTabulation()
        print("Surface: ")
        SurfaceExplorer.PrintSurface(aSurface)
        self.myNestingLevel -= 1

    def PrintEdge(self, theEdge: cadex.ModelData_Edge):
        self.PrintName("Edge")
        self.myNestingLevel += 1
        if theEdge.IsDegenerated():
            print("Degenerated: ", end="")
        self.PrintOrientation(theEdge.Orientation())
        self.PrintNamedParameter("Tolerance", theEdge.Tolerance())

        if not theEdge.IsDegenerated():
            aCurve, first, second = theEdge.Curve()
            print()
            self.PrintTabulation()
            self.PrintName("Curve")
            self.PrintRange("Edge Range", first, second)
            CurveExplorer.PrintCurveInfo(aCurve)

        if self.myCurrentFace:
            aPCurve, first, second = theEdge.PCurve(self.myCurrentFace)
            print()
            self.PrintTabulation()
            self.PrintName("PCurve")
            self.PrintRange("Edge Range", first, second)
            PCurveExplorer.PrintPCurveInfo(aPCurve)

        self.myNestingLevel -= 1

    def PrintVertex(self, theVertex:cadex.ModelData_Vertex):
        self.PrintName("Vertex")
        aLoc = theVertex.Point()
        aTolerance = theVertex.Tolerance()
        self.PrintOrientation(theVertex.Orientation())
        self.PrintNamedParameter("Tolerance", aTolerance)
        self.PrintNamedParameter("Location",  aLoc)
