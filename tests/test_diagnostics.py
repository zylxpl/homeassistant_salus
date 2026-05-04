"""Diagnostics tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

from homeassistant.const import CONF_HOST, CONF_TOKEN
from homeassistant.core import HomeAssistant

from custom_components.salus.coordinator import (
    SalusDataUpdateCoordinator,
    SalusRuntimeData,
)
from custom_components.salus.diagnostics import async_get_config_entry_diagnostics


def _sq610_device() -> SimpleNamespace:
    return SimpleNamespace(
        unique_id="sq610-1",
        available=True,
        name="Bedroom",
        model="SQ610RF",
        data={"UniID": "sq610-1"},
        online_status=1,
        hold_type=2,
        system_mode=4,
        running_state=0,
        heating_setpoint=22.0,
        cooling_setpoint=None,
        min_heat_temp=5.0,
        max_heat_temp=35.0,
        min_cool_temp=None,
        max_cool_temp=None,
        heating_control=1,
        cooling_control=0,
        supports_cooling=True,
        cooling_capability_source="cooling_control",
        diagnostic_fields={
            "OnlineStatus_i": 1,
            "CoolingControl": 0,
            "SystemMode": 4,
            "LockKey": 1,
            "LockKey_a": 1,
        },
    )


class FakeGateway:
    def __init__(self) -> None:
        self.climate_devices = {"sq610-1": _sq610_device()}

    async def poll_status(self) -> None:
        return None

    def get_climate_devices(self) -> dict[str, Any]:
        return self.climate_devices

    def get_binary_sensor_devices(self) -> dict[str, Any]:
        return {}

    def get_switch_devices(self) -> dict[str, Any]:
        return {}

    def get_cover_devices(self) -> dict[str, Any]:
        return {}

    def get_sensor_devices(self) -> dict[str, Any]:
        return {}

async def test_diagnostics_redacts_token_and_reports_health(hass: HomeAssistant) -> None:
    gateway = FakeGateway()
    entry = MagicMock()
    entry.entry_id = "entry-1"
    entry.title = "Salus"
    entry.data = {CONF_HOST: "192.0.2.10", CONF_TOKEN: "001E5E0D32906128"}
    entry.options = {}
    coordinator = SalusDataUpdateCoordinator(hass, entry, gateway)
    coordinator.gateway_id = "gateway-1"
    entry.runtime_data = SalusRuntimeData(
        gateway=gateway,
        coordinator=coordinator,
    )

    coordinator.data = await coordinator._async_update_data()
    diagnostics = await async_get_config_entry_diagnostics(hass, entry)

    assert diagnostics["entry"]["data"][CONF_HOST] == "192.0.2.10"
    assert diagnostics["entry"]["data"][CONF_TOKEN] == "**REDACTED**"
    assert diagnostics["runtime"]["loaded"] is True
    assert diagnostics["device_counts"]["climate"] == 1
    assert diagnostics["gateway"]["health"]["successful_updates"] == 1
    assert diagnostics["sq610"]["devices"]["sq610-1"]["support_fields"][
        "LockKey"
    ] == 1
    assert diagnostics["sq610"]["devices"]["sq610-1"]["support_fields"][
        "LockKey_a"
    ] == 1
    assert diagnostics["sq610"]["devices"]["sq610-1"]["support_fields"][
        "CoolingControl"
    ] == 0
    assert diagnostics["sq610"]["devices"]["sq610-1"]["normalized_fields"][
        "supports_cooling"
    ] is True


async def test_diagnostics_handles_unloaded_entry(hass: HomeAssistant) -> None:
    entry = SimpleNamespace(
        entry_id="entry-1",
        title="Salus",
        data={CONF_HOST: "192.0.2.10", CONF_TOKEN: "001E5E0D32906128"},
    )

    diagnostics = await async_get_config_entry_diagnostics(hass, entry)

    assert diagnostics["runtime"]["loaded"] is False
    assert diagnostics["entry"]["data"][CONF_TOKEN] == "**REDACTED**"
