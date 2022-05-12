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


def parse_vsedge(string_table):
    return {
        'productName': string_table[0][0],
    }

register.snmp_section(
    name='vsedge',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Linux vsedge"),
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.65535.1.1',
        oids=[
            '2.0',  #productName
        ],
    ),
    parse_function=parse_vsedge,
)


def discovery_vsedge(section):
    if section:
        yield Service()


def check_vsedge(params, section):
    if section['productName'] == "vsedge":
        summary = 'Device Type is VSEdge.'
    else:
        summary = "Device Type is CF-IR."
    yield Result(state=State.OK, summary=summary)


register.check_plugin(
    name='vsedge',
    service_name='Device Type',
    discovery_function=discovery_vsedge,
    check_function=check_vsedge,
    check_ruleset_name='vsedge',
    check_default_parameters={},
)