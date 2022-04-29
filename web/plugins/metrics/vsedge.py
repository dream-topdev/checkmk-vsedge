#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2021  Marius Rieder <marius.rieder@durchmesser.ch>
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

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import metric_info, check_metrics, perfometer_info, MB

metric_info["vsedge"] = {
    "title": _("VSEdge Users"),
    "unit": "count",
    "color": "#1DB1FF",
}

check_metrics["check_mk-vsedge"] = {
    "users": {
        "name": "vsedge",
    },
}

perfometer_info.append({
    "type": "logarithmic",
    "metric": "vsedge",
    "half_value": 10,
    "exponent": 2,
})