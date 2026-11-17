# JS Library for X-Plane

A JavaScript library for glass-cockpit instruments that run in a browser view
inside X-Plane 12. It was written independently for the A380 for X-Plane 12
port and is meant for any aircraft.

- `xplane-js/data` (`data/`): datarefs, commands, plugin variables, key
  events, named plugin calls, settings, explicit units and the instrument
  host.
- `xplane-js/ui` (`lib/`): reactive values, an event bus, components with a
  JSX renderer (`UI.node`), an instrument board, and maths, formatting and
  navigation helpers.

`spec/data-api.d.ts` declares the DATA half.

## Similarity check

Every library file is compared with Microsoft's MSFS avionics framework by a
separate checker; the reports ship with each release.

License: GPL-3.0.
