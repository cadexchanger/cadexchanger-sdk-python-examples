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
import cadexchanger.CadExAdvGeom as geom

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license


class FaceCounter(cadex.ModelData_Model_VoidElementVisitor):
    def __init__(self):
        super().__init__()
        self.myNumberOfFaces = 0

    def VisitPart(self, thePart: cadex.ModelData_Part):
        aBRep = thePart.BRepRepresentation()
        aBodyList = aBRep.Get()
        for aBody in aBodyList:
            aFaceIt = cadex.ModelData_Shape_Iterator(aBody, cadex.ModelData_ST_Face)
            self.myNumberOfFaces += len(list(aFaceIt))


def main(theSource: str, theDest: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aReader = cadex.ModelData_ModelReader()

    aModel = cadex.ModelData_Model()

    # Opening and converting the file
    if not aReader.Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to open and convert the file " + theSource)
        return 1

    # Basic info about model
    aBeforeCounter = FaceCounter()
    aModel.AcceptElementVisitor(aBeforeCounter)
    print(f"Model name: {aModel.Name()}")
    print(f"# of faces before: {aBeforeCounter.myNumberOfFaces}")

    # Running the simplifier
    aBuilder = geom.ModelSimplifier_SimplifierBuilder()
    aBuilder.SetLevel(geom.ModelSimplifier_SimplifierBuilder.High)
    aBuilder.SetFeatureSize(geom.ModelSimplifier_SimplifierBuilder.Large)
    aSimplifier = aBuilder.CreatePipeline()

    aNewModel = aSimplifier.Perform(aModel)

    # How many shapes does simplified model contain?
    anAfterCounter = FaceCounter()
    aNewModel.AcceptElementVisitor(anAfterCounter)
    print(f"# of faces after: {anAfterCounter.myNumberOfFaces}")

    # Saving the simplified model
    if not cadex.ModelData_ModelWriter().Write(aNewModel, cadex.Base_UTF16String(theDest)):
        print("Failed to save the .xml file")
        return 1

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("    <input_file>  is a name of the ACIS file to be read")
        print("    <output_file> is a name of the XML file to Save() the model")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])
    aDest = os.path.abspath(sys.argv[2])

    sys.exit(main(aSource, aDest))
