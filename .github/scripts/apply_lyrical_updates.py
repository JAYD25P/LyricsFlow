from pathlib import Path
root = Path("app/src/main")
def edit(path, fn):
    p = root / path
    s = p.read_text()
    p.write_text(fn(s))

def model(s):
    return s.replace(
        'SYSTEM("System colours"), SOLID("Solid"), GRADIENT("Gradient"), ALBUM_ART("Album art"), IMAGE("My photo")',
        'SYSTEM("System colours"), SOLID("Solid"), GRADIENT("Gradient"), ALBUM_ART("Album art"), IMAGE("My photo"), ICE("Ice"), GLASS("Glass")')
edit("java/com/lyricflow/data/Model.kt", model)

def lyrics(s):
    s = s.replace("import androidx.compose.foundation.layout.matchParentSize", "import androidx.compose.foundation.layout.fillMaxSize")
    s = s.replace('if (s.bgMode == BgMode.SYSTEM) LyricColors(dyn?.onSurface ?: Color.White, dyn?.primary ?: Color(0xFFFF6FD8))\n    else LyricColors(Color(s.textColor), Color(s.accentColor))',
                  'if (s.bgMode == BgMode.SYSTEM) LyricColors(dyn?.onSurface ?: Color.White, dyn?.primary ?: Color(0xFFFF6FD8))\n    else if (s.bgMode == BgMode.ICE) LyricColors(Color(0xFF142B3A), Color(0xFF135D78))\n    else LyricColors(Color(s.textColor), Color(s.accentColor))')
    s = s.replace("Modifier.matchParentSize()", "Modifier.fillMaxSize()")
    old_typewriter = '''        } else if (active && style == AnimStyle.TYPEWRITER) {
            val shownChars = (main.length * progress * 1.25f).roundToInt().coerceIn(0, main.length)
            addStyle(SpanStyle(color = Color.Transparent), shownChars, main.length)
        }'''
    new_typewriter = '''        } else if (active && style == AnimStyle.TYPEWRITER) {
            val codePoints = main.codePointCount(0, main.length)
            val shownChars = (codePoints * progress * 1.25f).roundToInt().coerceIn(0, codePoints)
            val revealEnd = main.offsetByCodePoints(0, shownChars)
            addStyle(SpanStyle(color = c.accent), 0, revealEnd)
            addStyle(SpanStyle(color = Color.Transparent), revealEnd, main.length)
        }'''
    if old_typewriter not in s:
        raise SystemExit("Typewriter source block did not match; stopping safely.")
    s = s.replace(old_typewriter, new_typewriter)
    s = s.replace('''            BgMode.GRADIENT ->
                Box(Modifier.fillMaxSize().background(Brush.linearGradient(gradient.colors.map { Color(it) }), alpha = a))''',
    '''            BgMode.GRADIENT ->
                Box(Modifier.fillMaxSize().background(Brush.linearGradient(gradient.colors.map { Color(it) }), alpha = a))
            BgMode.ICE -> {
                Box(Modifier.fillMaxSize().background(Brush.linearGradient(listOf(Color(0xFFB9E7F5), Color(0xFF6E9FB8), Color(0xFFD9F4FA))), alpha = a))
                Box(Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.22f)))
            }
            BgMode.GLASS -> {
                Box(Modifier.fillMaxSize().background(Brush.linearGradient(listOf(Color(0xFF101827), Color(0xFF26364A), Color(0xFF111827))), alpha = a))
                Box(Modifier.fillMaxSize().background(Color(0xFF081526).copy(alpha = 0.38f)))
            }''')
    s = s.replace('else 0.4f) else 0.38f + 0.62f * a', 'else 0.72f) else 0.68f + 0.32f * a')
    s = s.replace('style = TextStyle(shadow = glow),', 'style = TextStyle(shadow = glow ?: Shadow(color = Color.Black.copy(alpha = 0.55f), blurRadius = 5f)),')
    s = s.replace('color = c.text.copy(alpha = 0.6f),', 'color = c.text.copy(alpha = 0.88f),')
    return s
