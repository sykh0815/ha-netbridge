"""Schalter fuer das Display."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .devices import device_label, find_device, track_new_devices
from .entity import NetBridgeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NetBridgeDisplay(coordinator, "display", "Display")])
    track_new_devices(entry, coordinator, async_add_entities, NetBridgeBlock)


class NetBridgeDisplay(NetBridgeEntity, SwitchEntity):
    _attr_icon = "mdi:monitor"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("display") == "ON"

    async def async_turn_on(self, **kwargs) -> None:
        self.coordinator.async_set_updated_data(await self.coordinator.api.set_display(True))

    async def async_turn_off(self, **kwargs) -> None:
        self.coordinator.async_set_updated_data(await self.coordinator.api.set_display(False))


class NetBridgeBlock(NetBridgeEntity, SwitchEntity):
    """Sperrt ein WLAN-Geraet: es wird direkt nach dem Verbinden wieder abgemeldet."""

    _attr_icon = "mdi:cancel"

    def __init__(self, coordinator, mac: str) -> None:
        dev = find_device(coordinator, mac) or {"mac": mac}
        super().__init__(coordinator, f"block_{mac}", f"Block {device_label(dev)}")
        self._mac = mac

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool:
        return self._mac in [m.lower() for m in self.coordinator.data.get("blocked", [])]

    async def async_turn_on(self, **kwargs) -> None:
        self.coordinator.async_set_updated_data(await self.coordinator.api.block(self._mac, True))

    async def async_turn_off(self, **kwargs) -> None:
        self.coordinator.async_set_updated_data(await self.coordinator.api.block(self._mac, False))
