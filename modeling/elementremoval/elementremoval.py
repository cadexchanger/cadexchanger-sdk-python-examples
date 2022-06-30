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

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + r"/../../"))
import cadex_license as license


class RemovedSGEFinder(cadex.ModelData_Model_VoidElementVisitor):
    def __init__(self, theNameToRemove: cadex.Base_UTF16String):
        super().__init__()
        self.myNameToRemove = theNameToRemove
        self.SGEsToRemove =  {}

    # Non-root SGEs that can be removed are under assemblies. Iterate
    # through the assembly's child instances and find those that reference
    # SGEs with given name
    def VisitEnterAssembly(self, theElement: cadex.ModelData_Assembly) -> bool:
        for aSGE in cadex.ModelData_Model_ElementIterator(theElement):
            aChild = cadex.ModelData_Instance.Cast(aSGE)

            if aChild.Reference() and aChild.Reference().Name() == self.myNameToRemove:
                self.RemoveElement(aChild, theElement)

        return True

    def RemoveElement(self, theElement: cadex.ModelData_Instance, theParent: cadex.ModelData_Assembly):
        if self.SGEsToRemove.get(theParent):
            self.SGEsToRemove[theParent].append(theElement)
        else:
            self.SGEsToRemove[theParent] = [theElement]

def main(theSource: str, theOutput: str, theNameToRemove: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    # Load the model
    aModel = cadex.ModelData_Model()

    if not cadex.ModelData_ModelReader().Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to read the file " + theSource)
        return 1

    # Remove roots with specified name
    aRootsToRemove = []
    for anElement in cadex.ModelData_Model_ElementIterator(aModel):
        if anElement.Name() == cadex.Base_UTF16String(theNameToRemove):
            aRootsToRemove.append(anElement)

    for aRootToRemove in aRootsToRemove:
        aModel.RemoveRoot(aRootToRemove)

    # Find the rest of scene graph elements that need to be removed and their parents
    aFinder = RemovedSGEFinder(cadex.Base_UTF16String(theNameToRemove))
    aModel.AcceptElementVisitor(aFinder)

    # Perform the recorded removals of non-root SGEs
    for aParent in aFinder.SGEsToRemove:
        aChildrenToRemove = aFinder.SGEsToRemove[aParent]

        for aChildToRemove in aChildrenToRemove:
            aParent.RemoveInstance(aChildToRemove)

    # Save the result
    cadex.ModelData_ModelWriter().Write(aModel, cadex.Base_UTF16String(theOutput))

    print("Completed")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) +
              " <input_file> <output_file> <sge_to_remove>, where:")
        print("    <input_file>  is a name of the XML file to be read")
        print("    <output_file>   is a name of the XML file where the output should be stored")
        print("    <sge_to_remove> is a name of the scene graph elements to remove")
        sys.exit(1)

    aSource = sys.argv[1]
    anOutput = sys.argv[2]
    aNameToRemove = sys.argv[3]

    sys.exit(main(aSource, anOutput, aNameToRemove))
