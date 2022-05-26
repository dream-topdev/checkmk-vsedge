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
# metrics for summary


metric_info["mikrotik_summary_deviceUptime"] = {
    "title": _("Device Up Time"),
    "unit": "s",
    "color": "#00e060",
}

check_metrics["check_mk-mikrotik_summary"] = {
    "deviceUptime": {
        "name": "mikrotik_summary_deviceUptime",
    },
}

perfometer_info.append(
    {
        "type": "logarithmic",
        "metric": "mikrotik_summary_deviceUptime",
        "half_value": 2592000.0,
        "exponent": 2,
    }
)

# metrics for traffic
metric_info["mikrotik_traffic_currentTx"] = {
    "title": _("Current TX rate"),
    "unit": "bytes/s",
    "color": "#1DB1FF",
}

metric_info["mikrotik_traffic_currentRx"] = {
    "title": _("Current RX rate"),
    "unit": "bytes/s",
    "color": "#1DB1FF",
}

metric_info["mikrotik_traffic_totalTx"] = {
    "title": _("Total transmited"),
    "unit": "bytes",
    "color": "#00e060",
}

metric_info["mikrotik_traffic_totalRx"] = {
    "title": _("Total received"),
    "unit": "bytes",
    "color": "#00e060",
}

check_metrics["check_mk-mikrotik_traffic"] = {
    "currentTx": {
        "name": "mikrotik_traffic_currentTx",
    },
    "currentRx": {
        "name": "mikrotik_traffic_currentRx",
    },
    "totalTx": {
        "name": "mikrotik_traffic_totalTx",
    },
    "totalRx": {
        "name": "mikrotik_traffic_totalRx",
    },
}

perfometer_info.append(
    {
        "type": "dual",
        "perfometers": [
            {
                "type": "logarithmic",
                "metric": "mikrotik_traffic_currentTx",
                "half_value": 5000,
                "exponent": 2,
            },
            {
                "type": "logarithmic",
                "metric": "mikrotik_traffic_currentRx",
                "half_value": 5000,
                "exponent": 2,
            },
        ],
    }
)

# metrics for resource
metric_info["mikrotik_resource_cpuUsed"] = {
    "title": _("Current CPU Usage"),
    "unit": "%",
    "color": "#1DB1FF",
}

metric_info["mikrotik_resource_memoryUsed"] = {
    "title": _("Current Memory Usage"),
    "unit": "%",
    "color": "#1DB1FF",
}

check_metrics["check_mk-mikrotik_traffic"] = {
    "cpuUsed": {
        "name": "mikrotik_resource_cpuUsed",
    },
    "memoryUsed": {
        "name": "mikrotik_resource_memoryUsed",
    }
}

perfometer_info.append(
    {
        "type": "dual",
        "perfometers": [
            {
                "type": "linear",
                "segments": ["mikrotik_resource_cpuUsed"],
                "total": 100.0,
            },
            {
                "type": "linear",
                "segments": ["mikrotik_resource_memoryUsed"],
                "total": 100.0,
            },
        ],
    }
)


# metrics for wireless
metric_info["mikrotik_wireless_wirelessSignal"] = {
    "title": _("Wireless signal level"),
    "unit": "dbm",
    "color": "#1DB1FF",
}

check_metrics["check_mk-mikrotik_wireless"] = {
    "wirelessSignal": {
        "name": "mikrotik_wireless_wirelessSignal",
    }
}

perfometer_info.append({
    "type": "linear",
    "segments": ["mikrotik_wireless_wirelessSignal"],
    "total": 100.0,
})