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


class LayersFiller(cadex.ModelData_Model_CombinedElementVisitor):
    def __init__(self):
        super().__init__()
        self.mySubShapesLayer = cadex.ModelData_Layer(cadex.Base_UTF16String("SubshapesLayer"))
        self.mySGELayer = cadex.ModelData_Layer(cadex.Base_UTF16String("SGELayer"))

    def VisitPart(self, thePart: cadex.ModelData_Part):
        self.mySGELayer.Add(thePart)
        aBRep = thePart.BRepRepresentation()
        if aBRep:
            aBodyList = aBRep.Get()
            for aBody in aBodyList:
                aBRep.AddToLayer(aBody, self.mySubShapesLayer)

    def VisitEnterSGE(self, theElement) -> bool:
        self.mySGELayer.Add(theElement)
        return True


class LayerItemVisitor(cadex.ModelData_Layer_ItemVisitor):
    def __init__(self):
        super().__init__()
        self.myPartsNb = 0
        self.myAssembliesNb = 0
        self.myInstancesNb = 0
        self.myShapesNb = 0

    def GetElementsCount(self):
        print(f"Number of parts:      {self.myPartsNb}")
        print(f"Number of assemblies: {self.myAssembliesNb}")
        print(f"Number of instances:  {self.myInstancesNb}")
        print(f"Number of shapes:     {self.myShapesNb}")

    def VisitSGE(self, theSGE: cadex.ModelData_SceneGraphElement):
        if theSGE.TypeId() == cadex.ModelData_Part.GetTypeId():
            self.myPartsNb += 1
        elif theSGE.TypeId() == cadex.ModelData_Assembly.GetTypeId():
            self.myAssembliesNb += 1
        elif theSGE.TypeId() == cadex.ModelData_Instance.GetTypeId():
            self.myInstancesNb += 1

    def VisitShape(self, theShape: cadex.ModelData_Shape, theRep: cadex.ModelData_Representation):
        self.myShapesNb += 1

class LayersVisitor(cadex.ModelData_Model_LayerVisitor):
    def __init__(self):
        super().__init__()

    def VisitLayer(self, theLayer: cadex.ModelData_Layer):
        aLayerItemVisitor = LayerItemVisitor()
        theLayer.Accept(aLayerItemVisitor)
        print(f"Layer {theLayer.Name()} contains:")
        aLayerItemVisitor.GetElementsCount()


def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    aLayerIt = aModel.GetLayerIterator()
    if not aLayerIt.HasNext():
        #Create a visitor to fill its layers
        aVisitor = LayersFiller()
        aModel.AcceptLayerVisitor(aVisitor)

        # Add created layers to the model
        aModel.AddLayer(aVisitor.mySGELayer)
        aModel.AddLayer(aVisitor.mySubShapesLayer)

    aLayerVisitor = LayersVisitor()
    aModel.AcceptLayerVisitor(aLayerVisitor)

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])
    sys.exit(main(aSource))
