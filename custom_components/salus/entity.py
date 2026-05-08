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
