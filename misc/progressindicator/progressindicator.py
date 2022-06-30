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
import cadexchanger.CadExACIS as acis

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
import cadex_license as license


class ProgressBarObserver(cadex.Base_ProgressStatus_Observer):
    def __init__(self):
        super().__init__()

    def ChangedValue(self, theInfo: cadex.Base_ProgressStatus):
        print(theInfo.Value())

    def Completed(self, theInfo: cadex.Base_ProgressStatus):
        print(f"{theInfo.Value()}: complete!")

def main(theSource: str):
    aKey = license.Value()

    if not cadex.LicenseManager.Activate(aKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()

    anObserver = ProgressBarObserver()
    anObserver.SetAllNotifyingThreads()

    anIsOK = False
    with cadex.Base_ProgressStatus() as aStatus:
        aStatus.Register(anObserver);                                                # Register an Observer to progress status

        with cadex.Base_ProgressScope(aStatus) as aTopScope:                         # The top scope occupies the whole progress status range
            with cadex.Base_ProgressScope(aTopScope, 40) as aReaderScope:            # 40% of TopScope for file importing
                aReader = acis.ACIS_Reader()
                aReader.SetProgressStatus(aStatus)                                   # Connect progress status object

                if not aStatus.WasCanceled():
                    with cadex.Base_ProgressScope(aReaderScope, 25):    # 25% of ReaderScope (10% of TopScope)
                        anIsOK = aReader.ReadFile(cadex.Base_UTF16String(theSource))

                if anIsOK and not aStatus.WasCanceled():
                    with cadex.Base_ProgressScope(aReaderScope, 75):    # 75% of ReaderScope (30% of TopScope)
                        anIsOK = aReader.Transfer(aModel)

            if anIsOK and not aStatus.WasCanceled():
                with cadex.Base_ProgressScope(aTopScope, -1):        # The remaining 60% of TopScope for meshing
                    aMesher = cadex.ModelAlgo_BRepMesher()
                    aMesher.SetProgressStatus(aStatus)                               # Connect progress status object
                    aMesher.Compute(aModel)

    # Observer will be automatically unregistered from progress status on destruction (end of the "using" scope).

    print("Completed")
    return 0 if anIsOK else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + os.path.abspath(Path(__file__).resolve()) + " <input_file>, where:")
        print("    <input_file>  is a name of the SAT file to be read")
        sys.exit(1)

    aSource = os.path.abspath(sys.argv[1])

    sys.exit(main(aSource))
