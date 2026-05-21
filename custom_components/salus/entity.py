"""Base entity helpers for the Salus iT600 integration."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from salus_it600.exceptions import IT600CommandError, IT600ConnectionError

from .const import DOMAIN
from .coordinator import SalusConfigEntry, SalusData, SalusDataUpdateCoordinator

CHILD_ENTITY_NAME_BY_DEVICE_CLASS = {
    "battery": "Battery",
    "energy": "Energy",
    "humidity": "Humidity",
    "power": "Power",
    "problem": "Problem",
    "temperature": "Temperature",
}

CHILD_ENTITY_NAME_BY_UNIQUE_ID_SUFFIX = (
    ("_battery_error", "Battery problem"),
    ("_battery_problem", "Battery problem"),
    ("_floor_temperature", "Floor temperature"),
    ("_low_battery", "Low battery"),
    ("_battery", "Battery"),
    ("_energy", "Energy"),
    ("_humidity", "Humidity"),
    ("_power", "Power"),
    ("_problem", "Problem"),
)


class SalusEntity(CoordinatorEntity[SalusDataUpdateCoordinator]):
    """Base class for Salus entities."""

    _attr_has_entity_name = True
    _attr_name = None
    _data_collection: str | None = None

    def __init__(
        self,
        coordinator: SalusDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = device_id

    @property
    def _device(self) -> Any | None:
        """Return the current Salus device snapshot."""
        if self._data_collection is None:
            raise NotImplementedError
        data = self.coordinator.data
        if data is None:
            return None
        return getattr(data, self._data_collection).get(self._device_id)

    def _device_attr(self, attr: str, default: Any = None) -> Any:
        """Return one attribute from the current device snapshot."""
        device = self._device
        return default if device is None else getattr(device, attr, default)

    def _parent_device_name(self, parent_unique_id: str) -> str | None:
        """Return the name of a parent device from the current data snapshot."""
        data = self.coordinator.data
        if data is None:
            return None

        for collection in (
            data.climate_devices,
            data.switch_devices,
            data.cover_devices,
            data.binary_sensor_devices,
            data.sensor_devices,
        ):
            device = collection.get(parent_unique_id)
            name = getattr(device, "name", None)
            if isinstance(name, str):
                return name

        for device in data.sensor_devices.values():
            device_data = getattr(device, "data", None)
            if not isinstance(device_data, dict):
                continue
            if device_data.get("UniID") == parent_unique_id:
                name = getattr(device, "name", None)
                if isinstance(name, str):
                    return name

        return None

    def _child_entity_name(self, device: Any) -> str | None:
        """Return the short entity name for a child entity."""
        parent_unique_id = getattr(device, "parent_unique_id", None)
        if not parent_unique_id:
            return None

        raw_name = getattr(device, "name", None)
        parent_name = self._parent_device_name(parent_unique_id)
        if isinstance(raw_name, str) and isinstance(parent_name, str):
            child_name = raw_name.removeprefix(parent_name).strip()
            if child_name:
                return child_name

        unique_id = getattr(device, "unique_id", self._device_id)
        if isinstance(unique_id, str):
            for suffix, name in CHILD_ENTITY_NAME_BY_UNIQUE_ID_SUFFIX:
                if unique_id.endswith(suffix):
                    return name

        device_class = getattr(device, "device_class", None)
        if isinstance(device_class, str):
            return CHILD_ENTITY_NAME_BY_DEVICE_CLASS.get(device_class)

        return None

    async def _async_run_gateway_command(
        self,
        action: str,
        command: Callable[[], Awaitable[None]],
    ) -> None:
        """Run one gateway command and convert client failures to HA service errors."""
        try:
            async with self.coordinator.gateway_lock:
                await command()
        except (IT600CommandError, IT600ConnectionError) as ex:
            raise HomeAssistantError(
                f"Failed to {action} for Salus device {self._device_id}: {ex}"
            ) from ex

    async def _async_run_gateway_command_and_refresh(
        self,
        action: str,
        command: Callable[[], Awaitable[None]],
    ) -> None:
        """Run one gateway command and request the normal post-command refresh."""
        await self._async_run_gateway_command(action, command)
        await self.coordinator.async_request_debounced_refresh()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        device = self._device
        return (
            super().available
            and device is not None
            and bool(getattr(device, "available", True))
        )

    def _device_info_unique_id(self, device: Any) -> str:
        """Return the device-registry identifier for a primary entity."""
        return getattr(device, "unique_id", self._device_id)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        device = self._device
        if device is None:
            return None

        parent_unique_id = getattr(device, "parent_unique_id", None)
        if parent_unique_id:
            return {"identifiers": {(DOMAIN, parent_unique_id)}}

        unique_id = self._device_info_unique_id(device)
        device_info: DeviceInfo = {
            "identifiers": {(DOMAIN, unique_id)},
            "name": getattr(device, "name", unique_id),
            "manufacturer": getattr(device, "manufacturer", "SALUS"),
            "model": getattr(device, "model", None),
            "sw_version": getattr(device, "sw_version", None),
        }

        if self.coordinator.gateway_id and self.coordinator.gateway_id != unique_id:
            device_info["via_device"] = (DOMAIN, self.coordinator.gateway_id)

        return device_info


def async_add_salus_entities(
    config_entry: SalusConfigEntry,
    coordinator: SalusDataUpdateCoordinator,
    async_add_entities: Callable[[list[SalusEntity]], None],
    entity_factory: Callable[[str], SalusEntity],
    devices_getter: Callable[[SalusData], Mapping[str, Any]],
) -> None:
    """Add existing and newly discovered Salus entities for one platform."""
    known_devices: set[str] = set()

    @callback
    def _async_add_new_entities() -> None:
        if coordinator.data is None:
            return

        current_devices = set(devices_getter(coordinator.data))
        new_device_ids = current_devices - known_devices
        if not new_device_ids:
            return

        known_devices.update(new_device_ids)
        async_add_entities(
            [entity_factory(device_id) for device_id in sorted(new_device_ids)]
        )

    _async_add_new_entities()
    config_entry.async_on_unload(
        coordinator.async_add_listener(_async_add_new_entities)
    )


def async_setup_salus_platform_entities(
    config_entry: SalusConfigEntry,
    async_add_entities: Callable[[list[SalusEntity]], None],
    entity_factory: Callable[[SalusDataUpdateCoordinator, str], SalusEntity],
    devices_getter: Callable[[SalusData], Mapping[str, Any]],
) -> None:
    """Set up one Salus platform using the shared entity discovery helper."""
    coordinator = config_entry.runtime_data.coordinator

    async_add_salus_entities(
        config_entry,
        coordinator,
        async_add_entities,
        lambda device_id: entity_factory(coordinator, device_id),
        devices_getter,
    )
