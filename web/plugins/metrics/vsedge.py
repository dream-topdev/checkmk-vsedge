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

# metrics for traffic
metric_info["vsedge_traffic_currentTx"] = {
    "title": _("Current TX rate"),
    "unit": "bytes/s",
    "color": "#1DB1FF",
}

metric_info["vsedge_traffic_currentRx"] = {
    "title": _("Current RX rate"),
    "unit": "bytes/s",
    "color": "#1DB1FF",
}

metric_info["vsedge_traffic_totalTx"] = {
    "title": _("Total transmited"),
    "unit": "bytes",
    "color": "#00e060",
}

metric_info["vsedge_traffic_totalRx"] = {
    "title": _("Total received"),
    "unit": "bytes",
    "color": "#00e060",
}

check_metrics["check_mk-vsedge_traffic"] = {
    "currentTx": {
        "name": "vsedge_traffic_currentTx",
    },
    "currentRx": {
        "name": "vsedge_traffic_currentRx",
    },
    "totalTx": {
        "name": "vsedge_traffic_totalTx",
    },
    "totalRx": {
        "name": "vsedge_traffic_totalRx",
    },
}

perfometer_info.append({
    "type": "logarithmic",
    "metric": "vsedge_traffic_currentTx",
    "half_value": 10,
    "exponent": 2.0,
})

# metrics for resource
metric_info["vsedge_resource_cpuUsed"] = {
    "title": _("Current CPU Usage"),
    "unit": "%",
    "color": "#1DB1FF",
}

metric_info["vsedge_resource_memoryUsed"] = {
    "title": _("Current Memory Usage"),
    "unit": "%",
    "color": "#1DB1FF",
}

check_metrics["check_mk-vsedge_traffic"] = {
    "cpuUsed": {
        "name": "vsedge_resource_cpuUsed",
    },
    "memoryUsed": {
        "name": "vsedge_resource_memoryUsed",
    }
}

perfometer_info.append({
    "type": "linear",
    "segments": ["vsedge_resource_cpuUsed"],
    "total": 100.0,
})