import logging
_LOGGER = logging.getLogger(__name__)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

#from .coordinator import VWCoordinator
from .const import DOMAIN

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from carconnectivity.carconnectivity import CarConnectivity
import carconnectivity_connectors.volkswagen

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    #config = entry.data

    config = {
        "carConnectivity": {
            "connectors": [
                {
                    "connectorId": "vw",
                    "type": "volkswagen",
                    "config": {
                        "username": entry.data["username"],
                        "password": entry.data["password"],
                        "country": "SE", 
                        "brand": "vW",
                        "region": "emea",
                    },
                }
            ]
        }
    }   

    # Kör blocking init i executor
    try:
        cc = await hass.async_add_executor_job(
            CarConnectivity,
            config
        )
    
    except Exception as e:
        _LOGGER.error("CarConnectivity init failed: %s", e)
        raise    

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = cc

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop(entry.entry_id)
    return True


