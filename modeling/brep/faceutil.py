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
import math

a3Axis = cadex.ModelData_Axis3Placement()

def MakePlanarFace() -> cadex.ModelData_Face:
    aSurface = cadex.ModelData_Plane(a3Axis)
    return cadex.ModelData_Face(aSurface, -2.0, 2.0, -2.0, 2.0)

def MakeSphericalFace() -> cadex.ModelData_Face:
    aSurface = cadex.ModelData_SphericalSurface(a3Axis, 10.0)
    return cadex.ModelData_Face(aSurface, 0.0, math.pi / 2, 0.0, math.pi / 2)

def MakeCylindricalFace() -> cadex.ModelData_Face:
    aSurface = cadex.ModelData_CylindricalSurface(a3Axis, 10.0)
    return cadex.ModelData_Face(aSurface, 0.0, math.pi, -2.0, 2.0)

def MakeConicalFace() -> cadex.ModelData_Face:
    aSurface = cadex.ModelData_ConicalSurface(a3Axis, 1.0, 7.0)
    return cadex.ModelData_Face(aSurface, 0.0, math.pi, 0.0, math.pi)

def MakeToroidalFace() -> cadex.ModelData_Face:
    aSurface = cadex.ModelData_ToroidalSurface(a3Axis, 7.0, 3.0)
    return cadex.ModelData_Face(aSurface, 0.0, math.pi, 0.0, math.pi)

def MakeFaceFromSurfaceOfLinearExtrusion() -> cadex.ModelData_Face:
    aPoles = [
        cadex.ModelData_Point(-2.0,  1.0, 0.0),
        cadex.ModelData_Point(-1.0, -1.0, 0.0),
        cadex.ModelData_Point( 0.0,  1.0, 0.0),
        cadex.ModelData_Point( 1.0, -1.0, 0.0),
        cadex.ModelData_Point( 2.0,  1.0, 0.0)
    ]

    aBasisCurve = cadex.ModelData_BezierCurve(aPoles)

    aSurface = cadex.ModelData_SurfaceOfLinearExtrusion(aBasisCurve, cadex.ModelData_Direction.ZDir())
    return cadex.ModelData_Face(aSurface, 0.1, 0.9, -10.0, 10.0)

def MakeFaceFromSurfaceOfRevolution() -> cadex.ModelData_Face:
    aPoles = [
        cadex.ModelData_Point(-2.0, 1.0, 0.0),
        cadex.ModelData_Point(-1.0, 3.0, 0.0),
        cadex.ModelData_Point( 0.0, 2.0, 0.0),
        cadex.ModelData_Point( 1.0, 1.0, 0.0),
        cadex.ModelData_Point( 2.0, 2.0, 0.0)
    ]

    aBasisCurve = cadex.ModelData_BezierCurve(aPoles)

    aSurface = cadex.ModelData_SurfaceOfRevolution(aBasisCurve,
                                                   cadex.ModelData_Point(0.0, 0.0, 0.0),
                                                   cadex.ModelData_Direction.XDir())
    return cadex.ModelData_Face(aSurface, 0.0, math.pi + math.pi / 2, 0.1, 0.9)

def MakeFaceFromOffsetSurface() -> cadex.ModelData_Face:
    aPoles = [
        cadex.ModelData_Point(0.0, 0.0,  1.0),
        cadex.ModelData_Point(0.0, 2.0,  1.0),
        cadex.ModelData_Point(2.0, 0.0,  1.0),
        cadex.ModelData_Point(2.0, 2.0, -1.0)
    ]

    aBasisSurface = cadex.ModelData_BezierSurface(aPoles, 2, 2)
    aSurface = cadex.ModelData_OffsetSurface(aBasisSurface, 10.0)
    return cadex.ModelData_Face(aSurface, 0.1, 0.9, 0.1, 0.9)

