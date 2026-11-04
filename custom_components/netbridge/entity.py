"""Gemeinsame Basisklasse."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NetBridgeCoordinator


class NetBridgeEntity(CoordinatorEntity[NetBridgeCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: NetBridgeCoordinator, key: str, name: str) -> None:
        super().__init__(coordinator)
        node = coordinator.data.get("id", coordinator.entry.entry_id)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{node}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, node)},
            name="NetBridge",
            manufacturer="WT32-ETH01-NetBridge",
            model="WT32-ETH01",
            sw_version=coordinator.data.get("version"),
            configuration_url=f"http://{coordinator.entry.data['host']}/",
        )

    @property
    def available(self) -> bool:
        return super().available and self._key_present()

    def _key_present(self) -> bool:
        return self._key in (self.coordinator.data or {})