edit("java/com/lyricflow/ui/LyricsView.kt", lyrics)

def screens(s):
    s = s.replace('Section("Background", "Opacity lets your wallpaper show through the widget.")',
                  'Section("Background & widget style", "Choose a look for the live home-screen lyrics widget too. Ice gives a cool frosted finish; Glass uses a smoked translucent panel.")')
    # Make the settings-screen when expression exhaustive for the added modes.
    if "BgMode.ICE -> Text(" not in s:
        anchor = "BgMode.SYSTEM -> Text("
        if anchor not in s:
            raise SystemExit("Could not locate BackgroundMode settings when-expression in Screens.kt")
        s = s.replace(anchor,
            'BgMode.ICE -> Text("Cool frosted-glass finish with an icy blue tint.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)' + chr(10) + '                BgMode.GLASS -> Text("Smoked translucent glass with a soft highlight and border.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)' + chr(10) + '                ' + anchor, 1)
    return s
edit("java/com/lyricflow/ui/Screens.kt", screens)

def renderer(s):
    return s.replace('''            BgMode.IMAGE -> {''', '''            BgMode.ICE -> {
      drawGradient(c, listOf(0xFFB9E7F5.toInt(), 0xFF6E9FB8.toInt(), 0xFFD9F4FA.toInt()))
      val frost = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(92, 225, 248, 255) }
      c.drawRoundRect(RectF(12f, 12f, W - 12f, H - 12f), 42f, 42f, frost)
      val shine = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(70, 255, 255, 255) }
      c.drawRect(0f, 0f, W.toFloat(), H * 0.22f, shine)
  }
  BgMode.GLASS -> {
      drawGradient(c, listOf(0xFF101827.toInt(), 0xFF26364A.toInt(), 0xFF111827.toInt()))
      val pane = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(130, 8, 15, 26) }
      c.drawRoundRect(RectF(10f, 10f, W - 10f, H - 10f), 48f, 48f, pane)
      val edge = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(95, 255, 255, 255); style = Paint.Style.STROKE; strokeWidth = 5f }
      c.drawRoundRect(RectF(12f, 12f, W - 12f, H - 12f), 46f, 46f, edge)
  }
  BgMode.IMAGE -> {''')
edit("java/com/lyricflow/widget/BackgroundRenderer.kt", renderer)

def widget(s):
    # Normalize Intent imports: keep exactly one Android Intent import and
    # remove competing/duplicate short-name imports that make Kotlin ambiguous.
    import_lines = s.splitlines()
    import_lines = [line for line in import_lines
                    if not (line.startswith("import ") and line.endswith(".Intent")
                            and line != "import android.content.Intent")]
    while import_lines.count("import android.content.Intent") > 1:
        import_lines.remove("import android.content.Intent")
    if "import android.content.Intent" not in import_lines:
        try:
            context_index = import_lines.index("import android.content.Context")
            import_lines.insert(context_index + 1, "import android.content.Intent")
        except ValueError:
            import_lines.insert(0, "import android.content.Intent")
    s = "\n".join(import_lines)
    s = s.replace("WidgetBody(s, np, bg, listening)", "WidgetBody(s, np, bg, listening, context)")
    s = s.replace("private fun WidgetBody(s: LyricSettings, np: NowPlaying, bg: Bitmap?, listening: Boolean)", "private fun WidgetBody(s: LyricSettings, np: NowPlaying, bg: Bitmap?, listening: Boolean, context: Context)")
    s = s.replace("ColorProvider(Color(s.textColor).copy(alpha = 0.55f))", "ColorProvider(Color(s.textColor).copy(alpha = 0.82f))")
    s = s.replace("val text: ColorProvider = if (system) GlanceTheme.colors.onSurface else ColorProvider(Color(s.textColor))",
                  "val text: ColorProvider = if (system) GlanceTheme.colors.onSurface else if (s.bgMode == BgMode.ICE) ColorProvider(Color(0xFF142B3A)) else ColorProvider(Color(s.textColor))")
    s = s.replace("else ColorProvider(Color(s.textColor).copy(alpha = 0.82f))",
                  "else if (s.bgMode == BgMode.ICE) ColorProvider(Color(0xFF29495A).copy(alpha = 0.88f)) else ColorProvider(Color(s.textColor).copy(alpha = 0.82f))")
    s = s.replace("else ColorProvider(Color(s.accentColor))",
                  "else if (s.bgMode == BgMode.ICE) ColorProvider(Color(0xFF135D78)) else ColorProvider(Color(s.accentColor))")
    # Keep the widget's existing lyric text rendering. Typewriter animation
    # remains implemented in the in-app lyrics view; Glance widget updates are
    # launcher-throttled and should not depend on fragile source rewriting.
    s = s.replace("actionStartActivity<MainActivity>()", "actionStartActivity(Intent(context, MainActivity::class.java))")
    return s
