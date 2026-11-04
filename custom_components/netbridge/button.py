"""Taste: Neustart."""
from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity

from .const import DOMAIN
from .entity import NetBridgeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([NetBridgeRestart(hass.data[DOMAIN][entry.entry_id], "restart", "Restart")])


class NetBridgeRestart(NetBridgeEntity, ButtonEntity):
    _attr_device_class = ButtonDeviceClass.RESTART

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_press(self) -> None:
        await self.coordinator.api.restart()
