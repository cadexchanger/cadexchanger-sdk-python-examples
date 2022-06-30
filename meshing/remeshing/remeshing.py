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

import typing

class MeshReplacementVisitor(cadex.ModelData_Model_VoidElementVisitor):
    def __init__(self):
        super().__init__()
        self.myRootReplacements: typing.Dict[cadex.ModelData_Part, cadex.ModelData_Part] = {}
        self.myInstances: typing.Deque[cadex.ModelData_Instance] = []
        self.myReplacedParts: typing.Dict[cadex.ModelData_Part, cadex.ModelData_Part] = {}

    def VisitEnterInstance(self, theInstance: cadex.ModelData_Instance):
        self.myInstances.append(theInstance)
        return True

    def VisitLeaveInstance(self, theInstance: cadex.ModelData_Instance):
        self.myInstances.pop()

    def VisitPart(self, thePart: cadex.ModelData_Part):
        if thePart.BRepRepresentation().IsNull():
            return

        if self.myReplacedParts.get(thePart) and len(self.myInstances) > 0:
            self.myInstances[-1].SetReference(self.myReplacedParts[thePart])
            return

        aNewPart = cadex.ModelData_Part(thePart.BRepRepresentation(), thePart.Name())
        aNewPart.SetAppearance(thePart.Appearance())
        aNewPart.AddProperties(thePart.Properties())
        aNewPart.AddPMI(thePart.PMI())
        for anIt in thePart.GetLayerIterator():
            aNewPart.AddToLayer(anIt)

        aMesherParams = cadex.ModelAlgo_BRepMesherParameters(cadex.ModelAlgo_BRepMesherParameters.Fine)
        aMesher = cadex.ModelAlgo_BRepMesher(aMesherParams)
        aMesher.Compute(aNewPart)

        if len(self.myInstances) == 0:
            self.myRootReplacements[thePart] = aNewPart
        else:
            self.myRootReplacements[thePart] = aNewPart
            self.myInstances[-1].SetReference(aNewPart)


def main(theSource: str, theDest: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aReader = cadex.ModelData_ModelReader()
    aModel = cadex.ModelData_Model()

    print("Conversion started...")
    # Opening and converting the file
    if not aReader.Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to open and convert the file " + theSource)
        return 1

    aVisitor = MeshReplacementVisitor()
    aModel.AcceptElementVisitor(aVisitor)
    aNewRoots: typing.List[cadex.ModelData_SceneGraphElement]  = []
    for aRoot in aModel.GetElementIterator():
        if aRoot.TypeId() == cadex.ModelData_Part.GetTypeId():
            aRootPart = cadex.ModelData_Part.Cast(aRoot)
            assert aVisitor.myRootReplacements.get(aRootPart), "Part was not processed"
            aNewRoots.append(aVisitor.myRootReplacements[aRootPart])
        else:
            aNewRoots.append(aRoot)

    aModel.Clear()
    for aNewRoot in aNewRoots:
        aModel.AddRoot(aNewRoot)

    aWriter = cadex.ModelData_ModelWriter()
    # Converting and writing the model to file
    if not aWriter.Write(aModel, cadex.Base_UTF16String(theDest)):
        print("Failed to convert and write the file to specified format " + theDest)
        return 1

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("    <input_file>  is a name of the SLD file to be read")
        print("    <output_file> is a name of the VRML file to Save() the model")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])
    aDest = os.path.abspath(sys.argv[2])

    sys.exit(main(aSource, aDest))
