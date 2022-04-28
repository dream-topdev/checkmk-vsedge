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
# .1.3.6.1.4.1.10704.1.11 47 --> PHION-MIB::vpnUsers

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    SNMPTree,
    exists,
    Service,
    check_levels,
    startswith
)
register.snmp_section(
    name='vsedge',
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Linux vsedge"),
    fetch=SNMPTree(
        base='.1.3.6.1.2.1.1.7',
        oids=[
            '0',  #
        ],
    )
)


def discovery_vsedge(section):
    if section:
        yield Service()


def check_vsedge(params, section):
    if section:
        users = int(section[0][0])

        yield from check_levels(
            users,
            levels_upper=params.get('users', None),
            label='Linux vsedge',
            metric_name='users',
            render_func=lambda v: "%d" % v
        )


register.check_plugin(
    name='vsedge',
    service_name='Linux vsedge',
    discovery_function=discovery_vsedge,
    check_function=check_vsedge,
    check_ruleset_name='vsedge',
    check_default_parameters={},
)
