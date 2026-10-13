# Fan fit

Ceiling fan sizing arithmetic: the room names the blade span, the ceiling names the drop, and the floor plan names the fans.

Live at https://ilanis-agent.github.io/fanfit/

## The three tools

- **Span plan** - room length x width gives the floor area; the smallest labeled span whose coverage holds it wins: 76 cm up to 7 m2, 107 cm up to 13 m2, 132 cm up to 23 m2, 152 cm up to 37 m2. Past 37 m2 the room wants a second fan.
- **Drop plan** - downrod = ceiling - labeled 30 cm fan body - labeled 240 cm target blade line, clamped at zero (flush mount). Below the labeled 240 cm minimum ceiling the tool refuses.
- **Count plan** - fan count = ceil(area / labeled 37 m2 coverage), spaced evenly along the long wall.

## Formulas and limits

- Areas and lengths are rounded to one decimal (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: spans, coverage, body drop, blade line, minimum ceiling.
- Illustrative sizing arithmetic only. A real fan hangs from a fan-rated box and follows the maker's instructions and the local electrical code; this is not a wiring ruling or a safety rating.

## Development

- `engine.js` - calculation and render engine (browser global `FanFit`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.
