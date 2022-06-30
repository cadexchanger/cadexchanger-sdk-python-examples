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
import cadexchanger.CadExMesh as mesh

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license

import math


# Visits directly every part and calls Poly representation exploring if a part has one
class PartVisitor(cadex.ModelData_Model_VoidElementVisitor):
    def __init__ (self):
        super().__init__()

    def VisitPart(self, thePart: cadex.ModelData_Part):
        # We need to get last poly representation because if model already
        # has poly representation, new representation with BRep-To-Poly associations
        # will be added to the end of representation list.
        aLastPolyRep = cadex.ModelData_PolyRepresentation()

        for aRep in thePart.GetRepresentationIterator():
            if aRep.TypeId() == cadex.ModelData_PolyRepresentation.GetTypeId():
                aLastPolyRep = cadex.ModelData_PolyRepresentation.Cast (aRep)

        self.ExplorePoly (aLastPolyRep)
        self.ExploreBRep (thePart.BRepRepresentation(), aLastPolyRep)

    def ExploreShape(self,
                     theShape: cadex.ModelData_Shape,
                     thePolyRep: cadex.ModelData_PolyRepresentation):
        aFaceIt = cadex.ModelData_Shape_Iterator(theShape, cadex.ModelData_ST_Face)
        anFCounter = 0
        for aFaceShape in aFaceIt:
            aFace = cadex.ModelData_Face.Cast (aFaceShape)
            anITS = thePolyRep.Triangulation (aFace)
            if not anITS:
                continue
            print(f"ITS {anFCounter} has: {anITS.NumberOfVertices()} vertices.")

            anECounter = 0
            anEdgeIt = cadex.ModelData_Shape_Iterator(aFaceShape, cadex.ModelData_ST_Edge)
            for anEdgeShape in anEdgeIt:
                anEdge = cadex.ModelData_Edge.Cast (anEdgeShape)
                aPLS = thePolyRep.PolyLine (anEdge)
                print(f"PLS {anFCounter}-{anECounter} has: {aPLS.NumberOfVertices()} vertices.")
                anECounter += 1

            anFCounter += 1

    def ExploreBRep(self,
                    theBRep: cadex.ModelData_BRepRepresentation,
                    thePolyRep: cadex.ModelData_PolyRepresentation):
        aBodyList = theBRep.Get()
        for aBody in aBodyList:
            self.ExploreShape (aBody, thePolyRep)

    def ExplorePoly(self, thePolyRep: cadex.ModelData_PolyRepresentation):
        aPolyShapeList = thePolyRep.Get()

        for i, aPolyShape in enumerate(aPolyShapeList):
            aSourceShape = thePolyRep.SourceShape (aPolyShape)
            if not aSourceShape:
                continue
            if aSourceShape.Type() == cadex.ModelData_ST_Face:
                aFace = cadex.ModelData_Face.Cast (aSourceShape)
                print(f"Poly shape on position {i}", end="")
                if aFace.Surface().Type() == cadex.ModelData_ST_BSpline:
                    print(" was generated from b-spline.")
                else:
                    print(" wasn't generated from b-spline.")


def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    # Set up mesher and parameters
    aParam = cadex.ModelAlgo_BRepMesherParameters()
    aParam.SetAngularDeflection(math.pi * 10 / 180)
    aParam.SetChordalDeflection(0.003)
    aParam.SetSaveBRepToPolyAssociations(True)

    aMesher = cadex.ModelAlgo_BRepMesher(aParam)
    aMesher.Compute(aModel, True)

    # Explore model:
    aVisitor = PartVisitor()
    aModel.AcceptElementVisitor(aVisitor)

    # Save the result
    if not cadex.ModelData_ModelWriter().Write(aModel, cadex.Base_UTF16String("out/VisMesher.xml")):
        print("Unable to save the model")
        return 1

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])

    sys.exit(main(aSource))
