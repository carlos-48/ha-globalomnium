#
# Copyright (C) 2021 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import os
from typing import Any

import globalomnium
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback  # noqa: F401
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from . import _LOGGER
from .const import CONF_CONTRACT, CONFIG_ENTRY_VERSION, DOMAIN

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, default=os.environ.get("HASS_GO_USERNAME")): str,
        vol.Required(CONF_PASSWORD, default=os.environ.get("HASS_GO_PASSWORD")): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    VERSION = CONFIG_ENTRY_VERSION

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = {}
        self.api = None

    # @staticmethod
    # @callback
    # def async_get_options_flow(config_entry):
    #     return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            # Not used correctly, check
            # https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#unique-ids
            #
            # await self.async_set_unique_id(user_input[CONF_NAME])
            # self._abort_if_unique_id_configured()

            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            try:
                self.api = await create_api(self.hass, username, password)

            except globalomnium.ClientError:
                errors["base"] = "invalid_auth"

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            else:
                self.info.update(
                    {
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    }
                )
                return await self.async_step_contract()

        return self.async_show_form(
            step_id="user",
            data_schema=AUTH_SCHEMA,
            errors=errors,
        )

    async def async_step_contract(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        contracts = await self.api.action_getSuministros() #OJO pendiente ver como se obtienen los diferentes suministros en la API de GLOBAL OMNIUM
        contracts = {f"{x['referencia']} ({x['direccion']})": x for x in contracts} #OJO pendiente ver como se obtienen los diferentes suministros en la API de GLOBAL OMNIUM

        schema = vol.Schema({vol.Required(CONF_CONTRACT): vol.In(contracts.keys())})

        if not user_input:
            return self.async_show_form(step_id="contract", data_schema=schema)

        contract = contracts[user_input["contract"]]
        self.info.update(
            {
                CONF_CONTRACT: contract["referencia"],
            }
        )

        title = "REF " + contract["referencia"]
        return self.async_create_entry(title=title, data=self.info)


# class OptionsFlowHandler(config_entries.OptionsFlow):
#     def __init__(self, config_entry):
#         """Initialize options flow."""
#         self.config_entry = config_entry
#
#     async def async_step_init(self, user_input=None):
#         if user_input is not None:
#             return self.async_create_entry(title="", data=user_input)
#
#         OPTIONS_SCHEMA = vol.Schema({})
#
#         return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)


async def create_api(hass, username, password):
    sess = async_create_clientsession(hass)
    client = globalomnium.Client(sess, username, password)

    await client.login()
    return client
