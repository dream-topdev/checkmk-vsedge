#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Checks based on the CF-PRIVATE-MIB for the Barracuda CloudGen Firewall.
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

# Example device summary from SNMP data:
# .1.3.6.1.4.1.14988.1.1.1.3.1.7.1 --> mikrotik::mtxrWlApFreq.1
# .1.3.6.1.4.1.14988.1.1.1.3.1.7.2 --> mikrotik::mtxrWlApFreq.2
# .1.3.6.1.4.1.14988.1.1.1.3.1.8.1 --> mikrotik::mtxrWlApBand.1
# .1.3.6.1.4.1.14988.1.1.1.3.1.8.2 --> mikrotik::mtxrWlApBand.2
# .1.3.6.1.4.1.14988.1.1.1.3.1.4.1 --> mikrotik::mtxrWlApSsid.1
# .1.3.6.1.4.1.14988.1.1.1.3.1.4.2 --> mikrotik::mtxrWlApSsid.2

from cmk.gui.i18n import _
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


def parse_mikrotik_wireless(string_table):
    return {
        'wirelessFrequency1': string_table[0][0],
        'wirelessFrequency2': string_table[0][1],
        'wirelessBand1': string_table[0][2],
        'wirelessBand2': string_table[0][3],
        'wirelessSsid1': string_table[0][4],
        'wirelessSsid2': string_table[0][5]
    }

register.snmp_section(
    name='mikrotik_wireless',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "RouterOS"),
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.14988.1.1.1.3.1',
        oids=[
            '7.1',  #wirelessFrequency1
            '7.2',  #wirelessFrequency2
            '8.1',  #wirelessBand1
            '8.2',  #wirelessBand2
            '4.1',  #wirelessSsid1
            '4.2',  #wirelessSsid2
        ],
    ),    
    parse_function=parse_mikrotik_wireless,
)


def discovery_mikrotik_wireless(section):
    if section:
        yield Service()


def check_mikrotik_wireless(params, section):
    summary = 'Wireless frequency (1) is %s MHz. Wireless frequency (2) is %s MHz. Wireless band (1) is %s. Wireless band (2) is %s. Wireless network ID (1) is %s. Wireless network ID (2) is %s.' % (section['wirelessFrequency1'], section['wirelessFrequency2'], section['wirelessBand1'], section['wirelessBand2'], section['wirelessSsid1'], section['wirelessSsid2'])
    yield Result(state=State.OK, summary=summary)


register.check_plugin(
    name='mikrotik_wireless',
    service_name='Wireless',
    discovery_function=discovery_mikrotik_wireless,
    check_function=check_mikrotik_wireless,
    check_ruleset_name='mikrotik',
    check_default_parameters={},
)
