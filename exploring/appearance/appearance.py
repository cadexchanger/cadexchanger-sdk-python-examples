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

class SubshapeAppearancesCollector(cadex.SubshapeVisitor):
    def __init__(self, theBRep: cadex.ModelData_BRepRepresentation, theAppSet: set):
        super().__init__()
        self.myBRep = theBRep
        self.myAppSet = theAppSet

    def VisitShape(self, theShape: cadex.ModelData_Shape):
        self.ExploreShapeAppearances(theShape)

    def ExploreShapeAppearances(self, theShape: cadex.ModelData_Shape):
        anApp = self.myBRep.Appearance(theShape)
        if anApp:
            self.myApp.add(anApp)


class RepVisitor(cadex.ModelData_Part_RepresentationVisitor):
    def __init__(self, theAppSet: set):
        super().__init__()
        self.myAppSet = theAppSet

    def VisitBRep(self, theBRep: cadex.ModelData_BRepRepresentation):
        aCollector = SubshapeAppearancesCollector(theBRep, self.myAppSet)
        theBRep.Accept(aCollector)

    def VisitPoly(self, thePolyRep: cadex.ModelData_PolyRepresentation):
        self.ExplorePVSAppearances(thePolyRep)

    def ExplorePVSAppearances(self, thePolyRep: cadex.ModelData_PolyRepresentation):
        aList = thePolyRep.Get()
        for aPVS in aList:
            anApp = aPVS.Appearance()
            if anApp:
                self.myAppSet.add(anApp)

class SGEAppearancesCollector(cadex.ModelData_Model_CombinedElementVisitor):
    def __init__(self, theAppSet):
        super().__init__()
        self.myAppSet = theAppSet

    def VisitPart(self, thePart: cadex.ModelData_Part):
        self.ExploreSGEAppearance(thePart)
        aVisitor = RepVisitor(self.myAppSet)
        thePart.Accept(aVisitor)

    def VisitEnterSGE(self, theElement) -> bool:
        self.ExploreSGEAppearance(theElement)
        return True

    # Collects SceneGraphElement appearance
    def ExploreSGEAppearance(self, theSGE: cadex.ModelData_SceneGraphElement):
        anApp = theSGE.Appearance()
        if anApp:
            self.myAppSet.add(anApp)


class AppearancesCollector:
    def __init__(self, theModel: cadex.ModelData_Model):
        self.myModel = theModel
        aCollector = SGEAppearancesCollector(set())
        self.myModel.AcceptElementVisitor(aCollector)
        self.myAppSet = aCollector.myAppSet


    def PrintAppearancesCount(self):
        print("Total model unique Appearances count:", len(self.myAppSet))


def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file", theSource)
        return 1

    # Explore model's appearances
    aCollector = AppearancesCollector(aModel)

    # Print the number of unique appearances in our model
    aCollector.PrintAppearancesCount()

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])
    sys.exit(main(aSource))
