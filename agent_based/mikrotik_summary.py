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
# .1.3.6.1.4.1.65535.1.1.1.0 --> 
# .1.3.6.1.4.1.14988.1.1.7.8.0 --> mikrotik::mtxrBoardName
# .1.3.6.1.2.1.25.1.1.0 --> hrSystemUptime
# .1.3.6.1.4.1.14988.1.1.7.3.0 --> mikrotik::serialNo
# .1.3.6.1.4.1.14988.1.1.7.4.0 --> mikrotik::firmwareVersion

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


def parse_mikrotik_summary(string_table):
    return {
        'productName': string_table[0][0],
        'deviceUptime': string_table[0][1],
        'serialNo': string_table[0][2],
        'firmwareVersion': string_table[0][3]
    }

register.snmp_section(
    name='mikrotik_summary',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "RouterOS"),
    fetch=SNMPTree(
        base='.1.3.6.1',
        oids=[
            '4.1.14988.1.1.7.8.0',  #productName
            '2.1.25.1.1.0',  #deviceUptime
            '4.1.14988.1.1.7.3.0',  #serialNo
            '4.1.14988.1.1.7.4.0',  #firmwareVersion
        ],
    ),    
    parse_function=parse_mikrotik_summary,
)


def discovery_mikrotik_summary(section):
    if section:
        yield Service()


def check_mikrotik_summary(params, section):
    yield from check_levels(
        int(section['deviceUptime']),
        levels_upper=params.get('deviceUptime', None),
        label='Device Up Time',
        metric_name='mikrotik_summary_deviceUptime',
        render_func=lambda v: render.timespan(v / 100)
    )
    summary = 'Product Name is %s. Serial No is %s. Firmware version is %s.' % (section['productName'], section['serialNo'], section['firmwareVersion'])
    yield Result(state=State.OK, summary=summary)


register.check_plugin(
    name='mikrotik_summary',
    service_name='Summary',
    discovery_function=discovery_mikrotik_summary,
    check_function=check_mikrotik_summary,
    check_ruleset_name='mikrotik',
    check_default_parameters={},
)
