# Upstream Issues Status

Companion status matrix for [upstream-issues.md](upstream-issues.md).

`upstream-issues.md` is an exported historical record from
`epoplavskis/homeassistant_salus`. Keep that export intact. Use this file for
local maintainer tracking.

Last reviewed: 2026-05-02.

## Status Labels

- `Solved locally`: fixed in this integration or in the pinned
  `salus-it600-client` version.
- `Closed upstream`: the exported upstream issue is already closed.
- `Backlog`: still open upstream and not confirmed fixed here.
- `Needs verification`: code may cover the case, but the exact issue report has
  not been retested.
- `Workaround documented`: the thread identifies a configuration/user action,
  not necessarily a code fix.
- `Not actionable`: question, sale, ownership, or historical note.

## Status Matrix

| Issue | Upstream state | Local status | Notes |
| --- | --- | --- | --- |
| [#85 Can UGE600 stay offline with this integration?](https://github.com/epoplavskis/homeassistant_salus/issues/85) | closed | Closed upstream | Historical/offline behavior discussion. |
| [#84 Infloor temperature sensors not displayed](https://github.com/epoplavskis/homeassistant_salus/issues/84) | open | Solved locally | Current client and integration expose floor-temperature sensors for supported SQ610-style payloads. |
| [#83 SD600 salus](https://github.com/epoplavskis/homeassistant_salus/issues/83) | open | Backlog | SD600 support request. |
| [#82 UG800 after update can no longer be integrated](https://github.com/epoplavskis/homeassistant_salus/issues/82) | open | Backlog | New UG800 firmware/protocol issue. |
| [#81 UG800 support?](https://github.com/epoplavskis/homeassistant_salus/issues/81) | open | Backlog | UG800 support request; needs current-firmware validation. |
| [#80 Problem with Salus FC600NH](https://github.com/epoplavskis/homeassistant_salus/issues/80) | open | Solved locally | FC600NH setpoint/control issue. Told user to test our branch |
| [#79 Failed to connect, please check IP address 2025.9.1](https://github.com/epoplavskis/homeassistant_salus/issues/79) | open | Backlog | Connection failure report. |
| [#77 Can't fetch integration files](https://github.com/epoplavskis/homeassistant_salus/issues/77) | closed | Closed upstream | Historical installation issue. |
| [#76 Failed to connect, please check EUID](https://github.com/epoplavskis/homeassistant_salus/issues/76) | open | Workaround documented | EUID/local-mode troubleshooting applies, but not all cases are resolved. |
| [#75 SD600 disappearing after a while](https://github.com/epoplavskis/homeassistant_salus/issues/75) | open | Backlog | SD600 stability issue. |
| [#74 Setting preset/target-temperature via HA?](https://github.com/epoplavskis/homeassistant_salus/issues/74) | open | Needs verification | Current climate entities support setpoint/preset commands, but this report needs retesting. |
| [#73 Running state for thermostat-connected valve](https://github.com/epoplavskis/homeassistant_salus/issues/73) | open | Backlog | TRV/valve running-state request. |
| [#72 mqtt2 integration](https://github.com/epoplavskis/homeassistant_salus/issues/72) | open | Not actionable | Separate integration approach. |
| [#71 Support for Salus iT800?](https://github.com/epoplavskis/homeassistant_salus/issues/71) | open | Backlog | Device family request. |
| [#70 2025.1 Salus HA integration stopped working](https://github.com/epoplavskis/homeassistant_salus/issues/70) | open | Solved locally | Covered by current HA compatibility fixes. |
| [#69 HomeKit](https://github.com/epoplavskis/homeassistant_salus/issues/69) | open | Backlog | HomeKit/scene feature request. |
| [#68 HA 2025.1 deprecations](https://github.com/epoplavskis/homeassistant_salus/issues/68) | closed | Solved locally | Current code uses modern HA APIs and passes the test suite. |
| [#67 Fahrenheit to Celsius](https://github.com/epoplavskis/homeassistant_salus/issues/67) | closed | Closed upstream | Historical unit display issue. |
| [#66 Gateway command error](https://github.com/epoplavskis/homeassistant_salus/issues/66) | open | Backlog | Generic command failure report. |
| [#65 New HTR-RF(20) without climate entity](https://github.com/epoplavskis/homeassistant_salus/issues/65) | open | Backlog | Device support request. |
| [#64 HA 2025.1 deprecated features](https://github.com/epoplavskis/homeassistant_salus/issues/64) | open | Solved locally | Covered by the same HA compatibility work as #68. |
| [#63 HA 2025.6 problem](https://github.com/epoplavskis/homeassistant_salus/issues/63) | open | Solved locally | Thread says it is solved by the PR suggested in #68. |
| [#62 NoneType object has no attribute available](https://github.com/epoplavskis/homeassistant_salus/issues/62) | open | Backlog | Parser/entity robustness issue; needs reproduction. |
| [#60 HA stops working](https://github.com/epoplavskis/homeassistant_salus/issues/60) | open | Backlog | Stability report without enough diagnostics. |
| [#59 Integration failing since new Salus app](https://github.com/epoplavskis/homeassistant_salus/issues/59) | open | Backlog | Needs current local-mode/protocol validation. |
| [#58 HA not adjusting Salus temperature](https://github.com/epoplavskis/homeassistant_salus/issues/58) | open | Backlog | Command/control issue. |
| [#57 Migration to new SALUS Premium Lite app](https://github.com/epoplavskis/homeassistant_salus/issues/57) | closed | Closed upstream | Historical app migration discussion. |
| [#56 HA 2024.01](https://github.com/epoplavskis/homeassistant_salus/issues/56) | open | Solved locally | Current code targets newer HA APIs. |
| [#55 Device names with spaces or special characters](https://github.com/epoplavskis/homeassistant_salus/issues/55) | open | Workaround documented | Reporter fixed by renaming devices; needs local verification for robust name handling. |
| [#54 HA 2024.01 breaking changes](https://github.com/epoplavskis/homeassistant_salus/issues/54) | open | Solved locally | Current code is compatible with newer HA versions; fan comment in this thread is covered separately by #46. |
| [#53 Unknown error when trying to connect](https://github.com/epoplavskis/homeassistant_salus/issues/53) | open | Backlog | Connection failure report. |
| [#52 How to add this to Home Assistant Green?](https://github.com/epoplavskis/homeassistant_salus/issues/52) | closed | Closed upstream | Installation support question. |
| [#51 Not all thermostats are visible](https://github.com/epoplavskis/homeassistant_salus/issues/51) | closed | Closed upstream | Historical discovery issue. |
| [#50 Config flow could not be loaded](https://github.com/epoplavskis/homeassistant_salus/issues/50) | open | Solved locally | Current config flow has regression coverage. |
| [#49 Notice of transfer of ownership](https://github.com/epoplavskis/homeassistant_salus/issues/49) | open | Not actionable | Project ownership note. |
| [#48 Deprecated code causing failure](https://github.com/epoplavskis/homeassistant_salus/issues/48) | open | Solved locally | Current code no longer uses the deprecated entity registry path described in the issue. |
| [#47 Selling my Salus devices on eBay](https://github.com/epoplavskis/homeassistant_salus/issues/47) | closed | Not actionable | Personal sale note. |
| [#46 Change fan mode not working](https://github.com/epoplavskis/homeassistant_salus/issues/46) | open | Solved locally | Fixed through `salus-it600-client 0.4.6`, which writes `sFanS.SetFanMode`. |
| [#45 SQ610RF thermostats not found](https://github.com/epoplavskis/homeassistant_salus/issues/45) | closed | Closed upstream | Historical discovery issue. |
| [#44 Maintainer wanted](https://github.com/epoplavskis/homeassistant_salus/issues/44) | closed | Not actionable | Historical maintenance note. |
| [#43 Cannot connect to UGE600](https://github.com/epoplavskis/homeassistant_salus/issues/43) | open | Workaround documented | Threads identify all-zero EUID, Local WiFi Mode, and network isolation cases; some reports remain unresolved. |
| [#42 RX10RF not updating](https://github.com/epoplavskis/homeassistant_salus/issues/42) | open | Backlog | Device update issue. |
| [#41 Support for ECM600](https://github.com/epoplavskis/homeassistant_salus/issues/41) | open | Backlog | Electric monitor support request. |
| [#40 Selling my Salus devices on eBay](https://github.com/epoplavskis/homeassistant_salus/issues/40) | closed | Not actionable | Personal sale note. |
| [#39 Temperature automations](https://github.com/epoplavskis/homeassistant_salus/issues/39) | open | Not actionable | Automation usage question rather than integration defect. |
| [#38 Troubleshooting UUID 15 chars not 16](https://github.com/epoplavskis/homeassistant_salus/issues/38) | open | Workaround documented | Correct EUID location/documentation issue. |
| [#36 Can I run more than one gateway?](https://github.com/epoplavskis/homeassistant_salus/issues/36) | closed | Closed upstream | Historical usage question. |
| [#35 SD600](https://github.com/epoplavskis/homeassistant_salus/issues/35) | open | Backlog | Device support request. |
| [#33 Not working](https://github.com/epoplavskis/homeassistant_salus/issues/33) | closed | Closed upstream | Historical support issue. |
| [#32 Data not updating after system update](https://github.com/epoplavskis/homeassistant_salus/issues/32) | open | Backlog | Separate from client upstream #32; not the FC600 fan-mode fix. |
| [#31 Support cooling mode](https://github.com/epoplavskis/homeassistant_salus/issues/31) | open | Needs verification | Current FC600/SQ610 climate support includes cooling paths, but this exact report needs retesting. |
| [#30 SQ610RF humidity extraction](https://github.com/epoplavskis/homeassistant_salus/issues/30) | open | Solved locally | Current client exposes SQ610 humidity where present. |
| [#29 HA 2022.3.0 breaking change](https://github.com/epoplavskis/homeassistant_salus/issues/29) | closed | Closed upstream | Historical dependency issue. |
| [#28 Blocking call](https://github.com/epoplavskis/homeassistant_salus/issues/28) | closed | Closed upstream | Historical async/blocking issue. |
| [#27 Error on HA 2021.12.10 Docker container](https://github.com/epoplavskis/homeassistant_salus/issues/27) | closed | Closed upstream | Historical dependency issue. |
| [#26 Always Follow Schedule mode](https://github.com/epoplavskis/homeassistant_salus/issues/26) | open | Needs verification | Current preset handling may cover this; needs issue-specific retest. |
| [#25 Unable to change HVAC modes or presets - SQ610RF](https://github.com/epoplavskis/homeassistant_salus/issues/25) | closed | Closed upstream | Historical command issue. |
| [#24 Underfloor heating automation](https://github.com/epoplavskis/homeassistant_salus/issues/24) | open | Backlog | Automation/control design request. |
| [#23 KL08RF control](https://github.com/epoplavskis/homeassistant_salus/issues/23) | open | Backlog | Wiring center control request. |
| [#22 Floor temperature feature request](https://github.com/epoplavskis/homeassistant_salus/issues/22) | open | Solved locally | Current client has floor-temperature parsing for SQ610-style payloads. |
| [#21 NA family of devices](https://github.com/epoplavskis/homeassistant_salus/issues/21) | open | Backlog | Region/device-family request. |
| [#20 Unable to connect - EUID error](https://github.com/epoplavskis/homeassistant_salus/issues/20) | open | Workaround documented | All-zero EUID, correct EUID label, and Local WiFi Mode are documented; some firmware/network cases remain unresolved. |
| [#19 After update to 0.3.0 thermostats do not work](https://github.com/epoplavskis/homeassistant_salus/issues/19) | closed | Closed upstream | Historical release regression. |
| [#18 Integration not showing up](https://github.com/epoplavskis/homeassistant_salus/issues/18) | open | Workaround documented | Thread suggests full HA reboot; needs current install validation. |
| [#17 Salus does not appear in integrations](https://github.com/epoplavskis/homeassistant_salus/issues/17) | closed | Closed upstream | Browser cache workaround. |
| [#15 SR600 delayed state change](https://github.com/epoplavskis/homeassistant_salus/issues/15) | open | Needs verification | Current polling options may improve this, but SR600 behavior needs retesting. |
| [#13 SR600 button S1/S2 features](https://github.com/epoplavskis/homeassistant_salus/issues/13) | open | Backlog | Feature request. |
| [#12 Bug with PS600](https://github.com/epoplavskis/homeassistant_salus/issues/12) | closed | Closed upstream | Historical bug. |
| [#11 Unavailable entries after reboot](https://github.com/epoplavskis/homeassistant_salus/issues/11) | closed | Closed upstream | Historical availability issue. |
| [#10 Salus is not showing up in integrations](https://github.com/epoplavskis/homeassistant_salus/issues/10) | closed | Closed upstream | Historical installation issue. |
| [#9 New features](https://github.com/epoplavskis/homeassistant_salus/issues/9) | open | Backlog | Umbrella feature request. |
| [#6 Missing follow schedule button](https://github.com/epoplavskis/homeassistant_salus/issues/6) | closed | Closed upstream | Fixed in pyit600 according to thread. |
| [#3 Athom Homey integration](https://github.com/epoplavskis/homeassistant_salus/issues/3) | closed | Not actionable | External platform request. |

## Cross-Repo Links

- Integration issue #46 corresponds to client upstream issue
  `epoplavskis/pyit600#32`.
- The fan-mode fix is released in `salus-it600-client 0.4.6`.
- This integration consumes that fix by requiring `salus-it600-client==0.4.6`
  or newer.
