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
import math

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license


def main():
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    # Extrusion
    # Edge to Face
    anExtrusionLine = cadex.ModelData_Line(cadex.ModelData_Point(-2.0, 0.0, -4.0), cadex.ModelData_Direction.XDir())
    anExtrusionEdge = cadex.ModelData_Edge(anExtrusionLine, 0.0, 4.0)
    aPlane = cadex.ModelAlgo_BRepFeatures.CreateExtrusion(anExtrusionEdge, cadex.ModelData_Vector(0.0, 4.0, 0.0))

    # Face to Solid
    aBlock = cadex.ModelAlgo_BRepFeatures.CreateExtrusion(aPlane, cadex.ModelData_Vector(0.0, 0.0, 8.0))

    # Revolution
    # Edge to Face
    aRevolutionLine = cadex.ModelData_Line(cadex.ModelData_Point(10.0, 0.0, 0.0), cadex.ModelData_Direction.ZDir())
    aRevolutionEdge = cadex.ModelData_Edge(aRevolutionLine, 1.0, 3.0)
    aCircularPlane = cadex.ModelAlgo_BRepFeatures.CreateRevolution(aRevolutionEdge,
        cadex.ModelData_Axis1Placement(cadex.ModelData_Point(10.0, 0.0, 0.0),
        cadex.ModelData_Direction.YDir()), math.pi * 2)
    # Face to Solid
    aTunnel = cadex.ModelAlgo_BRepFeatures.CreateRevolution(aCircularPlane, cadex.ModelData_Axis1Placement.OZ(), math.pi)

    # Create a model
    aModel = cadex.ModelData_Model()
    aBRepB = cadex.ModelData_BRepRepresentation(aBlock)
    anExtrusionPart = cadex.ModelData_Part(aBRepB, cadex.Base_UTF16String("Block"))
    aModel.AddRoot(anExtrusionPart)

    aBRepT = cadex.ModelData_BRepRepresentation(aTunnel)
    aRevolutionPart = cadex.ModelData_Part(aBRepT, cadex.Base_UTF16String("Tunnel"))
    aModel.AddRoot(aRevolutionPart)

    aWriter = cadex.ModelData_ModelWriter()

    # Save the result
    if not aWriter.Write(aModel, cadex.Base_UTF16String("out/Features.xml")):
        print("Unable to save the model!")
        return 1

    print("Completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
