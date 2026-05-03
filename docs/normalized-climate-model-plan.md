# Normalized Climate Model Integration Plan

## Goal

Adapt the Home Assistant integration to consume the richer normalized climate
model from `salus-it600-client`, while preserving or improving every current
SQ610, FC600, TRV, and standard thermostat feature.

The desired end state is that Home Assistant no longer needs a second raw SQ610
detail fetch during each coordinator update. The integration should use client
model fields for system mode, hold type, running state, heating/cooling
setpoints, cooling support, humidity, lock state, and diagnostics.

This branch does not need backwards compatibility with older
`salus-it600-client` releases. Optimize for maintainability by removing
transitional raw-property fallbacks, exact-model special cases, and duplicated
SQ610 command/state logic once the client exposes the normalized model. Preserve
old behavior only when it does not make the implementation or future maintenance
even slightly harder.

## Current Problem

The integration currently keeps SQ610 state working by reading
`raw_climate_props` from an extra `gateway.fetch_sq610_properties()` call. Those
raw props are then used for:

- SQ610 HVAC mode.
- SQ610 running action.
- SQ610 hold/preset state.
- SQ610 current temperature fallback from raw temperature fields.
- SQ610 heating vs cooling target temperature.
- SQ610 cooling capability detection.
- SQ610 humidity value.
- SQ610 diagnostics fields.

Those behaviors must be replaced by normalized client fields, not preserved by
continuing to poll raw SQ610 props.

## Feature Parity Checklist

Do not merge until `raw_climate_props` has no normal entity-state consumers and
all of these have replacements from the client model with tests proving parity:

- SQ610 HVAC `Off` maps from standby hold.
- SQ610 `Heat` and conditional `Cool` map from system/running state.
- SQ610 `Permanent Hold` and `Follow Schedule` remain available presets.
- SQ610 current temperature comes from the normalized client model without
  reading raw `LocalTemperature_x100` or `MeasuredValue_x100`.
- SQ610 target temperature uses cooling setpoint while cooling and heating
  setpoint otherwise.
- SQ610 active `min_temp` and `max_temp` use the active heat/cool range.
- SQ610 cooling support uses normalized client capability signals and does not
  infer cooling from `CoolingSetpoint_x100` alone.
- SQ610 cooling support stays exposed after it has been observed once when the
  device payload can become sparse.
- SQ610 temperature writes choose heat or cool setpoint correctly.
- SQ610 standby ignores target-temperature writes.
- SQ610 turn-on restores the remembered non-standby preset.
- SQ610 lock entity still appears and writes correctly.
- SQ610 humidity, floor temperature, battery, and problem sensors remain.
- SQ610 diagnostics and device availability remain useful without raw polling.
- FC600 heat/cool/off, Eco, fan modes, lock, and setpoint writes remain.
- FC600 variants such as `FC600NH` are treated like FC600.
- Standard thermostats keep the simplified HVAC menu behavior.
- TRV behavior, valve attributes, battery, problem, and open-window entities
  remain unchanged.
- Entity and device identifiers stay stable where doing so does not add adapter
  complexity. This includes climate IDs, lock IDs, and child IDs such as
  `_humidity`, `_floor_temperature`, `_battery`, `_problem`, `_battery_error`,
  and `_open_window`. If a cleaner physical-device model requires an identifier
  change, document it as an intentional breaking migration.

## Integration Changes

1. Add normalized-state accessors in `_climate_state.py`.
   - Read client fields such as `hold_type`, `system_mode`, `running_state`,
     `heating_setpoint`, `cooling_setpoint`, current temperature, heat/cool
     min/max ranges, active `min_temp` / `max_temp`, `supports_cooling`,
     `cooling_capability_source`, and diagnostic/support fields.
   - Include active `min_temp` and `max_temp` in `ClimateViewState`, then have
     `climate.py` read those values instead of returning the raw device range
     directly.
   - Use the client-provided cooling capability signal. Do not infer SQ610
     cooling support from `CoolingSetpoint_x100` or cool range fields.
   - Remove raw-prop fallback logic instead of carrying both paths.
   - Keep all SQ610 interpretation in these helpers so entity methods stay thin.

