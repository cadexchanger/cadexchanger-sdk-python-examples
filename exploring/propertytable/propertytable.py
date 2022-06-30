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

class PropertiesVisitor(cadex.ModelData_Model_CombinedElementVisitor):
    def VisitPart(self, thePart: cadex.ModelData_Part):
        aPT = thePart.Properties()
        self.ExplorePropertyTable(aPT)

        aBRep = thePart.BRepRepresentation()
        if aBRep:
            aVisitor = SubShapePropertiesVisitor(aBRep)
            aBRep.Accept(aVisitor)

            # Extract all PropertyTables from SubShapes in B-Rep and explore it
            aPTList = aVisitor.PropertyTables()
            for i in aPTList:
                self.ExplorePropertyTable(i)


    def VisitEnterSGE(self, theElement: cadex.ModelData_SceneGraphElement) -> bool:
        aPT = theElement.Properties()
        self.ExplorePropertyTable(aPT)

        return True

    def ExtractPropertyTables(self, theBRep: cadex.ModelData_BRepRepresentation) -> list:
        aPTList = []
        aBodyGen = theBRep.Get()
        for aBody in aBodyGen:
            aPTList.append(theBRep.PropertyTable(aBody))
        return aPTList

    def ExplorePropertyTable(self, thePT: cadex.ModelData_PropertyTable):
        if thePT and not thePT.IsEmpty():
            aPropVisitor = PropertyVisitor()
            thePT.Accept(aPropVisitor)
        else:
            print("\nProperty Table is empty")

class PropertyVisitor(cadex.ModelData_PropertyTable_VoidVisitor):
    def __init__(self):
        super().__init__()
        print("\nProperty table: ")

    def VisitI32(self, theName: cadex.Base_UTF16String, theValue):
        self.OutputData(theName, theValue)

    def VisitDouble(self, theName: cadex.Base_UTF16String, theValue):
        self.OutputData(theName, theValue)

    def VisitUTF16String(self, theName: cadex.Base_UTF16String, theValue: cadex.Base_UTF16String):
        self.OutputData(theName, theValue)

    def OutputData(self, theName: cadex.Base_UTF16String, theValue):
        print(f"{theName}: {theValue}")

    def ExplorePropertyTable(self, thePT: cadex.ModelData_PropertyTable):
        # Traverse property table
        aPropVisitor = PropertyVisitor()
        thePT.Accept(aPropVisitor)

class SubShapePropertiesVisitor(cadex.SubshapeVisitor):
    def __init__(self, theBRep: cadex.ModelData_BRepRepresentation):
        super().__init__()
        self.myPTList = []
        self.myBRep = theBRep

    def PropertyTables(self) -> list:
        return self.myPTList

    def VisitShape(self, theShape: cadex.ModelData_Shape):
        aPT = self.myBRep.PropertyTable(theShape)
        self.myPTList.append(aPT)


def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource )
        return 1

    aVisitor = PropertiesVisitor()
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
