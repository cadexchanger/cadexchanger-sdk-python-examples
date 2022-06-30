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


class InstancesTransformationsVisitor(cadex.ModelData_Model_VoidElementVisitor):
    def __init__(self):
        super().__init__()

        # We are going to multiply each matrix to produce transformations relative to the SceneGraph root
        self.myTransformationMatrix = []
        anIdentity = cadex.ModelData_Transformation()
        self.myTransformationMatrix.append(anIdentity)

    def VisitEnterInstance(self, theInstance: cadex.ModelData_Instance) -> bool:
        aTrsf = cadex.ModelData_Transformation()
        if theInstance.HasTransformation():
            aTrsf = theInstance.Transformation()

        aCumulativeTrsf = self.myTransformationMatrix[-1].Multiplied(aTrsf)
        self.myTransformationMatrix.append(aCumulativeTrsf)
        self.PrintTransformation(theInstance.Name())
        return True

    def PrintTransformation(self, theName: cadex.Base_UTF16String):
        if not theName:
            theName = cadex.Base_UTF16String("noName")
        print(f"Instance {theName} has transformations:")

        # Current transformations are relative to the SceneGraph root
        v00, v01, v02, v10, v11, v12, v20, v21, v22 = self.myTransformationMatrix[-1].RotationPart()
        aTranslation = self.myTransformationMatrix[-1].TranslationPart()
        print(f"| {v00} {v01} {v02} {aTranslation.X()} |")
        print(f"| {v10} {v11} {v12} {aTranslation.Y()} |")
        print(f"| {v20} {v21} {v22} {aTranslation.Z()} |")

    def VisitLeaveInstance(self, theInstance: cadex.ModelData_Instance):
        self.myTransformationMatrix.pop()


def main(theSource):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    # Visitor to check and print transformations of instances
    aVisitor = InstancesTransformationsVisitor()
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
