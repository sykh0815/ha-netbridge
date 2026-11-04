"""Einrichtung: automatisch per mDNS oder manuell mit IP/Name und Token."""
from __future__ import annotations

from aiohttp import ClientError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo

from .const import CONF_TOKEN, DOMAIN


async def _fetch(hass, host: str, token: str) -> dict:
    session = async_get_clientsession(hass)
    async with session.get(f"http://{host}/api/state", params={"token": token}, timeout=10) as resp:
        if resp.status == 401:
            raise PermissionError
        resp.raise_for_status()
        return await resp.json(content_type=None)


class NetBridgeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._host: str | None = None

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo) -> ConfigFlowResult:
        node = discovery_info.properties.get("id") or discovery_info.hostname.split(".")[0]
        await self.async_set_unique_id(node)
        self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})
        self._host = discovery_info.host
        self.context["title_placeholders"] = {"name": node}
        return await self.async_step_user()

    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            try:
                data = await _fetch(self.hass, host, user_input[CONF_TOKEN].strip())
            except PermissionError:
                errors["base"] = "invalid_auth"
            except (ClientError, TimeoutError, ValueError):
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(data["id"])
                self._abort_if_unique_id_configured(updates={CONF_HOST: host})
                return self.async_create_entry(
                    title=f"NetBridge ({data['id']})",
                    data={CONF_HOST: host, CONF_TOKEN: user_input[CONF_TOKEN].strip()},
                )
        schema = vol.Schema({
            vol.Required(CONF_HOST, default=self._host or ""): str,
            vol.Required(CONF_TOKEN): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
