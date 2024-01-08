#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PowerShell Remoting Protocol Client

# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Datei: call_dhcp_reservation_program.py
#
# Dieses Programm wird verwendet, um vom Linux Scriptserver gdepfh8s auf den Windows Scriptserver gdepfn2s zuzugreifen
# und von dort eine Dhcp reservierung zu erstellen.
# 
# Von tribe29 uebernommen.
#
# Erstellt 2023-03-06-scma

import os, sys

try:
    from pypsrp.client import Client
except:
    print("Python module ""pypsrp"" not available. Please install with: pip install pypsrp")
    sys.exit(2)



def main(argv=None):

    if argv is None: argv = sys.argv

    ### Wurde das Programm $0 mit einem Befehl aufgerufen ?
    try: 
        command = argv[1]

    except:
        command = 'C:\\Users\scma_site\zero_touch\create_dhcp_reservation.py --help'


    user, password, server = 'gebcorp\scma_site', 'PASSWORD', 'gdepfn2s.geberit.net' 

    client = Client(server, username=user, password=password, cert_validation=False)
    stdout, stderr, rc = client.execute_cmd(command)

    print(stdout)
    return rc


if __name__ == '__main__':

    sys.exit(main())
