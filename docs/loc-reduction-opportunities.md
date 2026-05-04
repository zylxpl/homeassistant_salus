# LOC Reduction Opportunities

Notes from a quick source scan of `homeassistant_salus`, focused on reducing
lines of code without changing runtime behavior. This intentionally excludes
removing or moving `docs/upstream-issues.md`.

## Highest-Value Code Changes

| Status | Area | Opportunity | Rough saving |
| --- | --- | --- | ---: |
| Done | `custom_components/salus/climate.py` preset and HVAC command flow | `async_set_hvac_mode()` and `async_set_preset_mode()` repeat SQ610, FC600, and generic preset handling. A small family helper for "remember resume preset, write raw preset, refresh" would keep payload behavior the same while flattening the branches. | 70-130 LOC |
| Done | `custom_components/salus/climate.py` raw preset helpers | `_async_set_sq610_raw_preset()`, `_async_set_fc600_raw_preset()`, and `_async_set_generic_raw_preset()` only vary action text and refresh helper. Merge them into one `_async_set_raw_preset()` with a refresh strategy argument. | 20-40 LOC |
| Done | `custom_components/salus/climate.py` SQ610/FC600 resume memory | `_current_sq610_preset_mode()`, `_current_fc600_preset_mode()`, `_remember_current_sq610_preset()`, and `_remember_current_fc600_preset()` are map-and-store variants. Constant maps plus one remember helper would remove duplicate control flow. | 30-60 LOC |
| Done | `custom_components/salus/_climate_state.py` effective mode/action mapping | `_effective_hvac_mode()`, `_effective_preset_mode()`, and `_hvac_action()` have many early returns. Using mapping tables for raw preset, hold type, running state, and action conversion would reduce branches and make behavior easier to audit. | 45-90 LOC |
| Done | `custom_components/salus/entity.py` command refresh wrapper | Switch, cover, lock, and climate methods repeat "run gateway command, then request debounced refresh". Add `_async_run_gateway_command_and_refresh()` to the base entity and use it for simple commands. | 30-60 LOC |
| Done | `custom_components/salus/entity.py` device lookup and simple attributes | Platform entities repeat `_device` lookup and `None if self._device is None else self._device.<attr>`. A class-level data collection name plus `_device_attr()` helper would shrink binary sensor, switch, sensor, cover, and lock modules. | 50-90 LOC |
| Done | Platform `async_setup_entry()` functions | Binary sensor, switch, sensor, cover, lock, and climate all unpack `runtime_data.coordinator` and call `async_add_salus_entities()`. A `async_setup_salus_platform_entities()` helper could leave only entity class and collection getter per platform. | 35-55 LOC |
| Done | `custom_components/salus/coordinator.py` diagnostics dataclasses | `SalusGatewayHealth.as_diagnostics()` and `SalusDeviceAvailability.as_diagnostics()` manually mirror dataclass fields. `dataclasses.asdict()` plus exclusion of `device_id` where needed would cut boilerplate. | 20-35 LOC |
| Done | `custom_components/salus/coordinator.py` option clamping | `_scan_interval_from_options()`, `_poll_failure_threshold()`, and `_post_command_refresh_delay()` repeat parse/default/clamp logic. A typed `_clamped_option()` helper would centralize this. | 25-45 LOC |
| Done | `custom_components/salus/diagnostics.py` normalized climate fields | `_climate_diagnostics()` manually lists many `getattr()` calls. A tuple of normalized field names and a dict comprehension would preserve output shape while reducing the body. | 35-55 LOC |

## Test Cleanup

| Status | Area | Opportunity | Rough saving |
| --- | --- | --- | ---: |
| Done | `tests/test_climate.py` command tests | Many tests repeat device, coordinator, entity setup and then assert gateway calls. Add `make_thermostat()` and `assert_gateway_calls()` helpers, then table-drive simple preset/HVAC command cases with `pytest.mark.parametrize`. | 120-220 LOC |
| Done | `tests/test_climate_state.py` view-state tests | The tests repeatedly build a device, call `build_climate_view_state()`, and assert a few attributes. A `state(**device_overrides)` helper plus `assert_attrs()` would reduce repeated scaffolding. | 70-130 LOC |
| Done | `tests/conftest.py` fake devices | `make_*_device()` factories repeat common `SimpleNamespace` fields. A `_device_base()` helper or small dataclass/default-dict factory would reduce boilerplate without changing test semantics. | 50-90 LOC |
| Done | `tests/test_init.py` patch blocks | Ruff flags two nested `with` blocks that can be combined. This is tiny but mechanical and safe. | 4-8 LOC |

## Documentation Cleanup

Do not reduce LOC in documentation

## Mechanical Ruff Wins

These are small cleanup items found with simplification-oriented Ruff rules:

- Done: Combine the nested FC600 temperature guard in `climate.py`.
- Done: Move local test imports in `tests/test_climate.py` and `tests/test_init.py`
  to module scope, if doing so does not interfere with monkeypatching.
- Done: Combine nested `with` statements in `tests/test_init.py`.
- Done: Consider an `EUID_LENGTH = 16` constant in `config_flow.py`.

## Suggested First Patch

Start with base entity helpers:

1. Done: Add `_async_run_gateway_command_and_refresh()` to `SalusEntity`.
2. Done: Convert simple switch, cover, lock, fan-mode, and generic preset commands to
   use it.
3. Done: Add `_device_attr()` for simple pass-through properties.
4. Done: Run the entity tests after each stage.

This is the lowest-risk source reduction because it removes repeated Home
Assistant wrapper code while keeping gateway method names, arguments, and
refresh timing unchanged.
