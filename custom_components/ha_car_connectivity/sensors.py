from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.entity import Entity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    vehicles = data["vehicles"]

    entities = []

    for vehicle in vehicles:
        status = await api.get_vehicle_status(vehicle["vin"])

        if "battery" in status:
            entities.append(CarBatterySensor(api, vehicle))

        if "range" in status:
            entities.append(CarRangeSensor(api, vehicle))

        if "doors" in status:
            entities.append(CarDoorLockSensor(api, vehicle))

    async_add_entities(entities)



"""
async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([BatterySensor(coordinator)])


class BatterySensor(SensorEntity):

    def __init__(self, coordinator):

        self.coordinator = coordinator

        self._attr_name = "VW Battery SOC"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):"""
        return self.coordinator.data["soc"]

    async def async_update(self):
        await self.coordinator.async_request_refresh()
