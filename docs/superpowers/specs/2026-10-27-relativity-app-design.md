# Relativity badge app design

A branded Universe 2026 badge app at `badge/apps/relativity/`, built from the Relativity brand guidelines (https://brand.relativity.com).

## Display and structure

- HIRES (320x240), `badge.mode(HIRES | VSYNC)`.
- Scene carousel. LEFT/RIGHT cycle scenes. The app opens on the intro.

## Scenes

1. **Intro:** scrolling "The AI platform for legal data intelligence" on Relativity Black, then a fade to the orange logo on Relativity Blue, then the Logo scene.
2. **Logo:** logo floats and shifts with IMU tilt over drifting orange particles. Hold SELECT to show the Rel / ty easter egg.
3. **Name card:** name and title on Relativity Orange with a white mark. Placeholders editable at the top of the file.
4. **QR code:** QR code for a placeholder URL on white. Uses a firmware QR helper if present, otherwise a precomputed bitmap.
5. **IR wave:** SELECT sends a short message over IR; received messages are displayed.

## Branding

- Palette: Orange #EF5F11, Blue #08253D, Green #166050, Black #16181C, White #FCFDFE.
- Logo only in orange or white, never stretched, outlined, rotated, shadowed or patterned.
- Neue Montreal and Inter are unavailable on the badge; use the closest built-in font.

## Assets

The user supplies the official orange and white logo and "R" files in `assets/`. They are converted to paletted PNGs. `icon.png` (48x48) comes from the "R" mark.

## Testing

Badge Simulator for scenes, input and rendering. IR and physical behavior need a real badge, so a hardware checklist is provided.
