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
# .1.3.6.1.4.1.14988.1.1.1.3.1.2.1 --> mikrotik::mtxrWlApTxRate.1
# .1.3.6.1.4.1.14988.1.1.1.3.1.3.1 --> mikrotik::mtxrWlApRxRate.1
# .1.3.6.1.4.1.14988.1.1.14.1.1.61.3 --> mikrotik::mtxrinterfaceStatsTxBytes.3
# .1.3.6.1.4.1.14988.1.1.14.1.1.31.3 --> mikrotik::mtxrinterfaceStatsRxBytes.3

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


def parse_mikrotik_traffic(string_table):
    return {
        'currentTx': string_table[0][0],
        'currentRx': string_table[0][1],
        'totalTx': string_table[0][2],
        'totalRx': string_table[0][3]
    }

register.snmp_section(
    name='mikrotik_traffic',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "RouterOS"),
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.14988.1.1',
        oids=[
            '1.3.1.2.1',  #currentTx
            '1.3.1.3.1',  #currentRx
            '14.1.1.61.3',  #totalTx
            '14.1.1.31.3',  #totalRx
        ],
    ),    
    parse_function=parse_mikrotik_traffic,
)


def discovery_mikrotik_traffic(section):
    if section:
        yield Service()


def check_mikrotik_traffic(params, section): 
    yield from check_levels(
        int(section['currentTx']),
        levels_upper=params.get('currentTx', None),
        label='Current TX rate',
        metric_name='mikrotik_traffic_currentTx',
        render_func=lambda v: render.iobandwidth(v)
    )

    yield from check_levels(
        int(section['currentRx']),
        levels_upper=params.get('currentRx', None),
        label='Current RX rate',
        metric_name='mikrotik_traffic_currentRx',
        render_func=lambda v: render.iobandwidth(v)
    )

    yield from check_levels(
        int(section['totalTx']),
        levels_upper=params.get('totalTx', None),
        label='Total transmited',
        metric_name='mikrotik_traffic_totalTx',
        render_func=lambda v: render.bytes(v)
    )

    yield from check_levels(
        int(section['totalRx']),
        levels_upper=params.get('totalRx', None),
        label='Total received',
        metric_name='mikrotik_traffic_totalRx',
        render_func=lambda v: render.bytes(v)
    )


register.check_plugin(
    name='mikrotik_traffic',
    service_name='Traffic',
    discovery_function=discovery_mikrotik_traffic,
    check_function=check_mikrotik_traffic,
    check_ruleset_name='mikrotik',
    check_default_parameters={},
)
