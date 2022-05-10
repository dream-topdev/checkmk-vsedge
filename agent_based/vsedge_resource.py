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
# .1.3.6.1.4.1.65535.1.4.1.0 --> CF-PRIVATE::cpuUsed
# .1.3.6.1.4.1.65535.1.4.2.0 --> CF-PRIVATE::memoryUsed

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


def parse_vsedge_resource(string_table):
    return {
        'cpuUsed': string_table[0][0],
        'memoryUsed': string_table[0][1]
    }

register.snmp_section(
    name='vsedge_resource',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Linux vsedge"),
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.65535.1.4',
        oids=[
            '1.0',  #cpuUsed
            '2.0',  #memoryUsed
        ],
    ),    
    parse_function=parse_vsedge_resource,
)


def discovery_vsedge_resource(section):
    if section:
        yield Service()


def check_vsedge_resource(params, section): 
    yield from check_levels(
        int(section['cpuUsed']),
        levels_upper=params.get('cpuUsed', None),
        label='Current cpu usage',
        metric_name='vsedge_resource_cpuUsed',
        render_func=lambda v: render.percent(v)
    )

    yield from check_levels(
        int(section['memoryUsed']),
        levels_upper=params.get('memoryUsed', None),
        label='Current memory usage',
        metric_name='vsedge_resource_memoryUsed',
        render_func=lambda v: render.percent(v)
    )


register.check_plugin(
    name='vsedge_resource',
    service_name='J-P Resource',
    discovery_function=discovery_vsedge_resource,
    check_function=check_vsedge_resource,
    check_ruleset_name='vsedge',
    check_default_parameters={},
)