2. Replace exact FC600 model checks.
   - Use the client classification helper for fan-coil models instead of
     comparing exactly with `MODEL_FC600`.
   - Replace checks in both `_climate_state.py` and `climate.py`.
   - Ensure `FC600NH` receives the same Home Assistant controls and resume
     behavior as `FC600`.

3. Remove raw SQ610 props from normal state.
   - Build SQ610 mode/action/preset/target/range/capability from the client
     model.
   - Audit every direct `_raw_props` access in `climate.py` and
     `_climate_state.py`; replace it with normalized helper calls.
   - Audit `raw_climate_props` consumers outside climate entities too,
     especially coordinator availability diagnostics, diagnostics output, test
     fakes, and shared fixture factories.
   - Update `extra_state_attributes` to expose normalized support fields, not
     raw `SystemMode`/`RunningState`/`HoldType` fetched by the coordinator.
   - Keep diagnostics based on a documented client support-field whitelist,
     rather than flattening raw gateway payloads into entity state.

4. Simplify coordinator polling.
   - Remove `_async_fetch_raw_climate_props()` from `_async_update_data()`.
   - Remove `raw_climate_props` from `SalusData`, coordinator docstrings, and
     normal test data builders unless an explicit support-diagnostics action
     keeps a separate raw snapshot.
   - Remove raw SQ610 health counters unless a separate support-data action still
     uses them.
   - Update availability diagnostics to use `device.available` and any
     normalized `online_status`/support field exposed by the client.
   - Update SQ610 diagnostics to read normalized diagnostic/support fields from
     climate devices and child entities. If raw debug data is still useful, make
     it an explicit support diagnostic action, not part of polling.

5. Simplify SQ610 command paths after client routing exists.
   - Prefer generic semantic client methods when they can route SQ610 writes
     safely.
   - Remove SQ610-specific Home Assistant command branches where the generic
     client method is equally clear.
   - Keep a branch only when Home Assistant behavior is genuinely different,
     such as standby resume memory.
   - Keep HA-side no-op behavior for target-temperature writes while SQ610 is in
     standby, unless the client exposes a cleaner semantic no-op helper.
   - Rely on the client to validate heat and cool setpoint writes against the
     matching active range.

## Test Plan

Integration tests must cover:

- Existing `test_climate.py`, `test_climate_state.py`, `test_coordinator.py`,
  `test_sensor.py`, `test_binary_sensor.py`, `test_lock.py`, and diagnostics
  tests.
- New tests using normalized client fields with no `raw_climate_props`.
- No transitional raw-prop fallback tests; this branch targets the new client
  contract only.
- SQ610 normalized current temperature, heat/cool target temperature, active
  min/max ranges, mode, action, preset, humidity, standby no-op writes, turn-on
  resume, and sparse payload cooling memory.
- SQ610 cooling support where `CoolingControl` proves support and where a
  heat-only payload still includes `CoolingSetpoint_x100`.
- SQ610 missing `HoldType`, `SystemMode`, `RunningState`, setpoints, or ranges
  follow the client fallback contract without requiring HA raw-property
  fallbacks.
- Coordinator tests proving normal updates do not call
  `gateway.fetch_sq610_properties()` and can run against a gateway fake that
  does not implement that method.
- FC600NH Home Assistant behavior with fan-coil controls.
- Diagnostics and availability with no raw SQ610 polling.
- Climate, lock, and child entity identifiers remain stable where that does not
  add adapter complexity; any intentional identifier change is documented as a
  breaking migration.
- Manifest and test requirement pins updated together.

Run before merging:

```bash
pytest
ruff check .
mypy
```

## Release Strategy

1. Release the client first with the richer model and derived convenience fields.
2. Raise `homeassistant_salus` minimum client version only after the client
   release is available.
3. Update both `custom_components/salus/manifest.json` and
   `requirements_test.txt` to the same published client version.
4. Update README, CONTRIBUTING, diagnostics documentation, and changelog entries
   that describe SQ610 raw polling or raw support fields.
5. Do not keep fallback logic for older clients on this branch.
6. Remove raw SQ610 polling only after field parity has been verified against
   tests and at least one real gateway payload for SQ610 heat-only and SQ610
   cooling-capable installations.
