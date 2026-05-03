# RS600 / SR600 Multifunction Mapping

RS600 and SR600 payloads are handled by protocol surface, with one product
correction:

- RS600 can expose a cover capability through `sLevelS`.
- RS600 can also expose separate relay switch endpoints through `sOnOffS`.
- SR600 is a dry relay switch and is not exposed as a cover.

For RS600, Home Assistant should keep each discovered capability as its own
entity. The cover entity keeps the base unique ID, while switch endpoints keep
their endpoint-specific unique IDs, such as `<UniID>_1` and `<UniID>_2`.

All related RS600/SR600 entities should use the base Salus `UniID` for the Home
Assistant device registry identifier. That groups the RS600 cover and relay
switches under one physical device instead of creating separate devices for each
endpoint.

Users should keep the entity type that matches the installation:

- Use the `cover` entity for shutters and blinds.
- Use the `switch` entities for independent relay channels.
- Disable the unused representation in Home Assistant.
- Do not assume RS600 cover and switch entities control independent outputs.
