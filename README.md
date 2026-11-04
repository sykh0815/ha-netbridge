# WT32-ETH01 NetBridge for Home Assistant

🇬🇧 **English** | 🇩🇪 [Deutsch](README.de.md)

HACS integration for the [WT32-ETH01-NetBridge](https://github.com/sykh0815/WT32-ETH01-NetBridge) firmware (version 3.24.0 or newer). No MQTT broker needed: Home Assistant polls the device over HTTP every 10 s.

## Installation
1. HACS → ⋮ → *Custom repositories* → add this repository as type *Integration*.
2. Install "WT32-ETH01 NetBridge" and restart Home Assistant.
3. The device is discovered automatically (mDNS). Otherwise: *Settings → Devices & services → Add integration → NetBridge*.
4. Enter the **access token** shown in the NetBridge web interface (section "Home Assistant") and, if discovery is not used, the device's IP address.

## Entities
Every connected WiFi device additionally gets its own device tracker and a "Disconnect" button (kicks it from the access point) plus a "Block" switch (the device is disconnected again right after every connection attempt; the list is stored on the device). Entities are created when a device is first seen and stay afterwards.

Uplink, download/upload rate, free heap, CPU load, uptime, mode, WiFi devices (attribute `devices` = list with MAC, IP, name, signal), WiFi channel / WiFi signal, dropped frames and LAN restarts (AP bridge), supply voltage (if enabled), switch "Display", button "Restart".

The device needs an IP in the home network (NAT and access point modes).
