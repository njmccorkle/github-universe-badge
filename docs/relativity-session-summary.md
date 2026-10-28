# Relativity badge app: session summary

Summary of the work done to bring the Relativity app from a VS Code prototype to a deployed Universe 2026 badge app.

## Setup

- The app was uncommitted in the main checkout, so `badge/apps/relativity/`, `docs/` and `tools/` were copied into a worktree for testing in the Badge Simulator canvas.
- The pre-flight check passed. Its only warning was that `icon.png` is 48x48 while the menu expects 24x24. The 48x48 icon was kept and tried on the badge as requested.

## App changes

| Change | Detail |
| --- | --- |
| Tagline intro | Replaced the sideways scroll with one large word at a time, each scaled to fill the screen. Timing is `WORD_MS` plus `WORD_MS_PER_CHAR` per letter. "intelligence" gets `LAST_WORD_EXTRA_MS` (800 ms) extra. |
| QR code | Removed the QR scene, `qr_data.py`, its import, and the QR generation and `qrcode` dependency in `tools/build_relativity_assets.py`. |
| Scene rotation | Tagline, logo and name card rotate automatically in a loop. LEFT and RIGHT move between scenes and restart the timer. |
| Dwell times | `DWELL_MS` holds a time per scene: logo 60 s, name card 20 s. The tagline advances on its own when its animation ends. |
| Name card | `NAME` is "Nathan McCorkle" and `TITLE` is "Senior Software Engineer". |
| Progress dots | The current dot is light gray on the name card, because orange was invisible on the orange background. |
| Easter egg | Holding SELECT on the logo scene swaps to the "Rel" nickname and, after about 1.8 s, to "ty / Thank you". Releasing returns to the logo. Auto-rotation pauses while SELECT is held. |
| README | Updated to describe the current behavior. |

## Deployment

- Installed with `mpremote` and USB mass-storage mode, following `hardware/USB_SERIAL.md`: the badge's menu lacked the icon patch, so the patched `badge/apps/menu/app.py` was copied along with the app.
- No reflash was needed. Apps are copied into `/system/apps/relativity/`.
- The app was redeployed after each change and verified on the badge before resetting to the menu.
- A stray `__pycache__` folder from a local compile check was removed from the badge.

## Open items

- The original design spec in `docs/superpowers/specs/` still lists the QR scene.
- The 24x24 icon fix was deferred; the icon is still 48x48.
- The Badge Simulator canvas had disconnected when the final timing change was made, so the one-minute logo scene was not run in the simulator.
