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
import cadexchanger.CadExSTEP as step

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license

class TabulatedOutput:
    myNestingLevel = 0

    @classmethod
    def WriteLine(cls, theObject: str):
        cls.PrintTabulation()
        print(theObject)

    @classmethod
    def IncreaseIndent(cls):
       cls.myNestingLevel += 1

    @classmethod
    def DecreaseIndent(cls):
        cls.myNestingLevel -= 1

    @classmethod
    def PrintTabulation(cls):
        if cls.myNestingLevel <= 0:
            return
        # Emulate tabulation like tree.
        for i in range(cls.myNestingLevel - 1):
            if i < 2 or i == 3:
                print("|  ", end="")
            else:
                print("   ", end="")
        print("|__", end="")
        if cls.myNestingLevel > 3:
            print(" ", end="")


class SceneGraphVisitor(cadex.ModelData_Model_ElementVisitor):
    def VisitPart(self, thePart: cadex.ModelData_Part):
        self.PrintName("Part", thePart.Name())
        self.ExplorePMI(thePart)

    def VisitEnterInstance(self, theInstance: cadex.ModelData_Instance):
        TabulatedOutput.IncreaseIndent()
        self.PrintName("Instance", theInstance.Name())
        self.ExplorePMI(theInstance)
        return True

    def VisitEnterAssembly(self, theAssembly: cadex.ModelData_Assembly):
        TabulatedOutput.IncreaseIndent()
        self.PrintName("Assembly", theAssembly.Name())
        self.ExplorePMI(theAssembly)
        return True

    def VisitLeaveInstance(self, theInstance: cadex.ModelData_Instance):
        TabulatedOutput.DecreaseIndent()

    def VisitLeaveAssembly(self, theAssembly: cadex.ModelData_Assembly):
        TabulatedOutput.DecreaseIndent()

    def ExplorePMI(self, theSGE: cadex.ModelData_SceneGraphElement):
        aPMITable : cadex.ModelData_PMITable = theSGE.PMI()
        if aPMITable:
            TabulatedOutput.WriteLine("PMI Table:")
            TabulatedOutput.IncreaseIndent()

            aDataIt = aPMITable.GetPMIDataIterator()
            for aData in aDataIt:
                TabulatedOutput.WriteLine(f"PMI Data: {aData.Name()}")

                TabulatedOutput.IncreaseIndent()

                aSemanticElement = aData.SemanticElement()
                if aSemanticElement:
                    TabulatedOutput.WriteLine("Semantic element:")
                    TabulatedOutput.IncreaseIndent()
                    aVisitor = PMISemanticVisitor()
                    aSemanticElement.Accept(aVisitor)
                    TabulatedOutput.DecreaseIndent()

                aGraphicalElement = aData.GraphicalElement()
                if aGraphicalElement:
                    TabulatedOutput.WriteLine("Graphical element:")
                    TabulatedOutput.IncreaseIndent()
                    aVisitor = PMIGraphicalVisitor()
                    aGraphicalElement.Accept(aVisitor)
                    TabulatedOutput.DecreaseIndent()

                TabulatedOutput.DecreaseIndent()
            TabulatedOutput.DecreaseIndent()


    def PrintName(self, theSGElement: str, theName: str):
        if theName:
            TabulatedOutput.WriteLine(f"{theSGElement}: {theName}")
        else:
            TabulatedOutput.WriteLine(f"{theSGElement}: <noname>")


