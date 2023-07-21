# Copyright (C) 2021-2022 Luis López <luis@cuarentaydos.com>
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


import enum
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import globalomnium
from homeassistant.core import dt_util
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .barrier import Barrier, BarrierDeniedError
from .const import (
    DATA_ATTR_HISTORICAL_CONSUMPTION,
    # DATA_ATTR_HISTORICAL_GENERATION,
    # DATA_ATTR_HISTORICAL_POWER_DEMAND,
    DATA_ATTR_MEASURE_ACCUMULATED,
    DATA_ATTR_MEASURE_INSTANT,
    HISTORICAL_PERIOD_LENGHT,
)
from .entity import GOEntity


class DataSetType(enum.IntFlag):
    NONE = 0
    MEASURE = 1 << 0
    HISTORICAL_CONSUMPTION = 1 << 1
    # HISTORICAL_GENERATION = 1 << 2 #comentar o borrar???
    # HISTORICAL_POWER_DEMAND = 1 << 3 #comentar o borrar???

    ALL = 0b1111 #afectará a esto si modifico lo de arriba?


_LOGGER = logging.getLogger(__name__)

_DEFAULT_COORDINATOR_DATA: dict[str, Any] = {
    DATA_ATTR_MEASURE_ACCUMULATED: None,
    DATA_ATTR_MEASURE_INSTANT: None,
    DATA_ATTR_HISTORICAL_CONSUMPTION: {
        "accumulated": None,
#         "accumulated-co2": None,
        "historical": [],
    },
#     DATA_ATTR_HISTORICAL_GENERATION: {
#         "accumulated": None,
#         "accumulated-co2": None,
#         "historical": [],
#     },
#     DATA_ATTR_HISTORICAL_POWER_DEMAND: [],
}


class GOCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass,
        api,
        barriers: dict[DataSetType, Barrier],
        update_interval: timedelta = timedelta(seconds=30),
    ):
        name = (
            f"{api.username}/{api._contract} coordinator" if api else "GO coordinator" #¿cambiar contract por referencia? creo que no
        )
        super().__init__(hass, _LOGGER, name=name, update_interval=update_interval)

        self.api = api
        self.barriers = barriers

        # FIXME: platforms from HomeAssistant should have types
        self.platforms: list[str] = []

        self.sensors: list[GOEntity] = []

    def register_sensor(self, sensor: GOEntity) -> None:
        self.sensors.append(sensor)
        _LOGGER.debug(f"Registered sensor '{sensor.__class__.__name__}'")

    def unregister_sensor(self, sensor: GOEntity) -> None:
        _LOGGER.debug(f"Unregistered sensor '{sensor.__class__.__name__}'")
        self.sensors.remove(sensor)

    def update_internal_data(self, data: dict[str, Any]):
        if self.data is None:  # type: ignore[has-type]
            self.data = _DEFAULT_COORDINATOR_DATA

        self.data.update(data)

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.

        See: https://developers.home-assistant.io/docs/integration_fetching_data/
        """

        # Raising 'asyncio.TimeoutError' or 'aiohttp.ClientError' are already
        # handled by the data update coordinator.

        # Raising ConfigEntryAuthFailed will cancel future updates
        # and start a config flow with SOURCE_REAUTH (async_step_reauth)

        # Raise UpdateFailed is something were wrong

        ds = DataSetType.NONE
        for sensor in self.sensors:
            for s_ds in sensor.GO_DATA_SETS:
                ds = ds | s_ds

        dsstr = ds.name.replace("|", ", ")
        _LOGGER.debug(f"Request update for datasets: {dsstr}")

        updated_data = await self._async_update_data_raw(datasets=ds)

        data = (self.data or _DEFAULT_COORDINATOR_DATA) | updated_data
        return data

    async def _async_update_data_raw(
        self, datasets: DataSetType = DataSetType.ALL, now: datetime | None = None
    ) -> dict[str, Any]:
        now = now or dt_util.utcnow()
        if now.tzinfo != timezone.utc:
            raise ValueError("now is missing tzinfo field")

        requested = (x for x in DataSetType)
        requested = (x for x in requested if x is not DataSetType.ALL)
        requested = (x for x in requested if x & datasets)
        requested = list(requested)  # type: ignore[assignment]

        data = {}

        for dataset in requested:
            # Barrier checks and handle exceptions
            try:
                self.barriers[dataset].check()

            except KeyError:
                _LOGGER.debug(f"update ignored for {dataset.name}: no barrier defined")
                continue

            except BarrierDeniedError as deny:
                _LOGGER.debug(f"update denied for {dataset.name}: {deny.reason}")
                continue

            _LOGGER.debug(f"update allowed for {dataset.name}")

            # API calls and handle exceptions
            try:
                if dataset is DataSetType.MEASURE:
                    data.update(await self.get_direct_reading_data())

                elif dataset is DataSetType.HISTORICAL_CONSUMPTION:
                    data.update(await self.get_historical_consumption_data())

#                 elif dataset is DataSetType.HISTORICAL_GENERATION:
#                     data.update(await self.get_historical_generation_data())
# 
#                 elif dataset is DataSetType.HISTORICAL_POWER_DEMAND:
#                     data.update(await self.get_historical_power_demand_data())

                else:
                    _LOGGER.debug(
                        f"update ignored for {dataset.name}: not implemented yet"
                    )
                    continue

            except UnicodeDecodeError:
                _LOGGER.debug(
                    f"update error for {dataset.name}: invalid encoding. File a bug"
                )
                continue

            except globalomnium.RequestFailedError as e:
                _LOGGER.debug(
                    f"update error for {dataset.name}: "
                    + f"{e.response.reason} ({e.response.status})"
                )
                continue

            except globalomnium.CommandError as e:
                _LOGGER.debug(
                    f"update error for {dataset.name}: command error from API ({e!r})"
                )
                continue

            except Exception as e:
                _LOGGER.debug(
                    f"update error for {dataset.name}: "
                    f"**FIXME** handle {dataset.name} raised exception: {e!r}"
                )
                continue

            self.barriers[dataset].success()

            _LOGGER.debug(f"update successful for {dataset.name}")

        # delay = random.randint(DELAY_MIN_SECONDS * 10, DELAY_MAX_SECONDS * 10) / 10
        # _LOGGER.debug(f"  → Random delay: {delay} seconds")
        # await asyncio.sleep(delay)

        return data

    async def get_direct_reading_data(self) -> dict[str, int | float]:
        data = await self.api.action_getDatosLecturaHorariaEntreFechas()

        return {
            DATA_ATTR_MEASURE_ACCUMULATED: data.accumulate,
            DATA_ATTR_MEASURE_INSTANT: data.instant,
        }

    async def get_historical_consumption_data(self) -> Any:
        end = datetime.today() # ¿cambiar formato de fecha?
        start = end - HISTORICAL_PERIOD_LENGHT #¿cambiar formato de fecha?
        data = await self.api.action_getDatosLecturaHorariaEntreFechas(start=start, end=end)

        return {DATA_ATTR_HISTORICAL_CONSUMPTION: data}

#     async def get_historical_generation_data(self) -> Any:
#         end = datetime.today()
#         start = end - HISTORICAL_PERIOD_LENGHT
#         data = await self.api.get_historical_generation(start=start, end=end)
# 
#         return {DATA_ATTR_HISTORICAL_GENERATION: data}
# 
#     async def get_historical_power_demand_data(self) -> Any:
#         data = await self.api.get_historical_power_demand()
# 
#        return {DATA_ATTR_HISTORICAL_POWER_DEMAND: data}
