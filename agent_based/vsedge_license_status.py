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
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Example excerpt from SNMP data:
# .1.3.6.1.4.1.65535.1.1.2.0 --> CF-PRIVATE::productName

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    SNMPTree,
    exists,
    Service,
    check_levels,
    startswith,
    Result,
    State,
    render
)
from cmk.base.plugins.agent_based import vsedge_license_core
 
def parse_license_status(string_table):
    return {
        'productName': string_table[0][0],
    }

register.snmp_section(
    name='license_status',
    detect = startswith(".1.3.6.1.2.1.2.2.1.2.1", "fxp0"),
    fetch=SNMPTree(
        base='.1.3.6.1.2.1.2.2.1.2',
        oids=[
            '1',  #Kernel Desc
        ],
    ),
    parse_function=parse_license_status,
)


def discovery_license_status(section):
    if section:
        yield Service()


def check_license_status(params, section):    
    licenseResult = vsedge_license_core.doCheckinglicense()
    if (licenseResult['status'] != "OK"):
        yield Result(state=State.CRIT, summary=licenseResult['msg'])
        return
    if (licenseResult['daysLeft'] < 10):
        yield Result(state=State.WARN, summary='%d days left. Software license will expire on %s. Please contact the CableFree support team.' % (licenseResult['daysLeft'], licenseResult['expiredAt']))
        return
    yield Result(state=State.OK, summary='You have a valid software license. Your software license will operate until %s.' % (licenseResult['expiredAt']))


register.check_plugin(
    name='vsedge_license_status',
    service_name='License status',
    discovery_function=discovery_license_status,
    check_function=check_license_status,
    check_ruleset_name='license',
    check_default_parameters={},
)