class PMISemanticVisitor(cadex.ModelData_PMISemanticElementComponentVisitor):
    def VisitDatumComponent(self, theComponent: cadex.ModelData_PMIDatumComponent):
        TabulatedOutput.WriteLine("Datum")
        TabulatedOutput.IncreaseIndent()
        TabulatedOutput.WriteLine(f"Label: {theComponent.Label()}")
        self.PrintAttributes(theComponent)
        TabulatedOutput.DecreaseIndent()

    def VisitDimensionComponent(self, theComponent: cadex.ModelData_PMIDimensionComponent):
        TabulatedOutput.WriteLine("Dimension")
        TabulatedOutput.IncreaseIndent()
        TabulatedOutput.WriteLine(f"Nominal Value: {theComponent.NominalValue()}")
        TabulatedOutput.WriteLine(f"Type of dimension: {int(theComponent.TypeOfDimension())}")
        self.PrintAttributes(theComponent)
        TabulatedOutput.DecreaseIndent()

    def VisitGeometricToleranceComponent(self, theComponent: cadex.ModelData_PMIGeometricToleranceComponent):
        TabulatedOutput.WriteLine("Geometric tolerance")
        TabulatedOutput.IncreaseIndent()
        TabulatedOutput.WriteLine(f"Magnitude: {theComponent.Magnitude()}")
        TabulatedOutput.WriteLine(f"Tolerance zone form: {int(theComponent.ToleranceZoneForm())}")
        self.PrintAttributes(theComponent)
        TabulatedOutput.DecreaseIndent()

    def PrintAttributes(self, theComponent: cadex.ModelData_PMISemanticElementComponent):
        if theComponent.HasAttributes():
            aVisitor = PMISemanticAttributeVisitor()
            theComponent.Accept(aVisitor)

class PMISemanticAttributeVisitor(cadex.ModelData_PMISemanticAttributeVisitor):
    def VisitModifierAttribute(self, theAttribute: cadex.ModelData_PMIModifierAttribute):
        TabulatedOutput.WriteLine(f"Modifier: {theAttribute.Modifier()}")

    def VisitModifierWithValueAttribute(self, theAttribute: cadex.ModelData_PMIModifierWithValueAttribute):
        TabulatedOutput.WriteLine(f"ModifierWithValue: modifier={theAttribute.Modifier()}, value={theAttribute.Value()}")

    def VisitQualifierAttribute(self, theAttribute: cadex.ModelData_PMIQualifierAttribute):
        TabulatedOutput.WriteLine(f"Qualifier: {theAttribute.Qualifier()}")

    def VisitPlusMinusBoundsAttribute(self, theAttribute: cadex.ModelData_PMIPlusMinusBoundsAttribute):
        TabulatedOutput.WriteLine(f"PlusMinusBounds: ({theAttribute.LowerBound()}, {theAttribute.UpperBound()})")

    def VisitRangeAttribute(self, theAttribute: cadex.ModelData_PMIRangeAttribute):
        TabulatedOutput.WriteLine(f"Range: [{theAttribute.LowerLimit()}, {theAttribute.UpperLimit()}]")

    def VisitLimitsAndFitsAttribute(self, theAttribute: cadex.ModelData_PMILimitsAndFitsAttribute):
        TabulatedOutput.WriteLine(f"LimitsAndFits: value={theAttribute.Value()} + {type}={theAttribute.Type()}")

    def VisitDatumTargetAttribute(self, theAttribute: cadex.ModelData_PMIDatumTargetAttribute):
        TabulatedOutput.WriteLine(f"DatumTarget: index={theAttribute.Index()}, description={theAttribute.Description()}")

    def VisitDatumRefAttribute(self, theAttribute: cadex.ModelData_PMIDatumRefAttribute):
        TabulatedOutput.WriteLine(f"DatumRef: precedence={theAttribute.Precedence()}, targetLabel={theAttribute.TargetLabel()}")

    def VisitDatumRefCompartmentAttribute(self, theAttribute: cadex.ModelData_PMIDatumRefCompartmentAttribute):
        TabulatedOutput.WriteLine("DatumRefCompartment:")

        TabulatedOutput.IncreaseIndent()

        aNumberOfReferences = theAttribute.NumberOfReferences()
        if aNumberOfReferences > 0:
            TabulatedOutput.WriteLine("References:")
            TabulatedOutput.IncreaseIndent()
            for i in range(aNumberOfReferences):
                theAttribute.Reference(i).Accept(self)
            TabulatedOutput.DecreaseIndent()

        aNumberOfModifierAttributes = theAttribute.NumberOfModifierAttributes()
        if aNumberOfModifierAttributes > 0:
            TabulatedOutput.WriteLine("Modifiers:")
            TabulatedOutput.IncreaseIndent()
            for i in range(aNumberOfModifierAttributes):
                theAttribute.ModifierAttribute(i).Accept(self)
            TabulatedOutput.DecreaseIndent()

        TabulatedOutput.DecreaseIndent()

    def VisitMaximumValueAttribute(self, theAttribute: cadex.ModelData_PMIMaximumValueAttribute):
        TabulatedOutput.WriteLine(f"MaximumValue: {theAttribute.MaxValue()}")

    def VisitDisplacementAttribute(self, theAttribute: cadex.ModelData_PMIDisplacementAttribute):
        TabulatedOutput.WriteLine(f"Displacement: {theAttribute.Displacement()}")

    def VisitLengthUnitAttribute(self, theAttribute: cadex.ModelData_PMILengthUnitAttribute):
        TabulatedOutput.WriteLine(f"LengthUnit: {theAttribute.Unit()}")

    def VisitAngleUnitAttribute(self, theAttribute: cadex.ModelData_PMIAngleUnitAttribute):
        TabulatedOutput.WriteLine(f"AngleUnit: {theAttribute.Unit()}")

