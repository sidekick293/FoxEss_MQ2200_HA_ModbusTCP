"""MQ2200MH sensor entities."""

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, UnitOfPower, UnitOfEnergy, PERCENTAGE
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = [
    ("total_pv_power", "PV power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("active_power", "Active power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("battery_power", "Battery power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("battery_soc", "Battery SOC", PERCENTAGE, SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT),
    ("pv_total_energy", "PV energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("battery_total_charge_energy", "Battery charge energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("battery_total_discharge_energy", "Battery discharge energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("grid_total_export_energy", "Grid export energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("grid_total_import_energy", "Grid import energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
]


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up sensor platform from config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    host = entry.data[CONF_HOST]

    async_add_entities(
        MQ2200MHSensor(coordinator, entry, host, *s) for s in SENSORS
    )


class MQ2200MHSensor(CoordinatorEntity, SensorEntity):
    """A single MQ2200MH sensor."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, host, key, name, unit, device_class, state_class):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"MQ2200MH ({host})",
            manufacturer="Fox ESS",
            model="MQ2200MH",
        )

    @property
    def native_value(self):
        if self.coordinator.data and self._key in self.coordinator.data:
            val = self.coordinator.data[self._key]
            return round(val, 2) if isinstance(val, float) else val
        return None
