"""Jedes verbundene WLAN-Geraet als eigener Tracker."""
from __future__ import annotations

from homeassistant.components.device_tracker import ScannerEntity, SourceType

from .const import DOMAIN
from .devices import device_label, find_device, track_new_devices
from .entity import NetBridgeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    track_new_devices(entry, coordinator, async_add_entities, NetBridgeDeviceTracker)


class NetBridgeDeviceTracker(NetBridgeEntity, ScannerEntity):
    _attr_source_type = SourceType.ROUTER

    def __init__(self, coordinator, mac: str) -> None:
        dev = find_device(coordinator, mac) or {"mac": mac}
        super().__init__(coordinator, f"dev_{mac}", device_label(dev))
        self._mac = mac

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def _dev(self) -> dict | None:
        return find_device(self.coordinator, self._mac)

    @property
    def is_connected(self) -> bool:
        return self._dev is not None

    @property
    def mac_address(self) -> str:
        return self._mac

    @property
    def ip_address(self) -> str | None:
        return (self._dev or {}).get("ip") or None

    @property
    def hostname(self) -> str | None:
        return (self._dev or {}).get("name")

    @property
    def extra_state_attributes(self):
        dev = self._dev
        if not dev:
            return None
        return {k: dev[k] for k in ("rssi", "vendor", "phy", "since") if k in dev}
