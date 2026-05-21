"""Support for Salus temperature sensors."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from .coordinator import SalusConfigEntry
from .entity import SalusEntity, async_setup_salus_platform_entities

PARALLEL_UPDATES = 0

STATE_CLASS_BY_DEVICE_CLASS = {
    "battery": SensorStateClass.MEASUREMENT,
    "humidity": SensorStateClass.MEASUREMENT,
    "power": SensorStateClass.MEASUREMENT,
    "temperature": SensorStateClass.MEASUREMENT,
    "energy": SensorStateClass.TOTAL_INCREASING,
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SalusConfigEntry,
    async_add_entities,
) -> None:
    """Set up Salus sensors from a config entry."""
    async_setup_salus_platform_entities(
        config_entry,
        async_add_entities,
        SalusSensor,
        lambda data: data.sensor_devices,
    )


class SalusSensor(SalusEntity, SensorEntity):
    """Representation of a Salus sensor."""

    _data_collection = "sensor_devices"

    @property
    def name(self) -> str | None:
        """Return the entity name."""
        if self._device is None:
            return None
        return self._child_entity_name(self._device)

    def _device_info_unique_id(self, device: Any) -> str:
        """Group primary standalone sensors under their physical Salus device."""
        device_data = getattr(device, "data", None)
        if isinstance(device_data, dict):
            unique_id = device_data.get("UniID")
            if isinstance(unique_id, str):
                return unique_id
        return super()._device_info_unique_id(device)

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self._device_attr("state")

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of this entity, if any."""
        return self._device_attr("unit_of_measurement")

    @property
    def state_class(self) -> SensorStateClass | None:
        """Return the long-term statistics behavior for numeric sensors."""
        if self._device is None:
            return None
        return STATE_CLASS_BY_DEVICE_CLASS.get(self._device.device_class)

    @property
    def device_class(self) -> str | None:
        """Return the device class of the sensor."""
        return self._device_attr("device_class")

    @property
    def entity_category(self) -> EntityCategory | None:
        """Return the entity category for diagnostic/config child sensors."""
        if self._device is None:
            return None
        if getattr(self._device, "entity_category", None) == "diagnostic":
            return EntityCategory.DIAGNOSTIC
        return None
