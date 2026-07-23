"""Config flow for MQ2200MH Control integration."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DOMAIN, DEFAULT_PORT, DEFAULT_DEVICE_ID, DEFAULT_SCAN_INTERVAL
from .modbus import read_registers


class MQ2200MHConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for MQ2200MH Control."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the setup form."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            device_id = user_input["device_id"]

            # Test connection by reading a register
            can_connect = await self.hass.async_add_executor_job(
                read_registers, host, port, 39424, 1, device_id
            )

            if can_connect is not None:
                # Prevent duplicate entries for the same host
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"MQ2200MH ({host})",
                    data=user_input,
                )

            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional("device_id", default=DEFAULT_DEVICE_ID): int,
                vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
            }),
            errors=errors,
        )
