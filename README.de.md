# WT32-ETH01 NetBridge für Home Assistant

🇬🇧 [English](README.md) | 🇩🇪 **Deutsch**

HACS-Integration für die Firmware [WT32-ETH01-NetBridge](https://github.com/sykh0815/WT32-ETH01-NetBridge) (Version 3.24.0 oder neuer). Kein MQTT-Broker nötig: Home Assistant fragt das Gerät alle 10 s per HTTP ab.

## Installation

[![Öffne deine Home-Assistant-Instanz und dieses Repository in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=sykh0815&repository=ha-netbridge&category=integration)

1. Oben auf den Button klicken: Er öffnet dieses Repository im HACS deiner Home-Assistant-Instanz, dann *Herunterladen* wählen. (Manuell: HACS → ⋮ → *Benutzerdefinierte Repositories* → dieses Repository als Typ *Integration*.)
2. Home Assistant neu starten.
3. Das Gerät wird automatisch gefunden (mDNS). Sonst den Button unten klicken oder *Einstellungen → Geräte & Dienste → Integration hinzufügen → NetBridge*.

   [![Starte die Einrichtung von NetBridge in deiner Home-Assistant-Instanz.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=netbridge)
4. Das **Zugangs-Token** eintragen, das im Webinterface der NetBridge (Abschnitt „Home Assistant“) steht, und bei manueller Einrichtung die IP-Adresse.

## Entitäten
Jedes verbundene WLAN-Gerät bekommt zusätzlich einen eigenen Device-Tracker und eine Taste „Abmelden“ (trennt es vom Access Point) sowie einen Schalter „Sperren“ (das Gerät wird nach jedem Verbindungsversuch sofort wieder abgemeldet; die Liste liegt im Gerät). Die Entitäten entstehen, sobald ein Gerät zum ersten Mal gesehen wird, und bleiben danach bestehen.

Uplink, Download-/Upload-Rate, freier Heap, CPU-Last, Laufzeit, Betriebsart, WLAN-Geräte (Attribut `devices` = Liste mit MAC, IP, Name, Signal), WLAN-Kanal / WLAN-Signal, verworfene Frames und LAN-Neustarts (AP-Bridge), Versorgungsspannung (falls aktiv), Schalter „Display“, Taste „Neustart“.

Das Gerät braucht eine IP im Heimnetz (NAT- und Access-Point-Modi).
