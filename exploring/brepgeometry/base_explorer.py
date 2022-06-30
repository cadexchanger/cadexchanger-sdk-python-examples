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

class BaseExplorer:
    def __init__(self):
        super().__init__()
        self.myNestingLevel = 0

    @classmethod
    def PrintElementary(cls, theGeometry):
        cls.PrintDomain(theGeometry)
        aPosition = theGeometry.Position()
        aLoc =   aPosition.Location()
        anAxis = aPosition.Axis()
        aXDir =  aPosition.XDirection()
        aYDir =  aPosition.YDirection()
        cls.PrintNamedParameter("Location",    aLoc)
        cls.PrintNamedParameter("Axis",        anAxis)
        cls.PrintNamedParameter("X Direction", aXDir)
        cls.PrintNamedParameter("Y Direction", aYDir)

    @classmethod
    def PrintElementary2d(cls, theGeometry):
        cls.PrintDomain(theGeometry)
        aPosition = theGeometry.Position()
        aLoc =  aPosition.Location()
        aXDir = aPosition.XDirection()
        aYDir = aPosition.YDirection()
        cls.PrintNamedParameter("Location",    aLoc)
        cls.PrintNamedParameter("X Direction", aXDir)
        cls.PrintNamedParameter("Y Direction", aYDir)

    @classmethod
    def PrintRange(cls, aName: str, aFirstParameter: float, aLastParameter: float):
        print(f"{aName} = [{aFirstParameter}, {aLastParameter}]; ", end="")

    @classmethod
    def PrintCurveDomain(cls, theCurve):
        cls.PrintRange("Domain", theCurve.UMin(), theCurve.UMax())

    @classmethod
    def PrintSurfaceDomain(cls, theSurface):
        cls.PrintRange("Domain U", theSurface.UMin(), theSurface.UMax())
        cls.PrintRange("V", theSurface.VMin(), theSurface.VMax())

    @classmethod
    def PrintDomain(cls, theValue):
        if isinstance(theValue, cadex.ModelData_Curve) or isinstance(theValue, cadex.ModelData_Curve2d):
            cls.PrintCurveDomain(theValue)
        elif isinstance(theValue, cadex.ModelData_Surface):
            cls.PrintSurfaceDomain(theValue)

    @classmethod
    def Print3dParameter(cls, thePoint):
        print(f"({thePoint.X()}, {thePoint.Y()}, {thePoint.Z()}); ", end="")

    @classmethod
    def Print2dParameter(cls, thePoint):
        print(f"({thePoint.X()}, {thePoint.Y()}); ", end="")

    @classmethod
    def Print1dParameter(cls, theValue):
        print(f"{theValue}; ", end="")

    @classmethod
    def PrintParameter(cls, theValue):
        if isinstance(theValue, cadex.ModelData_Point) or isinstance(theValue, cadex.ModelData_Direction):
            cls.Print3dParameter(theValue)
        elif isinstance(theValue, cadex.ModelData_Point2d) or isinstance(theValue, cadex.ModelData_Direction2d):
            cls.Print2dParameter(theValue)
        elif isinstance(theValue, float):
            cls.Print1dParameter(theValue)

    @classmethod
    def PrintNamedParameter(cls, theName, TheValue):
        print(f"{theName} = ", end="")
        cls.PrintParameter(TheValue)

    @classmethod
    def PrintName(cls, theName: str):
        print(f"{theName}: ", end="")

    @classmethod
    def Print2dCollection(cls, theName: str, theFinalIndex: int, thePrintElement):
        if theName:
            print(f"{theName} = ", end="")

        print("[", end="")
        for i in range(1, theFinalIndex + 1):
            if(i > 3):
                print("...", end="")
                break
            thePrintElement(i)

        print("]; ", end="")


    @classmethod
    def Print3dCollection(cls, theName: str, theFinalIndex1: int, theFinalIndex2: int, thePrintElement):
        def PrintString(i: int):
            cls.Print2dCollection(None, theFinalIndex2, lambda j: thePrintElement(i, j))
        cls.Print2dCollection(theName, theFinalIndex1, PrintString)

    @classmethod
    def PrintOrientation(cls, theOrientation):
        print("Orientation = ", end="")
        if theOrientation == cadex.ModelData_SO_Forward:
            print("Forward", end="")
        elif theOrientation == cadex.ModelData_SO_Reversed:
            print("Reversed", end="")
        else:
            print("Undefined")
        print("; ", end="")

    def PrintTabulation(self):
        print("--- " * self.myNestingLevel, end="")
