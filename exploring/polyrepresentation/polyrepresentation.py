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

 # Visits directly every part and calls Poly representation exploring if a part has one
class PartPolyVisitor(cadex.ModelData_Model_VoidElementVisitor):
    def VisitPart(self, thePart: cadex.ModelData_Part):
        aPolyRep = thePart.PolyRepresentation(cadex.ModelData_RM_Poly)
        if aPolyRep:
            self.ExplorePoly(aPolyRep)

    # Explores PolyVertexSets of Poly representation
    def ExplorePoly(self, thePoly: cadex.ModelData_PolyRepresentation):
        # Get() method retrieves PolyVertexSets listed in Poly representation by calling data providers flushing
        # Because of internal mechanics providers flushing is faster than for B-Rep representations
        aList = thePoly.Get()

        # Iterate over PolyShape list
        for i, aPVS in enumerate(aList):
            print(f"PolyShape {i}:")
            self.PrintPVSInfo(aPVS)

    # Function to print a PolyVertexSet info
    def PrintPVSInfo(self, thePVS: cadex.ModelData_PolyVertexSet):
        if thePVS.TypeId() == cadex.ModelData_IndexedTriangleSet.GetTypeId():
            print("IndexedTriangleSet type.")
            ITS = cadex.ModelData_IndexedTriangleSet.Cast(thePVS)
            self.DumpTriangleSet(ITS)
        elif thePVS.TypeId() == cadex.ModelData_PolyLineSet.GetTypeId():
            print("PolyLineSet type.")
            PLS = cadex.ModelData_PolyLineSet.Cast(thePVS)
            self.DumpPolyLineSet(PLS)
        elif thePVS.TypeId() == cadex.ModelData_PolyPointSet.GetTypeId():
            print("PolyPointSet type.")
            PPS = cadex.ModelData_PolyPointSet.Cast(thePVS)
            self.DumpPolyPointSet(PPS)
        else:
            print("Undefined type")

    def DumpPolyPointSet(self, thePS: cadex.ModelData_PolyPointSet):
        n = thePS.NumberOfVertices()

        print(f"PolyPoint set contains {n} vertices")
        for i in range(n):
            print(f"Point {i}:")
            print("  Node coordinates:")
            aP = thePS.Coordinate(i)
            print(f"  ({aP.X()}, {aP.Y()}, {aP.Z()})")

    # Prints number of PolyLines and local coordinates for every vertex of each PolyLine
    def DumpPolyLineSet(self, thePLS: cadex.ModelData_PolyLineSet):
        n = thePLS.NumberOfPolyLines()

        print(f"PolyLine set contains {n} PolyLines")
        for i in range(n):
            print(f"PolyLine {i}:")
            print("  Node coordinates:")
            for j in range(thePLS.NumberOfVertices(i)):
                aV = thePLS.Coordinate(i, j)
                print(f"  ({aV.X()}, {aV.Y()}, {aV.Z()})")

    # Prints number of triangles and local data for each node
    # Prints Coords and UV-Coords for each vertex and prints Normals and Colors for each triangle
    def DumpTriangleSet(self, theTS: cadex.ModelData_IndexedTriangleSet):
        n = theTS.NumberOfFaces()

        print(f"Triangle set contains {n} number of faces")
        for i in range(n):
            print(f"Triangle {i}:")
            for j in range(3):
                print(f"  Node {j}:")

                # Coordinates
                aV = theTS.Coordinate(i, j);
                print(f"  Coordinates: ({aV.X()}, {aV.Y()}, {aV.Z()})")

                # UV-coordinates
                if theTS.HasUVCoordinates():
                    aUV = theTS.UVCoordinate(i, j)
                    print(f"  UV Coordinates: ({aUV.X()}, {aUV.Y()})")

                # Normals
                if theTS.HasNormals():
                    aN = theTS.VertexNormal(i, j)
                    print(f"  Normal vector: ({aN.X()}, {aN.Y()}, {aN.Z()})")

                # Colors
                if theTS.HasColors():
                    aColor = theTS.VertexColor(i, j)


def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    # If there is no Poly representation in the model, mesher will compute it
    aMesherParams = cadex.ModelAlgo_BRepMesherParameters()
    aMesherParams.SetGranularity(cadex.ModelAlgo_BRepMesherParameters.Fine)

    aMesher = cadex.ModelAlgo_BRepMesher(aMesherParams)
    aMesher.Compute(aModel)

    # Explore Poly representation of model parts
    aVisitor = PartPolyVisitor()
    aModel.AcceptElementVisitor(aVisitor)

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])
    sys.exit(main(aSource))
