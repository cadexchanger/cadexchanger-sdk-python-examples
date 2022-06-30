#!/usr/bin/env python3

#  $Id$

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

class SceneGraphVisitor(cadex.ModelData_Model_ElementVisitor):
    def __init__(self):
        super().__init__()
        self.myNestingLevel = 0
        self.margin = 0; # This variable is used for formatting of output table
        self.mySGEMap = {}

    def PrintName(self, theSGEElement: cadex.ModelData_SceneGraphElement, theName: str):
        print("--- " * self.myNestingLevel, end="")

        if theName:
            print(f"{theSGEElement}: {theName}")
        else:
            print(f"{theSGEElement}: noname")

        # Calculating spacing for output table columns
        self.margin = max(self.margin, theName.Length())

    def UpdateTable(self, theSGE: cadex.ModelData_SceneGraphElement):
        if not self.mySGEMap.get(theSGE):
            self.mySGEMap[theSGE] = 1
        else:
            self.mySGEMap[theSGE] +=  1

    def PrintSGEType(self, theSGE: cadex.ModelData_SceneGraphElement) -> str:
        if theSGE.TypeId() == cadex.ModelData_Part.GetTypeId():
            return "Part"
        elif theSGE.TypeId() == cadex.ModelData_Assembly.GetTypeId():
            return "Assembly"
        elif theSGE.TypeId() == cadex.ModelData_Instance.GetTypeId():
            return "Instance"
        return "Undefined"

    def PrintCounts(self):
        print("Total:")
        print("\t" + "name".ljust(self.margin) + " | " + "type".ljust(self.margin) + " | count")

        for i in self.mySGEMap:
            aName = str(i.Name())
            aType = self.PrintSGEType(i)
            print("\t" + aName.ljust(self.margin) + " | " +
                  aType.ljust(self.margin) + " | " + str(self.mySGEMap[i]))


    def VisitPart(self, thePart: cadex.ModelData_Part):
        self.PrintName("Part", thePart.Name())
        self.UpdateTable(thePart)

    def VisitEnterAssembly(self, theAssembly: cadex.ModelData_Assembly) -> bool:
        self.PrintName("Assembly", theAssembly.Name())
        self.UpdateTable(theAssembly)
        self.myNestingLevel += 1
        return True

    def VisitEnterInstance(self, theInstance: cadex.ModelData_Instance) -> bool:
        self.PrintName("Instance", theInstance.Name())
        self.myNestingLevel += 1
        return True

    def VisitLeaveAssembly(self, theAssembly: cadex.ModelData_Assembly):
        self.myNestingLevel -= 1

    def VisitLeaveInstance(self, theInstance: cadex.ModelData_Instance):
        self.myNestingLevel -= 1


def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    aCounter = SceneGraphVisitor()

    aModel.AcceptElementVisitor(aCounter)
    aCounter.PrintCounts()

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        sys.exit()

    aSource = os.path.abspath(sys.argv[1])

    sys.exit(main(aSource))
