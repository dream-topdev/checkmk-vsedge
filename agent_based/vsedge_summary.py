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
# .1.3.6.1.4.1.65535.1.1.1.0 --> CF-PRIVATE::deviceIp
# .1.3.6.1.4.1.65535.1.1.2.0 --> CF-PRIVATE::productName
# .1.3.6.1.4.1.65535.1.1.3.0 --> CF-PRIVATE::deviceUptime
# .1.3.6.1.4.1.65535.1.1.4.0 --> CF-PRIVATE::serialNo
# .1.3.6.1.4.1.65535.1.1.5.0 --> CF-PRIVATE::firmwareVersion

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


def parse_vsedge_summary(string_table):
    return {
        'deviceIP': string_table[0][0],
        'productName': string_table[0][1],
        'deviceUptime': string_table[0][2],
        'serialNo': string_table[0][3],
        'firmwareVersion': string_table[0][4]
    }

register.snmp_section(
    name='vsedge_summary',
    detect = startswith(".1.3.6.1.4.1.65535.1.1.2.0", "vsedge"),
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.65535.1.1',
        oids=[
            '1.0',  #deviceIP
            '2.0',  #productName
            '3.0',  #deviceUptime
            '4.0',  #serialNo
            '5.0',  #firmwareVersion
        ],
    ),    
    parse_function=parse_vsedge_summary,
)


def discovery_vsedge_summary(section):
    if section:
        yield Service()


def check_vsedge_summary(params, section):
    yield from check_levels(
        int(section['deviceUptime']),
        levels_upper=params.get('deviceUptime', None),
        label='Device Up Time',
        metric_name='vsedge_summary_deviceUptime',
        render_func=lambda v: render.timespan(v)
    )
    summary = 'Device IP is %s. Product Name is %s. Serial No is %s. Firmware version is %s.' % (section['deviceIP'], section['productName'], section['serialNo'], section['firmwareVersion'])
    yield Result(state=State.OK, summary=summary)


register.check_plugin(
    name='vsedge_summary',
    service_name='Summary',
    discovery_function=discovery_vsedge_summary,
    check_function=check_vsedge_summary,
    check_ruleset_name='vsedge',
    check_default_parameters={},
)
