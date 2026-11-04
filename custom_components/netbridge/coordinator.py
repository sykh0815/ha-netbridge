"""Datenabfrage beim NetBridge (HTTP, /api/state)."""
from __future__ import annotations

from datetime import timedelta
import logging

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_TOKEN, DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class NetBridgeApi:
    """Kleiner HTTP-Client fuer die Firmware-Schnittstelle."""

    def __init__(self, hass: HomeAssistant, host: str, token: str) -> None:
        self._session = async_get_clientsession(hass)
        self._base = f"http://{host}"
        self._token = token

    async def _request(self, method: str, path: str, **params) -> dict:
        params["token"] = self._token
        async with self._session.request(method, self._base + path, params=params, timeout=10) as resp:
            if resp.status == 401:
                raise ConfigEntryAuthFailed("Token oder Passwort abgelehnt")
            resp.raise_for_status()
            return await resp.json(content_type=None)

    async def state(self) -> dict:
        return await self._request("GET", "/api/state")

    async def set_display(self, on: bool) -> dict:
        return await self._request("POST", "/api/display", on="1" if on else "0")

    async def block(self, mac: str, on: bool) -> dict:
        return await self._request("POST", "/api/block", mac=mac, on="1" if on else "0")

    async def kick(self, mac: str) -> None:
        await self._request("POST", "/api/kick", mac=mac)

    async def restart(self) -> None:
        await self._request("POST", "/api/restart")


class NetBridgeCoordinator(DataUpdateCoordinator[dict]):
    """Fragt den NetBridge regelmaessig ab."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS))
        self.entry = entry
        self.api = NetBridgeApi(hass, entry.data[CONF_HOST], entry.data[CONF_TOKEN])

    async def _async_update_data(self) -> dict:
        try:
            return await self.api.state()
        except ConfigEntryAuthFailed:
            raise
        except (ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"NetBridge nicht erreichbar: {err}") from err
