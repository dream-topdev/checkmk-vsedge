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
# .1.3.6.1.2.1.1.7.0 --> CF-PRIVATE::deviceIp
# .1.3.6.1.2.1.1.7.1 --> CF-PRIVATE::productName
# .1.3.6.1.2.1.1.7.2 --> CF-PRIVATE::deviceUptime
# .1.3.6.1.2.1.1.7.3 --> CF-PRIVATE::serialNo
# .1.3.6.1.2.1.1.7.4 --> CF-PRIVATE::firmwareVersion

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
)


def parse_vsedge_wireless(string_table):
    return {
        'wirelessMode': string_table[0][0],
        'wirelessFrequency': string_table[0][1],
        'wirelessWidth': string_table[0][2],
        'wirelessSignal': string_table[0][3],
        'wirelessSsid': string_table[0][4]
    }

register.snmp_section(
    name='vsedge_wireless',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Linux vsedge"),
    fetch=SNMPTree(
        base='.1.3.6.1.2.1.1.7',
        oids=[
            '0',  #wirelessMode
            '1',  #wirelessFrequency
            '2',  #wirelessWidth
            '3',  #wirelessSignal
            '4',  #wirelessSsid
        ],
    ),    
    parse_function=parse_vsedge_wireless,
)


def discovery_vsedge_wireless(section):
    if section:
        yield Service()


def check_vsedge_wireless(params, section):
    summary = 'Wireless operation mode is %s. Wireless frequency is %s. Wireless channel width is %s. Wireless signal level is %s. Wireless network ID is %s.' % (section['wirelessMode'], section['wirelessFrequency'], section['wirelessWidth'], section['wirelessSignal'], section['wirelessSsid'])
    yield Result(state=State.OK, summary=summary)


register.check_plugin(
    name='vsedge_wireless',
    service_name='VSEDGE Wireless',
    discovery_function=discovery_vsedge_wireless,
    check_function=check_vsedge_wireless,
    check_ruleset_name='vsedge',
    check_default_parameters={},
)
