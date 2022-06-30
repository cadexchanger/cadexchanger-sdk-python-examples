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


def AttachPrimitiveToModel(theName: str, thePrimitive: cadex.ModelData_Solid, theModel: cadex.ModelData_Model):
    aPart = cadex.ModelData_Part(cadex.ModelData_BRepRepresentation(thePrimitive), cadex.Base_UTF16String(theName))
    theModel.AddRoot(aPart)


def CreateBox(thePosition: cadex.ModelData_Point,
              Dx: float,
              Dy: float,
              Dz: float,
              theModel: cadex.ModelData_Model):
    aBox = cadex.ModelAlgo_TopoPrimitives.CreateBox(thePosition, Dx, Dy, Dz)
    AttachPrimitiveToModel("Box", aBox, theModel)

def CreateSphere(thePosition: cadex.ModelData_Point,
                 theRadius: float,
                 theModel: cadex.ModelData_Model):
    aSphere = cadex.ModelAlgo_TopoPrimitives.CreateSphere(thePosition, theRadius)
    AttachPrimitiveToModel("Sphere", aSphere, theModel)

def CreateCylinder(thePosition: cadex.ModelData_Point,
                   theRadius: float,
                   theHeight: float,
                   theModel: cadex.ModelData_Model):

    anAxis = cadex.ModelData_Axis2Placement(thePosition, cadex.ModelData_Direction.ZDir(), cadex.ModelData_Direction.YDir())
    aCylinder = cadex.ModelAlgo_TopoPrimitives.CreateCylinder(anAxis, theRadius, theHeight)
    AttachPrimitiveToModel("Cylinder", aCylinder, theModel)


def CreateCone(thePosition: cadex.ModelData_Point,
               theRadius1: float,
               theRadius2: float,
               theHeight: float,
               theModel: cadex.ModelData_Model):
    anAxis = cadex.ModelData_Axis2Placement(thePosition, cadex.ModelData_Direction.ZDir(), cadex.ModelData_Direction.YDir())
    aCone = cadex.ModelAlgo_TopoPrimitives.CreateCone(anAxis, theRadius1, theRadius2, theHeight)
    AttachPrimitiveToModel("Cone", aCone, theModel)

def CreateTorus(thePosition: cadex.ModelData_Point,
                theMinRadius: float,
                theMaxRadius: float,
                theModel: cadex.ModelData_Model):
    anAxis = cadex.ModelData_Axis2Placement(thePosition, cadex.ModelData_Direction.ZDir(), cadex.ModelData_Direction.YDir())
    aTorus = cadex.ModelAlgo_TopoPrimitives.CreateTorus(anAxis, theMaxRadius, theMinRadius)
    AttachPrimitiveToModel("Torus", aTorus, theModel)


def main():
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    CreateBox(cadex.ModelData_Point(10.0, 0.0, 0.0), 8.0, 8.0, 8.0, aModel)

    CreateSphere(cadex.ModelData_Point(0.0, 10.0, 0.0), 4.0, aModel)

    CreateCylinder(cadex.ModelData_Point(-10.0, 0.0, 0.0), 4.0, 8.0, aModel)

    CreateCone(cadex.ModelData_Point(0.0, -10.0, 0.0), 3.0, 5.0, 7.0, aModel)

    CreateTorus(cadex.ModelData_Point(0.0, 0.0, 0.0), 2.0, 3.0, aModel)

    # Save the result
    aWriter = cadex.ModelData_ModelWriter()
    if not aWriter.Write(aModel, cadex.Base_UTF16String("out/Primitives.xml")):
        print("Unable to save the model!");
        return 1

    print("Completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
