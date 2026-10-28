# Relativity

Relativity brand showcase with a word-by-word tagline, tilt-reactive logo, and name card.

## Usage

The app opens with the tagline "The AI platform for legal data intelligence" shown one large word at a time, then fades in the Relativity logo. The three scenes (tagline, logo, and name card) rotate automatically, with the logo showing for one minute and the name card for 20 seconds (`DWELL_MS`). Press LEFT or RIGHT to move between them manually, which restarts the timer. On the logo scene, tilt the badge to move the logo and the drifting particles. Hold SELECT on the logo scene to swap to the "Rel" nickname, and keep holding to change to the "ty" thank-you. Release to return to the logo.

Edit `NAME`, `TITLE` and `TAGLINE` at the top of `__init__.py` to change the name card. To regenerate the logo images and icon, run `python tools/build_relativity_assets.py` (requires `pymupdf` and `pillow`).

No extra hardware or network access is required.

The logos use the colors and artwork from the Relativity brand guidelines at https://brand.relativity.com.
