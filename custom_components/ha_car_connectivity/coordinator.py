import logging
import DOMAIN from .const

from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from carconnectivity import CarConnectivity
import carconnectivity_connectors.volkswagen

from .const import CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

class VolkswagenCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            logger=__import__(__name__),
            name="Volkswagen coordinator",
            update_interval=timedelta(minutes=5),
        )

        self.entry = entry
        self.cc = hass.data[DOMAIN][entry.entry_id]

    async def _async_update_data(self):
        # Kör blocking update i executor
        await self.hass.async_add_executor_job(self.cc.update)

        # Returnera data du vill exponera
        return self.cc

