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
import bodyutil
import edgeutil
import faceutil

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license


def SaveModel(theShape: cadex.ModelData_Shape, theName: str) -> bool:
    aModel = cadex.ModelData_Model()
    aBRep =  cadex.ModelData_BRepRepresentation(theShape)
    aPart =  cadex.ModelData_Part(aBRep, cadex.Base_UTF16String(theName))
    aModel.AddRoot(aPart)

    aPath = "out/" + str(theName) + ".xml"
    return cadex.ModelData_ModelWriter().Write(aModel, cadex.Base_UTF16String(aPath))

def main():
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aLine = edgeutil.MakeEdgeFromLine()
    SaveModel(aLine, cadex.Base_UTF16String("LineEdge"))
    aCircle = edgeutil.MakeEdgeFromCircle()
    SaveModel(aCircle, cadex.Base_UTF16String("CircleEdge"))
    anEllipse = edgeutil.MakeEdgeFromEllipse()
    SaveModel(anEllipse, cadex.Base_UTF16String("EllipseEdge"))
    aParabola = edgeutil.MakeEdgeFromParabola()
    SaveModel(aParabola, cadex.Base_UTF16String("ParabolaEdge"))
    aHyperbola = edgeutil.MakeEdgeFromHyperbola()
    SaveModel(aHyperbola, cadex.Base_UTF16String("HyperbolaEdge"))
    anEdgeFromOffsetCurve = edgeutil.MakeEdgeFromOffSetCurve()
    SaveModel(anEdgeFromOffsetCurve, cadex.Base_UTF16String("OffsetEdge"))
    aBezierEdge = edgeutil.MakeEdgeFromBezier()
    SaveModel(aBezierEdge, cadex.Base_UTF16String("BezierEdge"))
    aBSplineEdge = edgeutil.MakeEdgeFromBSpline()
    SaveModel(aBSplineEdge, cadex.Base_UTF16String("BSplineEdge"))

    aPlane = faceutil.MakePlanarFace()
    SaveModel(aPlane, cadex.Base_UTF16String("PlaneFace"))
    aSphere = faceutil.MakeSphericalFace()
    SaveModel(aSphere, cadex.Base_UTF16String("SphereFace"))
    aCylinder = faceutil.MakeCylindricalFace()
    SaveModel(aCylinder, cadex.Base_UTF16String("CylinderFace"))
    aCone = faceutil.MakeConicalFace()
    SaveModel(aCone, cadex.Base_UTF16String("ConeFace"))
    aTorus = faceutil.MakeToroidalFace()
    SaveModel(aTorus, cadex.Base_UTF16String("TorusFace"))
    aFaceFromLESurface = faceutil.MakeFaceFromSurfaceOfLinearExtrusion()
    SaveModel(aFaceFromLESurface, cadex.Base_UTF16String("LEFace"))
    aFaceFromRevSurface = faceutil.MakeFaceFromSurfaceOfRevolution()
    SaveModel(aFaceFromRevSurface, cadex.Base_UTF16String("RevFace"))
    aFaceFromOffsetSurface = faceutil.MakeFaceFromOffsetSurface()
    SaveModel(aFaceFromOffsetSurface, cadex.Base_UTF16String("OffsetFace"))
    aBezierFace = faceutil.MakeFaceFromBezier()
    SaveModel(aBezierFace, cadex.Base_UTF16String("BezierFace"))
    aBSplineFace = faceutil.MakeFaceFromBSpline()
    SaveModel(aBSplineFace, cadex.Base_UTF16String("BSplineFace"))
    aFace = faceutil.MakeFaceWithInnerWire()
    SaveModel(aFace, cadex.Base_UTF16String("InnerWireFace"))

    aSolid = bodyutil.MakeSolidBody()
    SaveModel(aSolid, cadex.Base_UTF16String("SolidBody"))
    aSheet = bodyutil.MakeSheetBody()
    SaveModel(aSheet, cadex.Base_UTF16String("SheetBody"))
    aWireframe = bodyutil.MakeWireframeBody()
    SaveModel(aWireframe, cadex.Base_UTF16String("WireframeBody"))
    anAcorn = bodyutil.MakeAcornBody()
    SaveModel(anAcorn, cadex.Base_UTF16String("AcornBody"))

    print("Completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
