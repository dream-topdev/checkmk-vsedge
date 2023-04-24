#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Checks based on the Phion-MIB for the Barracuda CloudGen Firewall.
#
# Copyright (C) 2021  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# License Core module
 
import json
import rsa
import datetime
def doCheckinglicense():
    machinIdPath = "/etc/machine-id"
    licensePath = "/home/cfvnms/Downloads/license.key"
    productName = "vsedge"
    privateKeySize = 1197
    try:
        # Load machine id file
        machineIdFile = open(machinIdPath)
        machineId = machineIdFile.readline()
        machineId = machineId.rstrip()
        # Load License key file
        licenseFile = open(licensePath, 'rb')
        ## Load RSA private key file        
        privateKeyData = licenseFile.read(privateKeySize)
        privateKey = rsa.PrivateKey.load_pkcs1(privateKeyData, format="DER")
        ## Load License part
        licenseKey = licenseFile.read()
        # Parse License json data
        decMessageBytes = rsa.decrypt(licenseKey, privateKey)
        decMessage = decMessageBytes.decode("UTF-8")
        licenseObj = json.loads(decMessage)
        result = {
            'expiredAt': '',
            'daysLeft': 0,
            'status': '',
            'msg': '',
            'machineId': machineId
        }
        if (licenseObj["machineId"] == machineId and licenseObj["products"].count(productName) > 0):
            expiredAt = datetime.datetime.fromisoformat(licenseObj["expiredAt"])
            currentTime = datetime.datetime.now()
            delta = expiredAt - currentTime
            result['expiredAt'] = expiredAt.strftime("%Y-%m-%d")
            result['daysLeft'] = delta.days
            if (expiredAt < currentTime):
                result['status'] = "License expired"
                result['msg'] = "License expired, Please contact CableFree support team.  Machine ID: %s" % (machineId)
            else:
                result['status'] = "OK"
        else:
            result['status'] = "Not Valid License Key"
            result['msg'] = "Please contact the CableFree support team to get a valid license.  Machine ID: %s" % (machineId)
        return result
    except Exception as e:
        print(f"License Error", e)   
        return "No License key"