edit("java/com/lyricflow/widget/LyricWidget.kt", widget)

def service(s):
    return s.replace('''                val next = np.lyrics.getOrNull(np.indexAt(pos) + 1) ?: break
      delay(((next.timeMs - pos) / np.speed).toLong().coerceAtLeast(40L))
      redraw()''',
    '''                val next = np.lyrics.getOrNull(np.indexAt(pos) + 1)
      val untilNextLine = next?.let { ((it.timeMs - pos) / np.speed).toLong().coerceAtLeast(40L) } ?: 1000L
      // Redraw at lyric boundaries and at least once per second while playing.
      // The periodic refresh recovers from dropped media-session callbacks.
      delay(minOf(untilNextLine, 1000L))
      redraw()''')
edit("java/com/lyricflow/playback/LyricListenerService.kt", service)

p = root / "res/values/strings.xml"
p.write_text(p.read_text().replace("<string name=\"app_name\">LyricFlow</string>", "<string name=\"app_name\">Lyrical</string>").replace("Live, synced lyrics for whatever is playing", "Lyrical live synced lyrics widget"))

edit("java/com/lyricflow/ui/Screens.kt", screens)

def renderer(s):
    return s.replace('''            BgMode.IMAGE -> {''', '''            BgMode.ICE -> {
      drawGradient(c, listOf(0xFFB9E7F5.toInt(), 0xFF6E9FB8.toInt(), 0xFFD9F4FA.toInt()))
      val frost = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(92, 225, 248, 255) }
      c.drawRoundRect(RectF(12f, 12f, W - 12f, H - 12f), 42f, 42f, frost)
      val shine = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(70, 255, 255, 255) }
      c.drawRect(0f, 0f, W.toFloat(), H * 0.22f, shine)
  }
  BgMode.GLASS -> {
      drawGradient(c, listOf(0xFF101827.toInt(), 0xFF26364A.toInt(), 0xFF111827.toInt()))
      val pane = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(130, 8, 15, 26) }
      c.drawRoundRect(RectF(10f, 10f, W - 10f, H - 10f), 48f, 48f, pane)
      val edge = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(95, 255, 255, 255); style = Paint.Style.STROKE; strokeWidth = 5f }
      c.drawRoundRect(RectF(12f, 12f, W - 12f, H - 12f), 46f, 46f, edge)
  }
  BgMode.IMAGE -> {''')
edit("java/com/lyricflow/widget/BackgroundRenderer.kt", renderer)

