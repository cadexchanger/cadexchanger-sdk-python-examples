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


import cadexchanger.CadExCore as cadex
from base_explorer import BaseExplorer
from curve_explorer import CurveExplorer

class SurfaceExplorer(BaseExplorer):
    def __init__():
        super().__init__()

    @classmethod
    def PrintSurface(cls, theSurface: cadex.ModelData_Surface):
        if theSurface.Type() == cadex.ModelData_ST_Plane:
            cls.PrintPlane(cadex.ModelData_Plane.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Cylinder:
            cls.PrintCylinder(cadex.ModelData_CylindricalSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Cone:
            cls.PrintCone(cadex.ModelData_ConicalSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Sphere:
            cls.PrintSphere(cadex.ModelData_SphericalSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Torus:
            cls.PrintTorus(cadex.ModelData_ToroidalSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_LinearExtrusion:
            cls.PrintLinearExtrusion(cadex.ModelData_SurfaceOfLinearExtrusion.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Revolution:
            cls.PrintRevolution(cadex.ModelData_SurfaceOfRevolution.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Bezier:
            cls.PrintBezierSurface(cadex.ModelData_BezierSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_BSpline:
            cls.PrintBSplineSurface(cadex.ModelData_BSplineSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Offset:
            cls.PrintOffsetSurface(cadex.ModelData_OffsetSurface.Cast(theSurface))
        elif theSurface.Type() == cadex.ModelData_ST_Trimmed:
            cls.PrintTrimmedSurface(cadex.ModelData_RectangularTrimmedSurface.Cast(theSurface))


    @classmethod
    def PrintPlane(cls, thePlane: cadex.ModelData_Plane):
        cls.PrintName("Plane")
        cls.PrintElementary(thePlane)

    @classmethod
    def PrintCylinder(cls, theCylinder: cadex.ModelData_CylindricalSurface):
        cls.PrintName("Cylinder")
        aRadius = theCylinder.Radius()
        cls.PrintElementary(theCylinder)
        cls.PrintNamedParameter("Radius", aRadius)

    @classmethod
    def PrintCone(cls, theCone: cadex.ModelData_ConicalSurface):
        cls.PrintName("Cone")
        aRadius =    theCone.Radius()
        aSemiAngle = theCone.SemiAngle()
        cls.PrintElementary(theCone)
        cls.PrintNamedParameter("Radius", aRadius)
        cls.PrintNamedParameter("Semi-Angle", aSemiAngle)

    @classmethod
    def PrintSphere(cls, theSphere: cadex.ModelData_SphericalSurface):
        cls.PrintName("Sphere")
        aRadius = theSphere.Radius()
        cls.PrintElementary(theSphere)
        cls.PrintNamedParameter("Radius", aRadius)

    @classmethod
    def PrintTorus(cls, theTorus: cadex.ModelData_ToroidalSurface):
        cls.PrintName("Torus")
        aMajorRadius = theTorus.MajorRadius()
        aMinorRadius = theTorus.MinorRadius()
        cls.PrintElementary(theTorus)
        cls.PrintNamedParameter("Major Radius", aMajorRadius)
        cls.PrintNamedParameter("Minor Radius", aMinorRadius)

    @classmethod
    def PrintLinearExtrusion(cls, theLinearExtrusion: cadex.ModelData_SurfaceOfLinearExtrusion):
        cls.PrintName("Linear Extrusion Surface")
        aDir = theLinearExtrusion.Direction()
        cls.PrintDomain(theLinearExtrusion)
        cls.PrintNamedParameter("Direction", aDir)
        print("Basis Curve = ", end="")
        CurveExplorer.PrintCurveInfo(theLinearExtrusion.BasisCurve())

    @classmethod
    def PrintRevolution(cls, theRevolution: cadex.ModelData_SurfaceOfRevolution):
        cls.PrintName("Revolution Surface")
        aDir = theRevolution.Direction()
        aLoc = theRevolution.Location()
        print(cls.PrintDomain(theRevolution), end="")
        cls.PrintNamedParameter("Location", aLoc)
        cls.PrintNamedParameter("Direction", aDir)
        print("Basis Curve = ", end="")
        CurveExplorer.PrintCurveInfo(theRevolution.BasisCurve())

    @classmethod
    def PrintBezierSurface(cls, theBezier: cadex.ModelData_BezierSurface):
        cls.PrintName("Bezier Surface")
        aUDegree = theBezier.UDegree()
        aVDegree = theBezier.VDegree()
        aNumberOfUPoles = theBezier.NumberOfUPoles()
        aNumberOfVPoles = theBezier.NumberOfVPoles()
        cls.PrintDomain(theBezier)
        cls.PrintNamedParameter("UKnots Degree", aUDegree)
        cls.PrintNamedParameter("VKnots Degree", aVDegree)
        cls.PrintNamedParameter("Number Of UKnots Poles", aNumberOfUPoles)
        cls.PrintNamedParameter("Number Of VKnots Poles", aNumberOfVPoles)

        def PrintPole(i, j):
            aPole = theBezier.Pole(i, j)
            cls.PrintParameter(aPole)

        cls.PrintCollection("Poles", aNumberOfUPoles, aNumberOfVPoles, PrintPole)

        def PrintWeight(i,j):
            aWeight = theBezier.Weight(i, j)
            cls.PrintParameter(aWeight)

        cls.PrintCollection("Weights", aNumberOfUPoles, aNumberOfVPoles, PrintWeight)

    @classmethod
    def PrintBSplineSurface(cls, theBSpline: cadex.ModelData_BSplineSurface):
        cls.PrintName("BSpline Surface")

        aUDegree = theBSpline.UDegree()
        aVDegree = theBSpline.VDegree()
        aNumberOfUKnots = theBSpline.NumberOfUKnots()
        aNumberOfVKnots = theBSpline.NumberOfVKnots()
        aNumberOfUPoles = theBSpline.NumberOfUPoles()
        aNumberOfVPoles = theBSpline.NumberOfVPoles()
        cls.PrintDomain(theBSpline)
        cls.PrintNamedParameter("UKnots Degree", aUDegree)
        cls.PrintNamedParameter("VKnots Degree", aVDegree)
        cls.PrintNamedParameter("Number Of UKnots ", aNumberOfUKnots)
        cls.PrintNamedParameter("Number Of VKnots ", aNumberOfVKnots)
        cls.PrintNamedParameter("Number Of UKnots Poles", aNumberOfUPoles)
        cls.PrintNamedParameter("Number Of VKnots Poles", aNumberOfVPoles)

        def PrintUKnot(i):
            aKnot = theBSpline.UKnot(i)
            cls.PrintParameter(aKnot)

        cls.Print2dCollection("UKnots ", aNumberOfUKnots, PrintUKnot)

        def PrintVKnot(i):
            aKnot = theBSpline.VKnot(i)
            cls.PrintParameter(aKnot)

        cls.Print2dCollection("VKnots ", aNumberOfVKnots, PrintVKnot)

        def PrintUMultiplicity(i):
            aUMultiplicity = theBSpline.UMultiplicity(i)
            cls.PrintParameter(aUMultiplicity)

        cls.Print2dCollection("UKnots Multiplicities", aNumberOfUKnots, PrintUMultiplicity)

        def PrintVMultiplicity(i):
            aVMultiplicity = theBSpline.VMultiplicity(i)
            cls.PrintParameter(aVMultiplicity)

        cls.Print2dCollection("VKnots Multiplicities", aNumberOfVKnots, PrintVMultiplicity)

        def PrintPole(i, j):
            aPole = theBSpline.Pole(i, j)
            cls.PrintParameter(aPole)

        cls.Print3dCollection("Poles", aNumberOfUPoles, aNumberOfVPoles, PrintPole)

        def PrintWeight(i,j):
            aWeight = theBSpline.Weight(i, j)
            cls.PrintParameter(aWeight)

        cls.Print3dCollection("Weights", aNumberOfUPoles, aNumberOfVPoles, PrintWeight)

    @classmethod
    def PrintOffsetSurface(cls, theOffset: cadex.ModelData_OffsetSurface):
        cls.PrintName("Offset Surface")
        anOffset = theOffset.Offset()
        cls.PrintDomain(theOffset)
        cls.PrintNamedParameter("Offset", anOffset)
        print("Basis Surface = ", end="")
        cls.PrintSurface(theOffset.BasisSurface())

    @classmethod
    def PrintTrimmedSurface(cls, theTrimmed: cadex.ModelData_RectangularTrimmedSurface):
        cls.PrintName("Trimmed Surface")
        cls.PrintDomain(theTrimmed)
        print("Basis Surface = ", end="")
        cls.PrintSurface(theTrimmed.BasisSurface())
