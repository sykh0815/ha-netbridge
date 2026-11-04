"""Gemeinsame Hilfen fuer die einzelnen WLAN-Geraete."""
from __future__ import annotations

from homeassistant.core import callback


def device_label(dev: dict) -> str:
    return dev.get("name") or dev.get("vendor") or dev["mac"]


def find_device(coordinator, mac: str) -> dict | None:
    for dev in (coordinator.data or {}).get("devices", []):
        if dev["mac"].lower() == mac:
            return dev
    return None


@callback
def track_new_devices(entry, coordinator, add_entities, factory) -> None:
    """Legt fuer jedes neu gesehene WLAN-Geraet eine Entitaet an (bleibt danach bestehen)."""
    known: set[str] = set()

    @callback
    def _add() -> None:
        new = []
        data = coordinator.data or {}
        macs = [dev["mac"].lower() for dev in data.get("devices", [])] + [m.lower() for m in data.get("blocked", [])]
        for mac in macs:
            if mac not in known:
                known.add(mac)
                new.append(factory(coordinator, mac))
        if new:
            add_entities(new)

    entry.async_on_unload(coordinator.async_add_listener(_add))
    _add()