def widget(s):
    s = s.replace("import com.lyricflow.data.Align", "import com.lyricflow.data.Align" + chr(10) + "import com.lyricflow.data.AnimStyle")
    s = s.replace("import android.content.Context", "import android.content.Context" + chr(10) + "import android.content.Intent")
    s = s.replace("WidgetBody(s, np, bg, listening)", "WidgetBody(s, np, bg, listening, context)")
    s = s.replace("private fun WidgetBody(s: LyricSettings, np: NowPlaying, bg: Bitmap?, listening: Boolean)", "private fun WidgetBody(s: LyricSettings, np: NowPlaying, bg: Bitmap?, listening: Boolean, context: Context)")
    s = s.replace("ColorProvider(Color(s.textColor).copy(alpha = 0.55f))", "ColorProvider(Color(s.textColor).copy(alpha = 0.82f))")
    s = s.replace("val text: ColorProvider = if (system) GlanceTheme.colors.onSurface else ColorProvider(Color(s.textColor))",
                  "val text: ColorProvider = if (system) GlanceTheme.colors.onSurface else if (s.bgMode == BgMode.ICE) ColorProvider(Color(0xFF142B3A)) else ColorProvider(Color(s.textColor))")
    s = s.replace("else ColorProvider(Color(s.textColor).copy(alpha = 0.82f))",
                  "else if (s.bgMode == BgMode.ICE) ColorProvider(Color(0xFF29495A).copy(alpha = 0.88f)) else ColorProvider(Color(s.textColor).copy(alpha = 0.82f))")
    s = s.replace("else ColorProvider(Color(s.accentColor))",
                  "else if (s.bgMode == BgMode.ICE) ColorProvider(Color(0xFF135D78)) else ColorProvider(Color(s.accentColor))")
    old_line = '''                                val (main, sub) = LyricText.prepare(s.scriptMode, raw)
                                val current = k == 0
                                Text(
                                    main,'''
    new_line = '''                                val (main, sub) = LyricText.prepare(s.scriptMode, raw)
                                val current = k == 0
                                val displayMain = if (current && s.animStyle == AnimStyle.TYPEWRITER) {
                                    val start = np.lyrics.getOrNull(idx)?.timeMs ?: 0L
                                    val end = np.lyrics.getOrNull(idx + 1)?.timeMs ?: (start + 4000L)
                                    val progress = ((np.positionMs() + s.syncOffsetMs - start).toFloat() / (end - start).coerceAtLeast(1L)).coerceIn(0f, 1f)
                                    val count = main.codePointCount(0, main.length)
                                    val endIndex = main.offsetByCodePoints(0, (count * progress * 1.25f).toInt().coerceIn(0, count))
                                    main.substring(0, endIndex) + if (endIndex < main.length) "▏" else ""
                                } else main
                                Text(
                                    displayMain,'''
    if old_line not in s:
        raise SystemExit("Widget lyric renderer source block did not match; stopping safely.")
    s = s.replace(old_line, new_line)
    s = s.replace("actionStartActivity<MainActivity>()", "actionStartActivity(Intent(context, MainActivity::class.java))")
    return s
edit("java/com/lyricflow/widget/LyricWidget.kt", widget)

def service(s):
    return s.replace('''                val next = np.lyrics.getOrNull(np.indexAt(pos) + 1) ?: break
      delay(((next.timeMs - pos) / np.speed).toLong().coerceAtLeast(40L))
      redraw()''',
    '''                val next = np.lyrics.getOrNull(np.indexAt(pos) + 1)
      val untilNextLine = next?.let { ((it.timeMs - pos) / np.speed).toLong().coerceAtLeast(40L) } ?: 1000L
      // Redraw at lyric boundaries and at least once per second while playing.
      // The periodic refresh recovers from dropped media-session callbacks.
      delay(minOf(untilNextLine, 1000L))
      redraw()''')
edit("java/com/lyricflow/playback/LyricListenerService.kt", service)

p = root / "res/values/strings.xml"
p.write_text(p.read_text().replace("<string name=\"app_name\">LyricFlow</string>", "<string name=\"app_name\">Lyrical</string>").replace("Live, synced lyrics for whatever is playing", "Lyrical live synced lyrics widget"))
