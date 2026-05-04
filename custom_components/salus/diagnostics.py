"""Diagnostics support for the Salus iT600 integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import SalusData, SalusRuntimeData

TO_REDACT = {CONF_TOKEN}

CLIMATE_SUPPORT_FIELDS = (
    "UniID",
    "DeviceName",
    "ModelIdentifier_i",
    "OnlineStatus_i",
    "FirmwareVersion",
    "LocalTemperature_x100",
    "MeasuredValue_x100",
    "HeatingControl",
    "CoolingControl",
    "HeatingSetpoint_x100",
    "CoolingSetpoint_x100",
    "MinHeatSetpoint_x100",
    "MaxHeatSetpoint_x100",
    "MinCoolSetpoint_x100",
    "MaxCoolSetpoint_x100",
    "SunnySetpoint_x100",
    "SystemMode",
    "RunningState",
    "HoldType",
    "LockKey",
    "LockKey_a",
)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a Salus config entry."""
    runtime_data = _runtime_data(hass, entry)

    diagnostics: dict[str, Any] = {
        "entry": {
            "entry_id": getattr(entry, "entry_id", None),
            "title": getattr(entry, "title", None),
            "data": async_redact_data(dict(getattr(entry, "data", {})), TO_REDACT),
        },
    }

    if runtime_data is None:
        diagnostics["runtime"] = {"loaded": False}
        return diagnostics

    coordinator = runtime_data.coordinator
    data: SalusData | None = coordinator.data

    diagnostics.update(
        {
            "runtime": {"loaded": True},
            "gateway": {
                "id": coordinator.gateway_id,
                "host": getattr(entry, "data", {}).get(CONF_HOST),
                "health": coordinator.gateway_diagnostics(),
            },
            "device_counts": _device_counts(data),
            "device_availability": coordinator.device_availability_diagnostics(),
            "climate": _climate_diagnostics(data),
        }
    )
    return diagnostics


def _runtime_data(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> SalusRuntimeData | None:
    """Return runtime data from modern or fallback Home Assistant storage."""
    runtime_data = getattr(entry, "runtime_data", None)
    if runtime_data is not None:
        return runtime_data

    domain_data = getattr(hass, "data", {}).get(DOMAIN, {})
    return domain_data.get(getattr(entry, "entry_id", None))


def _device_counts(data: SalusData | None) -> dict[str, int]:
    """Return device counts by platform."""
    if data is None:
        return {}

    return {
        "climate": len(data.climate_devices),
        "binary_sensor": len(data.binary_sensor_devices),
        "switch": len(data.switch_devices),
        "cover": len(data.cover_devices),
        "sensor": len(data.sensor_devices),
    }


def _climate_diagnostics(data: SalusData | None) -> dict[str, Any]:
    """Return normalized climate diagnostics useful for field support."""
    if data is None:
        return {"devices": {}}

    devices: dict[str, Any] = {}
    for device_id, device in sorted(data.climate_devices.items()):
        diagnostic_fields = getattr(device, "diagnostic_fields", None)
        if not isinstance(diagnostic_fields, dict):
            diagnostic_fields = {}

        devices[device_id] = {
            "model": getattr(device, "model", None),
            "available": getattr(device, "available", None),
            "field_count": len(diagnostic_fields),
            "present_fields": sorted(diagnostic_fields),
            "normalized_fields": {
                "current_temperature": getattr(device, "current_temperature", None),
                "current_humidity": getattr(device, "current_humidity", None),
                "target_temperature": getattr(device, "target_temperature", None),
                "min_temp": getattr(device, "min_temp", None),
                "max_temp": getattr(device, "max_temp", None),
                "hvac_mode": getattr(device, "hvac_mode", None),
                "hvac_action": getattr(device, "hvac_action", None),
                "hvac_modes": list(getattr(device, "hvac_modes", None) or []),
                "preset_mode": getattr(device, "preset_mode", None),
                "preset_modes": list(getattr(device, "preset_modes", None) or []),
                "fan_mode": getattr(device, "fan_mode", None),
                "fan_modes": (
                    None
                    if getattr(device, "fan_modes", None) is None
                    else list(getattr(device, "fan_modes", None) or [])
                ),
                "online_status": getattr(device, "online_status", None),
                "hold_type": getattr(device, "hold_type", None),
                "system_mode": getattr(device, "system_mode", None),
                "running_state": getattr(device, "running_state", None),
                "heating_setpoint": getattr(device, "heating_setpoint", None),
                "cooling_setpoint": getattr(device, "cooling_setpoint", None),
                "min_heat_temp": getattr(device, "min_heat_temp", None),
                "max_heat_temp": getattr(device, "max_heat_temp", None),
                "min_cool_temp": getattr(device, "min_cool_temp", None),
                "max_cool_temp": getattr(device, "max_cool_temp", None),
                "heating_control": getattr(device, "heating_control", None),
                "cooling_control": getattr(device, "cooling_control", None),
                "supports_cooling": getattr(device, "supports_cooling", None),
                "supports_fan": getattr(device, "supports_fan", None),
                "supports_heat": getattr(device, "supports_heat", None),
                "cooling_capability_source": getattr(
                    device,
                    "cooling_capability_source",
                    None,
                ),
            },
            "support_fields": {
                field: diagnostic_fields.get(field)
                for field in CLIMATE_SUPPORT_FIELDS
                if field in diagnostic_fields
            },
        }

    return {"devices": devices}
