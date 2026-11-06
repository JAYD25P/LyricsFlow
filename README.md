# LyricsFlow — Android

This repository contains the Android APK build workflow. The project source archive must be uploaded at the repository root as `LyricFlow-Android-Source-Ready.zip`.

## Build APK

1. Upload `LyricFlow-Android-Source-Ready.zip` to the repository root (use the prepared ZIP from this ChatGPT conversation).
2. Open **Actions → Build APK → Run workflow**.
3. When the run completes, download the `LyricsFlow-APK` artifact. It contains `app-debug.apk`.

The workflow extracts the `LyricFlow/` project and builds it with JDK 17, Android SDK, and Gradle 8.9.
