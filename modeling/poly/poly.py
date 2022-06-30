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

def CreatePolyPointSet() -> cadex.ModelData_PolyPointSet:
    aPoints1 = cadex.ModelData_PointList()
    aPoints2 = cadex.ModelData_PointList()

    for i in range(10):
        aPoints1.append(cadex.ModelData_Point(i, 0, 0))
        aPoints2.append(cadex.ModelData_Point(i, 0, i))

    # It's possible to add as much containers of points to same PolyPointSet as you want
    aPPS = cadex.ModelData_PolyPointSet()
    aPPS.Add(aPoints1) # aPPS.NumberOfVertices() == 10
    aPPS.Add(aPoints2) # aPPS.NumberOfVertices() == 20
    return aPPS

# Create PLS from lists of points: each list builds a cadex.PolyLine
def CreatePolyLineSet() -> cadex.ModelData_PolyPointSet:
    aPoints1 = cadex.ModelData_PointList()
    aPoints2 = cadex.ModelData_PointList()

    for i in range(10):
        aPoints1.append(cadex.ModelData_Point(i, 3, i / 2))
        aPoints2.append(cadex.ModelData_Point(i, 0, i % 2))

    # For each cadex.list of points there will be a cadex.PolyLine
    aPLS = cadex.ModelData_PolyLineSet()
    aPLS.AddPolyline(aPoints1) # aPLS.NumberOfPolyLines() == 1
    aPLS.AddPolyline(aPoints2) # aPLS.NumberOfPolyLines() == 2
    return aPLS

# Creates ITS with full information provided
def CreateITS() -> cadex.ModelData_IndexedTriangleSet:
    aCoords = [cadex.ModelData_Point( 1.0,  1.0,  1.0),
               cadex.ModelData_Point(-1.0,  1.0,  1.0),
               cadex.ModelData_Point(-1.0, -1.0,  1.0),
               cadex.ModelData_Point( 1.0, -1.0,  1.0),
               cadex.ModelData_Point( 1.0,  1.0, -1.0),
               cadex.ModelData_Point(-1.0,  1.0, -1.0),
               cadex.ModelData_Point(-1.0, -1.0, -1.0),
               cadex.ModelData_Point( 1.0, -1.0, -1.0)
               ]



    aVerticesIndices = [0, 1, 2, 3, #1
                        1, 0, 4, 5, #2
                        2, 1, 5, 6, #3
                        3, 2, 6, 7, #4
                        0, 3, 7, 4, #5
                        7, 6, 5, 4  #6
                        ]

    aCounts = [ 4, 4, 4, 4, 4, 4 ]

    aNormals = [cadex.ModelData_Vectorf( 0,  0,  1),
                cadex.ModelData_Vectorf( 0,  1,  0),
                cadex.ModelData_Vectorf(-1,  0,  0),
                cadex.ModelData_Vectorf( 0, -1,  0),
                cadex.ModelData_Vectorf( 1,  0,  0),
                cadex.ModelData_Vectorf( 0,  0, -1)
                ]

    aNormalsIndices = [0, 0, 0, 0, #1
                       1, 1, 1, 1, #2
                       2, 2, 2, 2, #3
                       3, 3, 3, 3, #4
                       4, 4, 4, 4, #5
                       5, 5, 5, 5  #6
                       ]

    aColors = [cadex.ModelData_Color(255,   0,   0),
               cadex.ModelData_Color(  0, 255,   0),
               cadex.ModelData_Color(  0,   0, 255),
               cadex.ModelData_Color(255, 255,   0),
               cadex.ModelData_Color(  0, 255, 255),
               cadex.ModelData_Color(255, 255, 255)
               ]

    aColorIndices = [0, 0, 0, 0, #1
                     1, 1, 1, 1, #2
                     2, 2, 2, 2, #3
                     3, 3, 3, 3, #4
                     4, 4, 4, 4, #5
                     5, 5, 5, 5  #6
                     ]

    anITS = cadex.ModelData_IndexedTriangleSet()
    anITS.AddCoordinates(aCoords, aVerticesIndices, aCounts)
    anITS.AddNormals(aNormals, aNormalsIndices, aCounts)
    anITS.AddColors(aColors, aColorIndices, aCounts)
    return anITS

def main():
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1
    # Create PolyPointSet and explore it
    aPPS = CreatePolyPointSet()

    # Create PolyLineSet and explore it
    aPLS = CreatePolyLineSet()

    # Create IndexedTriangleSet and explore it
    anITS = CreateITS()

    aPolyWithPPS = cadex.ModelData_PolyRepresentation(aPPS)
    aPolyWithPLS = cadex.ModelData_PolyRepresentation(aPLS)
    aPolyWithITS = cadex.ModelData_PolyRepresentation(anITS)

    aPart = cadex.ModelData_Part()

    aPart.AddRepresentation(aPolyWithPPS)
    aPart.AddRepresentation(aPolyWithPLS)
    aPart.AddRepresentation(aPolyWithITS)

    aModel = cadex.ModelData_Model()
    aModel.AddRoot(aPart)
    cadex.ModelData_ModelWriter().Write(aModel, cadex.Base_UTF16String("out/Poly.xml"))

    print("Completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
