"""Schalter fuer das Display."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import NetBridgeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([NetBridgeDisplay(hass.data[DOMAIN][entry.entry_id], "display", "Display")])


class NetBridgeDisplay(NetBridgeEntity, SwitchEntity):
    _attr_icon = "mdi:monitor"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("display") == "ON"

    async def async_turn_on(self, **kwargs) -> None:
        self.coordinator.async_set_updated_data(await self.coordinator.api.set_display(True))

    async def async_turn_off(self, **kwargs) -> None:
        self.coordinator.async_set_updated_data(await self.coordinator.api.set_display(False))
