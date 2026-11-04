"""Taste: Neustart."""
from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity

from .const import DOMAIN
from .devices import device_label, find_device, track_new_devices
from .entity import NetBridgeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NetBridgeRestart(coordinator, "restart", "Restart")])
    track_new_devices(entry, coordinator, async_add_entities, NetBridgeKick)


class NetBridgeRestart(NetBridgeEntity, ButtonEntity):
    _attr_device_class = ButtonDeviceClass.RESTART

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_press(self) -> None:
        await self.coordinator.api.restart()


class NetBridgeKick(NetBridgeEntity, ButtonEntity):
    """Meldet ein WLAN-Geraet vom Access Point ab."""

    _attr_icon = "mdi:wifi-off"

    def __init__(self, coordinator, mac: str) -> None:
        dev = find_device(coordinator, mac) or {"mac": mac}
        super().__init__(coordinator, f"kick_{mac}", f"Disconnect {device_label(dev)}")
        self._mac = mac

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and find_device(self.coordinator, self._mac) is not None

    async def async_press(self) -> None:
        await self.coordinator.api.kick(self._mac)
        await self.coordinator.async_request_refresh()