class PMIGraphicalVisitor(cadex.ModelData_PMIGraphicalElementComponentVisitor):
    def VisitOutlinedComponent(self, theComponent: cadex.ModelData_PMIOutlinedComponent):
        TabulatedOutput.WriteLine("Outline")
        TabulatedOutput.IncreaseIndent()
        aVisitor = PMIOutlineVisitor()
        theComponent.Outline().Accept(aVisitor)
        TabulatedOutput.DecreaseIndent()

    def VisitTextComponent(self, theComponent: cadex.ModelData_PMITextComponent):
        TabulatedOutput.WriteLine(f"Text [{theComponent.Text()}]")

    def VisitTriangulatedComponent(self, theComponent: cadex.ModelData_PMITriangulatedComponent):
        TabulatedOutput.WriteLine(f"Triangulation [{theComponent.TriangleSet().NumberOfFaces()} triangles]")
class PMIOutlineVisitor(cadex.ModelData_PMIOutlineVisitor):
    def VisitPolyOutline(self, theOutline: cadex.ModelData_PMIPolyOutline):
        TabulatedOutput.WriteLine(f"PolyLine set [{theOutline.LineSet().NumberOfPolyLines()} polylines]")

    def VisitPoly2dOutline(self, theOutline: cadex.ModelData_PMIPoly2dOutline):
        TabulatedOutput.WriteLine(f"PolyLine2d set [{theOutline.LineSet().NumberOfPolyLines()} polylines]")

    def VisitCurveOutline(self, theOutline: cadex.ModelData_PMICurveOutline):
        TabulatedOutput.WriteLine(f"Curve set [{theOutline.NumberOfCurves()} curves]")

    def VisitCurve2dOutline(self, theOutline: cadex.ModelData_PMICurve2dOutline):
        TabulatedOutput.WriteLine(f"Curve2d set [{theOutline.NumberOfCurves()} curves]")

    def VisitEnterCompositeOutline(self, theOutline: cadex.ModelData_PMICompositeOutline):
        TabulatedOutput.WriteLine("Composite outline:")
        TabulatedOutput.IncreaseIndent()
        return True

    def VisitLeaveCompositeOutline(self, theOutline: cadex.ModelData_PMICompositeOutline):
        TabulatedOutput.DecreaseIndent()

def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()
    aReader = cadex.ModelData_ModelReader()
    aParams = step.STEP_ReaderParameters()
    aParams.SetReadPMI(True)
    aReader.SetReaderParameters(aParams)

    # Opening and converting the file
    if not aReader.Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to open and convert the file ", theSource)
        return 1

    # Create a PMI visitor
    aVisitor = SceneGraphVisitor()
    aModel.AcceptElementVisitor(aVisitor)

    print("Completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("    <input_file>  is a name of the STEP file to be read")
        sys.exit()

    aSource = os.path.abspath(sys.argv[1])

    sys.exit(main(aSource))
