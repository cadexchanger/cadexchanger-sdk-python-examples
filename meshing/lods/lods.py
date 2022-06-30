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

def NumberOfTriangles(thePoly: cadex.ModelData_PolyRepresentation) -> int:
    trianglesNB = 0

    aList = thePoly.Get()
    for aPVS in aList:
        if aPVS.TypeId() == cadex.ModelData_IndexedTriangleSet.GetTypeId():
            anITS = cadex.ModelData_IndexedTriangleSet.Cast(aPVS)
            trianglesNB += anITS.NumberOfFaces()
    return trianglesNB

def CreateSphereBRep(thePosition: cadex.ModelData_Point, theRadius: float) -> cadex.ModelData_BRepRepresentation:
    aSphere = cadex.ModelAlgo_TopoPrimitives.CreateSphere(thePosition, theRadius)
    aBody = cadex.ModelData_Body.Create(aSphere)
    aBRep = cadex.ModelData_BRepRepresentation(aBody)
    return aBRep

def AddPolyToPart(thePart: cadex.ModelData_Part, theLOD):
    aBRep = thePart.BRepRepresentation()
    aParam = cadex.ModelAlgo_BRepMesherParameters(theLOD)
    aMesher = cadex.ModelAlgo_BRepMesher(aParam)

    aPoly = aMesher.Compute(aBRep)

    thePart.AddRepresentation(aPoly)
    print(f"A polygonal representation with {NumberOfTriangles(aPoly)} triangles has been added");


def main():
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aBRep = CreateSphereBRep(cadex.ModelData_Point(0.0, 0.0, 0.0), 10)
    aPart = cadex.ModelData_Part(aBRep, cadex.Base_UTF16String("Sphere"))

    AddPolyToPart(aPart, cadex.ModelAlgo_BRepMesherParameters.Coarse)
    AddPolyToPart(aPart, cadex.ModelAlgo_BRepMesherParameters.Medium)
    AddPolyToPart(aPart, cadex.ModelAlgo_BRepMesherParameters.Fine)

    aModel = cadex.ModelData_Model()
    aModel.AddRoot(aPart)

    if not cadex.ModelData_ModelWriter().Write(aModel, cadex.Base_UTF16String("out/SphereWithLODs.xml")):
        print("Unable to save the model")
        return 1

    print("Completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())