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

a2Axis = cadex.ModelData_Axis2Placement()

def MakeEdgeFromLine() -> cadex.ModelData_Edge:
    aCurve = cadex.ModelData_Line(cadex.ModelData_Point(0.0, 0.0, 0.0), cadex.ModelData_Direction.XDir())
    return cadex.ModelData_Edge(aCurve, -2.0, 2.0)

def MakeEdgeFromCircle() -> cadex.ModelData_Edge:
    aCurve = cadex.ModelData_Circle(a2Axis, 5.0)
    return cadex.ModelData_Edge(aCurve, 0.0, math.pi)

def MakeEdgeFromEllipse() -> cadex.ModelData_Edge:
    aCurve = cadex.ModelData_Ellipse(a2Axis, 7.0, 3.0)
    return cadex.ModelData_Edge(aCurve, 0.0, math.pi)

def MakeEdgeFromParabola() -> cadex.ModelData_Edge:
    aCurve = cadex.ModelData_Parabola(a2Axis, 5.0)
    return cadex.ModelData_Edge(aCurve, -2.0, 2.0)

def MakeEdgeFromHyperbola() -> cadex.ModelData_Edge:
    aCurve = cadex.ModelData_Hyperbola(a2Axis, 7.0, 3.0)
    return cadex.ModelData_Edge(aCurve, -2.0, 2.0)

def MakeEdgeFromOffSetCurve() -> cadex.ModelData_Edge:
    aBasisCurve = cadex.ModelData_Circle(a2Axis, 5.0)
    aCurve = cadex.ModelData_OffsetCurve(aBasisCurve, 10.0, cadex.ModelData_Direction.ZDir())
    return cadex.ModelData_Edge(aCurve, 0.0, math.pi)

def MakeEdgeFromOffsetCurve() -> cadex.ModelData_Edge:
    aBasisCurve = cadex.ModelData_Circle(a2Axis, 5.0)
    aCurve = cadex.ModelData_OffsetCurve(aBasisCurve, 10.0, cadex.ModelData_Direction.ZDir())
    return cadex.ModelData_Edge(aCurve, 0.0, math.pi)

def MakeEdgeFromBezier() -> cadex.ModelData_Edge:
    aPoles = [
        cadex.ModelData_Point(-2.0, 1.0, 0.0),
        cadex.ModelData_Point(-1.0,-1.0, 0.0),
        cadex.ModelData_Point( 0.0, 1.0, 0.0),
        cadex.ModelData_Point( 1.0,-1.0, 0.0)
        ]

    aCurve = cadex.ModelData_BezierCurve(aPoles)
    return cadex.ModelData_Edge(aCurve)

def MakeEdgeFromBSpline() -> cadex.ModelData_Edge:
    aPoles = [
        cadex.ModelData_Point(1.0, 1.0, 0.0),
        cadex.ModelData_Point(2.0, 3.0, 0.0),
        cadex.ModelData_Point(3.0, 2.0, 0.0),
        cadex.ModelData_Point(4.0, 3.0, 0.0),
        cadex.ModelData_Point(5.0, 1.0, 0.0),
    ]

    aKnots = [ 0.0, 0.25, 0.75, 1.0 ]

    aMultiplicities = [ 3, 1, 1, 3 ]

    aDegree = 2
    aCurve = cadex.ModelData_BSplineCurve(aPoles, aKnots, aMultiplicities, aDegree)
    return cadex.ModelData_Edge(aCurve)
