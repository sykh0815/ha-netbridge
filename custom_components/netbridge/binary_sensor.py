"""Uplink-Status."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from .const import DOMAIN
from .entity import NetBridgeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([NetBridgeUplink(hass.data[DOMAIN][entry.entry_id], "link", "Uplink")])


class NetBridgeUplink(NetBridgeEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("link") == "ON"
