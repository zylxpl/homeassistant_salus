"""Climate state interpretation tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from salus_it600.const import (
    CURRENT_HVAC_COOL,
    FAN_MODE_AUTO,
    FAN_MODE_HIGH,
    HVAC_MODE_HEAT,
    PRESET_OFF,
)
from salus_it600.const import (
    PRESET_ECO as RAW_PRESET_ECO,
)
from salus_it600.const import (
    PRESET_FOLLOW_SCHEDULE as RAW_PRESET_FOLLOW_SCHEDULE,
)
from salus_it600.device_models import (
    SQ610_HOLD_AUTO,
    SQ610_HOLD_PERMANENT,
    SQ610_HOLD_STANDBY,
    SQ610_MODE_COOL,
    SQ610_MODE_HEAT,
    SQ610_RUNNING_COOL,
    SQ610_RUNNING_HEAT,
)

from custom_components.salus._climate_state import (
    PRESET_ECO,
    PRESET_FOLLOW_SCHEDULE,
    PRESET_PERMANENT_HOLD,
    build_climate_view_state,
)


def _device(**overrides: Any) -> SimpleNamespace:
    values = {
        "model": "HTRP-RF(50)",
        "hvac_mode": HVAC_MODE_HEAT,
        "hvac_action": "idle",
        "hvac_modes": [HVAC_MODE_HEAT],
        "preset_mode": RAW_PRESET_FOLLOW_SCHEDULE,
        "preset_modes": [
            RAW_PRESET_FOLLOW_SCHEDULE,
            "Permanent Hold",
            PRESET_OFF,
        ],
        "current_temperature": 20.0,
        "current_humidity": None,
        "target_temperature": 21.0,
        "fan_mode": None,
        "fan_modes": None,
        "hold_type": None,
        "system_mode": None,
        "running_state": None,
        "heating_setpoint": None,
        "cooling_setpoint": None,
        "supports_cooling": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_sq610_cooling_uses_normalized_cooling_setpoint() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            system_mode=SQ610_MODE_COOL,
            running_state=SQ610_RUNNING_COOL,
            hold_type=SQ610_HOLD_PERMANENT,
            cooling_setpoint=22.5,
            heating_setpoint=21.0,
            target_temperature=22.5,
            supports_cooling=True,
        ),
    )

    assert state.supports_cooling is True
    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    assert state.hvac_mode == HVACMode.COOL
    assert state.hvac_action == HVACAction.COOLING
    assert state.target_temperature == 22.5
    assert state.preset_mode == PRESET_PERMANENT_HOLD
    assert state.preset_modes == [PRESET_PERMANENT_HOLD, PRESET_FOLLOW_SCHEDULE]


def test_sq610_auto_hold_preserves_cooling_system_mode() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            system_mode=SQ610_MODE_COOL,
            running_state=SQ610_RUNNING_COOL,
            hold_type=SQ610_HOLD_AUTO,
            cooling_setpoint=22.5,
            heating_setpoint=21.0,
            target_temperature=22.5,
            supports_cooling=True,
        ),
    )

    assert state.hvac_mode == HVACMode.COOL
    assert state.target_temperature == 22.5
    assert state.preset_mode == PRESET_FOLLOW_SCHEDULE


def test_sq610_auto_hold_preserves_heating_system_mode() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            system_mode=SQ610_MODE_HEAT,
            running_state=SQ610_RUNNING_HEAT,
            hold_type=SQ610_HOLD_AUTO,
            cooling_setpoint=22.5,
            heating_setpoint=21.0,
            target_temperature=21.0,
            supports_cooling=True,
        ),
    )

    assert state.hvac_mode == HVACMode.HEAT
    assert state.target_temperature == 21.0
    assert state.preset_mode == PRESET_FOLLOW_SCHEDULE


def test_sq610_current_temperature_uses_normalized_temperature() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            current_temperature=22.35,
            hold_type=SQ610_HOLD_PERMANENT,
            heating_setpoint=21.0,
        ),
    )

    assert state.current_temperature == 22.35


def test_sq610_humidity_uses_normalized_percent_value() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            current_humidity=63.0,
            hold_type=SQ610_HOLD_PERMANENT,
            heating_setpoint=21.0,
        ),
    )

    assert state.current_humidity == 63.0


def test_sq610_humidity_accepts_normalized_fractional_value() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            current_humidity=45.5,
            hold_type=SQ610_HOLD_PERMANENT,
            heating_setpoint=21.0,
        ),
    )

    assert state.current_humidity == 45.5


def test_sq610_standby_maps_to_off_mode_and_off_action() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            running_state=SQ610_RUNNING_HEAT,
            hold_type=SQ610_HOLD_STANDBY,
            heating_setpoint=21.0,
        ),
    )

    assert state.hvac_mode == HVACMode.OFF
    assert state.hvac_action == HVACAction.OFF
    assert state.preset_mode is None


def test_sq610_standby_hides_remembered_resume_preset() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            running_state=SQ610_RUNNING_HEAT,
            hold_type=SQ610_HOLD_STANDBY,
            heating_setpoint=21.0,
        ),
        PRESET_FOLLOW_SCHEDULE,
    )

    assert state.hvac_mode == HVACMode.OFF
    assert state.preset_mode is None


def test_sq610_unknown_hold_type_uses_remembered_resume_preset() -> None:
    state = build_climate_view_state(
        _device(model="SQ610RF", hold_type=99, heating_setpoint=21.0),
        PRESET_FOLLOW_SCHEDULE,
    )

    assert state.preset_mode == PRESET_FOLLOW_SCHEDULE


def test_sq610_auto_hold_without_system_state_falls_back_to_heat_mode() -> None:
    state = build_climate_view_state(
        _device(model="SQ610RF", hold_type=SQ610_HOLD_AUTO, heating_setpoint=21.0),
    )

    assert state.hvac_mode == HVACMode.HEAT
    assert state.preset_mode == PRESET_FOLLOW_SCHEDULE


def test_sq610_heat_only_exposes_off_heat_modes() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            hold_type=SQ610_HOLD_PERMANENT,
            heating_setpoint=21.0,
            supports_cooling=False,
        ),
    )

    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT]
    assert state.supports_cooling is False


def test_sq610_keeps_cool_mode_when_cooling_was_seen_before() -> None:
    state = build_climate_view_state(
        _device(
            model="SQ610RF",
            hold_type=SQ610_HOLD_PERMANENT,
            heating_setpoint=21.0,
            supports_cooling=False,
        ),
        sq610_known_supports_cooling=True,
    )

    assert state.supports_cooling is True
    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]


def test_standard_off_preset_maps_to_hvac_off_without_preset_menu() -> None:
    state = build_climate_view_state(
        _device(preset_mode=PRESET_OFF),
    )

    assert state.hvac_mode == HVACMode.OFF
    assert state.hvac_action == HVACAction.OFF
    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT, HVACMode.AUTO]
    assert state.preset_mode is None
    assert state.preset_modes == []


def test_simple_heat_only_device_uses_hvac_menu_without_preset_menu() -> None:
    state = build_climate_view_state(_device())

    expected = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | getattr(ClimateEntityFeature, "TURN_ON", ClimateEntityFeature(0))
        | getattr(ClimateEntityFeature, "TURN_OFF", ClimateEntityFeature(0))
    )
    assert state.hvac_mode == HVACMode.AUTO
    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT, HVACMode.AUTO]
    assert state.preset_mode is None
    assert state.preset_modes == []
    assert state.supported_features == expected


def test_fc600_fan_modes_are_exposed() -> None:
    state = build_climate_view_state(
        _device(
            model="FC600",
            hvac_mode=HVACMode.COOL,
            hvac_action=CURRENT_HVAC_COOL,
            preset_modes=[
                RAW_PRESET_FOLLOW_SCHEDULE,
                "Permanent Hold",
                RAW_PRESET_ECO,
                PRESET_OFF,
            ],
            fan_mode=FAN_MODE_HIGH,
            fan_modes=[FAN_MODE_AUTO, FAN_MODE_HIGH],
        ),
    )

    assert state.supports_cooling is True
    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    assert state.hvac_mode == HVACMode.COOL
    assert state.preset_modes == [
        PRESET_FOLLOW_SCHEDULE,
        PRESET_PERMANENT_HOLD,
        PRESET_ECO,
    ]
    assert state.fan_mode == "high"
    assert state.fan_modes == ["auto", "high"]
    assert state.supported_features & ClimateEntityFeature.FAN_MODE


def test_fc600nh_variant_is_treated_as_fan_coil() -> None:
    state = build_climate_view_state(
        _device(
            model="FC600NH",
            hvac_mode=HVACMode.COOL,
            hvac_action=CURRENT_HVAC_COOL,
            preset_modes=[
                RAW_PRESET_FOLLOW_SCHEDULE,
                "Permanent Hold",
                RAW_PRESET_ECO,
                PRESET_OFF,
            ],
            fan_mode=FAN_MODE_HIGH,
            fan_modes=[FAN_MODE_AUTO, FAN_MODE_HIGH],
        ),
    )

    assert state.supports_cooling is True
    assert state.hvac_modes == [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    assert state.hvac_mode == HVACMode.COOL
    assert state.preset_modes == [
        PRESET_FOLLOW_SCHEDULE,
        PRESET_PERMANENT_HOLD,
        PRESET_ECO,
    ]
    assert state.fan_modes == ["auto", "high"]


def test_fc600_off_preset_maps_to_off_hvac_mode() -> None:
    state = build_climate_view_state(
        _device(
            model="FC600",
            hvac_mode=HVACMode.COOL,
            preset_mode=PRESET_OFF,
            fan_mode=FAN_MODE_AUTO,
            fan_modes=[FAN_MODE_AUTO, FAN_MODE_HIGH],
        ),
    )

    assert state.hvac_mode == HVACMode.OFF
    assert state.hvac_action == HVACAction.OFF
    assert state.preset_mode is None


def test_fc600_off_preset_hides_remembered_resume_preset() -> None:
    state = build_climate_view_state(
        _device(
            model="FC600",
            hvac_mode=HVACMode.COOL,
            preset_mode=PRESET_OFF,
            fan_mode=FAN_MODE_AUTO,
            fan_modes=[FAN_MODE_AUTO, FAN_MODE_HIGH],
        ),
        fc600_resume_preset_mode=PRESET_ECO,
    )

    assert state.hvac_mode == HVACMode.OFF
    assert state.preset_mode is None


def test_fc600_eco_maps_to_ha_eco_preset() -> None:
    state = build_climate_view_state(
        _device(
            model="FC600",
            hvac_mode=HVACMode.HEAT,
            preset_mode=RAW_PRESET_ECO,
            fan_mode=FAN_MODE_AUTO,
            fan_modes=[FAN_MODE_AUTO, FAN_MODE_HIGH],
        ),
    )

    assert state.hvac_mode == HVACMode.HEAT
    assert state.preset_mode == PRESET_ECO
