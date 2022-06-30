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

def MakeSolidBody() -> cadex.ModelData_Body:
    aSolid = cadex.ModelAlgo_TopoPrimitives.CreateBox(cadex.ModelData_Point(-3.0, -3.0, -4.0), cadex.ModelData_Point(3.0, 3.0, -2.0));
    aBody = cadex.ModelData_Body.Create(aSolid);
    return aBody;

def MakeSheetBody() -> cadex.ModelData_Body:
    aPlane = cadex.ModelData_Plane(cadex.ModelData_Point(0.0, 0.0, 0.0), cadex.ModelData_Direction.ZDir());
    aFace1 = cadex.ModelData_Face(aPlane, -4.0, 0.0, -4.0, 0.0);
    aFace2 = cadex.ModelData_Face(aPlane, 0.0, 4.0, 0.0, 4.0);

    aShell = cadex.ModelData_Shell(aFace1);
    aShell.Append(aFace2);

    aBody = cadex.ModelData_Body.Create(aShell);
    return aBody;

def MakeWireframeBody() -> cadex.ModelData_Body:
    anAxis = cadex.ModelData_Axis2Placement(cadex.ModelData_Point(0.0, 0.0, 0.0),
                                            cadex.ModelData_Direction.ZDir(),
                                            cadex.ModelData_Direction.XDir());
    aCircle = cadex.ModelData_Circle(anAxis, 5.0);
    anEdge1 = cadex.ModelData_Edge(aCircle, 1.0, 3.0);
    anEdge2 = cadex.ModelData_Edge(aCircle, 1.0, 3.0);

    aWire = cadex.ModelData_Wire(anEdge1);
    aWire.Append(anEdge2);

    aBody = cadex.ModelData_Body.Create(aWire);
    return aBody;

def MakeAcornBody() -> cadex.ModelData_Body:
    aVertex = cadex.ModelData_Vertex(cadex.ModelData_Point(0.0, 0.0, 0.0));
    aBody = cadex.ModelData_Body.Create(aVertex);
    return aBody;
