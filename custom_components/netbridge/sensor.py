"""Sensoren."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, SIGNAL_STRENGTH_DECIBELS_MILLIWATT, UnitOfElectricPotential, UnitOfTime
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .entity import NetBridgeEntity

# key, Name, Einheit, Geraeteklasse, Zustandsklasse, Kategorie, nur im AP-Modus
SENSORS = [
    ("down", "Download rate", "Mbit/s", SensorDeviceClass.DATA_RATE, SensorStateClass.MEASUREMENT, None, False),
    ("up", "Upload rate", "Mbit/s", SensorDeviceClass.DATA_RATE, SensorStateClass.MEASUREMENT, None, False),
    ("heap", "Free heap", "kB", None, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC, False),
    ("cpu", "CPU load", PERCENTAGE, None, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC, False),
    ("uptime", "Uptime", UnitOfTime.SECONDS, SensorDeviceClass.DURATION, None, EntityCategory.DIAGNOSTIC, False),
    ("mode", "Mode", None, None, None, EntityCategory.DIAGNOSTIC, False),
    ("clients", "WiFi devices", None, None, SensorStateClass.MEASUREMENT, None, True),
    ("channel", "WiFi channel", None, None, None, EntityCategory.DIAGNOSTIC, True),
    ("rssi", "WiFi signal", SIGNAL_STRENGTH_DECIBELS_MILLIWATT, SensorDeviceClass.SIGNAL_STRENGTH, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC, False),
    ("drops", "Dropped frames", None, None, SensorStateClass.TOTAL_INCREASING, EntityCategory.DIAGNOSTIC, True),
    ("lan_restarts", "LAN restarts", None, None, SensorStateClass.TOTAL_INCREASING, EntityCategory.DIAGNOSTIC, True),
    ("voltage", "Supply voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC, False),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data
    entities = []
    for key, name, unit, dclass, sclass, category, ap_only in SENSORS:
        if key not in data:  # z. B. Spannung nur bei aktiver Messung
            continue
        if ap_only and not data.get("ap"):
            continue
        if key == "rssi" and data.get("ap"):
            continue
        entities.append(NetBridgeSensor(coordinator, key, name, unit, dclass, sclass, category))
    async_add_entities(entities)


class NetBridgeSensor(NetBridgeEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit, dclass, sclass, category) -> None:
        super().__init__(coordinator, key, name)
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = dclass
        self._attr_state_class = sclass
        self._attr_entity_category = category

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

    @property
    def extra_state_attributes(self):
        # Verbundene WLAN-Geraete als Attribut des Sensors "WiFi devices"
        if self._key == "clients":
            return {"devices": self.coordinator.data.get("devices", [])}
        return None
