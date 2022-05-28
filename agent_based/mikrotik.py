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
# .1.3.6.1.2.1.1.1.0 --> sysDescr

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


def parse_sysDescr(string_table):
    return {
        'productName': string_table[0][0],
    }

register.snmp_section(
    name='mikrotik',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "RouterOS"),
    fetch=SNMPTree(
        base='.1.3.6.1.2.1.1',
        oids=[
            '1.0',  #sysDescr
        ],
    ),
    parse_function=parse_sysDescr,
)


def discovery_mikrotik(section):
    if section:
        yield Service()


def check_mikrotik(params, section):
    summary = 'Device Type is CableFree RadioOS.'    
    yield Result(state=State.OK, summary=summary)


register.check_plugin(
    name='mikrotik',
    service_name='Device Type',
    discovery_function=discovery_mikrotik,
    check_function=check_mikrotik,
    check_ruleset_name='mikrotik',
    check_default_parameters={},
)