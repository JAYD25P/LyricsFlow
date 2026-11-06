# Lyrical — Android live lyrics

Lyrical is an Android synced-lyrics app with a coffee-inspired interface and a configurable home-screen lyrics widget.

## Coffee Edition update

- Espresso, mocha, caramel and cream Material 3 palette.
- Coffee, Ice, Glass, Solid, Gradient, Album Art and Photo backgrounds.
- Separate live lyrics and home-screen widget previews in the Customise tab.
- Typewriter, Karaoke, Fade, Slide, Zoom and Glow effects in the in-app preview.
- Widget styling follows saved font, alignment, size, colours, background, opacity and selected effect where supported by Glance.
- The notification-listener service requests widget refreshes every 500 ms during active playback.

Android launchers may coalesce or throttle widget redraw requests. The home-screen widget is best-effort live, not guaranteed frame-by-frame animation; the in-app preview remains continuously animated.

## Build APK

Open **Actions → Build APK → Run workflow**. Download the `Lyrical-APK` artifact from a successful run and extract `app-debug.apk` from the artifact ZIP.

Notification access is required to read active media-session metadata and synchronize lyrics.