def MakeFaceFromBezier() -> cadex.ModelData_Face:
    aPoles = [
        cadex.ModelData_Point(0.0, 0.0,  1.0),
        cadex.ModelData_Point(0.0, 2.0,  1.0),
        cadex.ModelData_Point(2.0, 0.0,  1.0),
        cadex.ModelData_Point(2.0, 2.0, -1.0)
    ]

    aSurface = cadex.ModelData_BezierSurface(aPoles, 2, 2)
    return cadex.ModelData_Face(aSurface, 0.25, 0.75, 0.25, 0.75)

def MakeFaceFromBSpline() -> cadex.ModelData_Face:
    aPoles = [
        cadex.ModelData_Point( 0.0,  0.0, 1.0),
        cadex.ModelData_Point( 0.0,  2.0, 3.0),
        cadex.ModelData_Point( 0.0,  6.0, 2.0),
        cadex.ModelData_Point( 0.0,  8.0, 3.0),
        cadex.ModelData_Point( 0.0, 10.0, 1.0),

        cadex.ModelData_Point( 2.0,  0.0, 2.0),
        cadex.ModelData_Point( 2.0,  2.0, 2.0),
        cadex.ModelData_Point( 2.0,  6.0, 2.0),
        cadex.ModelData_Point( 2.0,  8.0, 2.0),
        cadex.ModelData_Point( 2.0, 10.0, 2.0),

        cadex.ModelData_Point( 4.0,  0.0, 3.0),
        cadex.ModelData_Point( 4.0,  2.0, 1.0),
        cadex.ModelData_Point( 4.0,  6.0, 2.0),
        cadex.ModelData_Point( 4.0,  8.0, 1.0),
        cadex.ModelData_Point( 4.0, 10.0, 3.0),

        cadex.ModelData_Point( 6.0,  0.0, 2.0),
        cadex.ModelData_Point( 6.0,  2.0, 2.0),
        cadex.ModelData_Point( 6.0,  6.0, 2.0),
        cadex.ModelData_Point( 6.0,  8.0, 2.0),
        cadex.ModelData_Point( 6.0, 10.0, 2.0),

        cadex.ModelData_Point(10.0,  0.0, 3.0),
        cadex.ModelData_Point(10.0,  2.0, 1.0),
        cadex.ModelData_Point(10.0,  6.0, 2.0),
        cadex.ModelData_Point(10.0,  8.0, 1.0),
        cadex.ModelData_Point(10.0, 10.0, 3.0)
    ]

    aUPoles = 5
    aVPoles = 5

    aUKnots = [ 0.0, 0.25, 0.75, 1.0]
    aVKnots = [ 0.0, 0.25, 0.75, 1.0 ]

    aVMultiplicities = [ 3, 1, 1, 3 ]
    aUMultiplicities = [ 3, 1, 1, 3 ]

    aUDegree = 2
    aVDegree = 2

    aSurface = cadex.ModelData_BSplineSurface(aPoles, aUPoles, aVPoles, aUKnots, aVKnots,
                                              aUMultiplicities, aVMultiplicities,
                                              aUDegree, aVDegree)
    return cadex.ModelData_Face(aSurface, 0.25, 0.75, 0.25, 0.75)

def MakeFaceWithInnerWire() -> cadex.ModelData_Face:
    anAxis2 = cadex.ModelData_Axis2Placement()
    anInnerCircle = cadex.ModelData_Circle(anAxis2, 10.0)
    anOuterCircle = cadex.ModelData_Circle(anAxis2, 20.0)

    anOuterEdge = cadex.ModelData_Edge(anOuterCircle)
    anInnerEdge = cadex.ModelData_Edge(anInnerCircle)

    anOuterWire = cadex.ModelData_Wire(anOuterEdge)
    anInnerWire = cadex.ModelData_Wire(cadex.ModelData_Edge.Cast(anInnerEdge.Reversed()))

    anAxis3 = cadex.ModelData_Axis3Placement(anAxis2)
    aPlane = cadex.ModelData_Plane(anAxis3)
    aFace = cadex.ModelData_Face(aPlane)

    aFace.Append(anOuterWire)
    aFace.Append(anInnerWire)

    return aFace
