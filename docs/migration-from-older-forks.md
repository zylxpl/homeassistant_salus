# Migrating From Older Forks

This repository keeps the Home Assistant integration domain as `salus`, so most
installations can move from an older fork without deleting the integration entry.
That helps preserve gateway configuration and existing entity registry records.

## Before You Start

1. Back up your Home Assistant configuration.
2. Note your current custom repository URL in HACS.
3. Note the installed `homeassistant_salus` version if HACS shows one.
4. Export diagnostics from **Settings** -> **Devices & Services** -> **Salus iT600** -> **Download diagnostics**.

## HACS Migration

1. Open HACS.
2. Go to **Integrations** -> **Custom repositories**.
3. Remove the old `homeassistant_salus` fork URL if it is still present.
4. Add `https://github.com/Jordi-14/homeassistant_salus` as an **Integration**.
5. Install or update **Salus iT600** from the new repository entry.
6. Restart Home Assistant.
7. Open **Settings** -> **Devices & Services** and confirm the Salus iT600 integration loads.

Do not delete and recreate the Salus integration entry unless you are prepared
to recreate entity customizations, dashboards, and automations that depend on
the old entity registry entries.

## After Restart

Check the integration before changing entity IDs:

- All expected devices are present.
- Climate, sensor, binary sensor, switch, cover, and lock entities become available after polling.
- Existing automations still reference the intended entities.
- Diagnostics download still works.
- Logs do not show repeated setup, polling, or duplicate unique ID errors.

For duplicate-looking entities:

1. Compare the old and new entity state, device class, unit, and attributes.
2. Check which entity your dashboards and automations currently use.
3. Disable the unused entity first if you are not sure.
4. Delete old registry entries only after confirming they are not used.
5. Rename the kept entity if you need to preserve the old dashboard or automation name.

## When To Open An Issue

Open a Support / Bug issue if migration leaves missing devices, unavailable
entities, duplicate unique ID warnings, or command failures. Attach diagnostics
and include:

- The old fork URL.
- The old and new `homeassistant_salus` versions if known.
- Home Assistant version.
- Gateway model, such as UGE600 or UG800.
- A list of affected entity IDs.

## Rollback

If you need to roll back, reinstall the previous fork from HACS and restart
Home Assistant. Restore your Home Assistant backup if the migration changed
entity registry data in a way you cannot easily undo from the UI.
