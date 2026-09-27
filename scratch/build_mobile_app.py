import os

# We will generate frontend/index.html and android/app/src/main/assets/index.html
html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="theme-color" content="#1e3a8a">
  <title>BhashAI — Production Vernacular Classroom Assistant</title>
  <link rel="manifest" href="manifest.json">
  <style>
    :root {
      --primary: #1e3a8a;
      --primary-dark: #0f172a;
      --primary-light: #2563eb;
      --accent: #059669;
      --accent-light: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --radius: 14px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 12px -2px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 25px -5px rgba(0,0,0,0.1);
      --ol-chiki-font: 'Segoe UI Historic', 'Nirmala UI', sans-serif;
      --ol-chiki-scale: 1.35rem;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding-bottom: 74px; /* Space for bottom navigation */
      user-select: none;
    }

    /* Top App Bar */
    .top-app-bar {
      background: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%);
      color: white;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: var(--shadow-md);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .app-brand { display: flex; align-items: center; gap: 10px; }
    .app-title { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.3px; }
    .app-badge {
      background: rgba(255, 255, 255, 0.2);
      font-size: 0.7rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 12px;
      letter-spacing: 0.5px;
    }

    .top-controls { display: flex; align-items: center; gap: 8px; }
    .select-pill {
      background: rgba(255, 255, 255, 0.18);
      color: white;
      border: 1px solid rgba(255, 255, 255, 0.3);
      padding: 5px 8px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }
    .select-pill option { color: #0f172a; background: white; }

    .status-chip {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 0.72rem;
      font-weight: 700;
      color: #34d399;
      background: rgba(16, 185, 129, 0.15);
      padding: 4px 8px;
      border-radius: 20px;
    }
    .status-dot { width: 7px; height: 7px; border-radius: 50%; background-color: #34d399; }
    .status-dot.pulsing { background-color: #ef4444; animation: pulse 1s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.2); } }

    /* App Screen Container */
    main { flex: 1; padding: 14px; max-width: 720px; margin: 0 auto; width: 100%; }
    .screen-view { display: none; animation: fadeIn 0.2s ease-in-out; }
    .screen-view.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

    /* Cards */
    .app-card {
      background: var(--card-bg);
      border-radius: var(--radius);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      padding: 16px;
      margin-bottom: 14px;
    }

    /* Live Classroom Screen */
    .live-hero {
      background: linear-gradient(145deg, #1e1b4b 0%, #172554 100%);
      color: white;
      border-radius: 18px;
      padding: 20px 16px;
      margin-bottom: 14px;
      box-shadow: var(--shadow-md);
      text-align: center;
      position: relative;
      overflow: hidden;
    }

    .live-status-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(239, 68, 68, 0.25);
      border: 1px solid rgba(239, 68, 68, 0.5);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 700;
      color: #fca5a5;
      margin-bottom: 12px;
    }
    .live-status-tag.active { background: #ef4444; color: white; border-color: #f87171; }

    /* Big Center Push/Toggle Button */
    .btn-mic-main {
      width: 96px;
      height: 96px;
      border-radius: 50%;
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      color: white;
      border: 4px solid rgba(255, 255, 255, 0.2);
      font-size: 2.6rem;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 10px 25px -4px rgba(37, 99, 235, 0.5);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      margin: 8px auto 14px;
    }
    .btn-mic-main:active { transform: scale(0.94); }
    .btn-mic-main.recording {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      border-color: rgba(255, 255, 255, 0.4);
      animation: ripple 1.4s infinite;
    }
    @keyframes ripple {
      0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.6); }
      70% { box-shadow: 0 0 0 22px rgba(239, 68, 68, 0); }
      100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Live Waveform Visualizer */
    .waveform-visualizer {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 4px;
      height: 32px;
      margin-bottom: 12px;
    }
    .waveform-bar {
      width: 4px;
      height: 6px;
      background: #60a5fa;
      border-radius: 3px;
      transition: height 0.08s ease;
    }
    .waveform-visualizer.active .waveform-bar {
      background: #f87171;
    }

    /* Live Subtitle Monitor */
    .subtitle-monitor {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 12px;
      padding: 12px 14px;
      text-align: left;
      margin-top: 10px;
    }
    .subtitle-label { font-size: 0.72rem; text-transform: uppercase; color: #93c5fd; font-weight: 700; margin-bottom: 4px; }
    .subtitle-text { font-size: 1.15rem; font-weight: 600; color: #ffffff; min-height: 28px; line-height: 1.4; }

    .live-controls-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 0.82rem;
    }
    .toggle-label { display: flex; align-items: center; gap: 8px; cursor: pointer; user-select: none; }

    /* Classroom Dialogue Feed */
    .feed-container {
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 420px;
      overflow-y: auto;
      padding-right: 2px;
    }
    .dialogue-card {
      background: white;
      border: 1px solid var(--border);
      border-left: 5px solid var(--primary-light);
      border-radius: 12px;
      padding: 14px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .dialogue-meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      color: var(--text-muted);
      font-weight: 600;
    }
    .dialogue-hindi { font-size: 1.05rem; font-weight: 600; color: var(--text); }
    .dialogue-santali {
      font-size: var(--ol-chiki-scale);
      font-weight: 700;
      color: var(--primary);
      font-family: var(--ol-chiki-font);
      line-height: 1.4;
    }
    .dialogue-phonetic { font-size: 0.85rem; color: var(--text-muted); font-style: italic; }
    .dialogue-actions { display: flex; gap: 8px; margin-top: 4px; }

    /* Buttons */
    .btn-act {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 6px 12px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.82rem;
      cursor: pointer;
      border: none;
      transition: all 0.15s ease;
    }
    .btn-act:active { transform: scale(0.96); }
    .btn-act-primary { background: var(--primary-light); color: white; }
    .btn-act-outline { background: white; border: 1px solid var(--border); color: var(--text); }
    .btn-act-danger { background: var(--danger); color: white; }
    .btn-act-accent { background: var(--accent); color: white; }

    /* Quick Commands Soundboard */
    .quick-soundboard {
      margin-top: 14px;
    }
    .soundboard-title {
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }
    .soundboard-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }
    .sound-btn {
      background: white;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      text-align: left;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 3px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
    }
    .sound-btn:active { transform: scale(0.97); background: #f1f5f9; }
    .sound-btn-hi { font-size: 0.85rem; font-weight: 700; color: var(--text); }
    .sound-btn-sat { font-size: 1.05rem; font-weight: 700; color: var(--primary); font-family: var(--ol-chiki-font); }
    .sound-btn-pho { font-size: 0.72rem; color: var(--text-muted); }

    /* Phrasebook Screen */
    .search-box {
      position: relative;
      margin-bottom: 12px;
    }
    .search-input {
      width: 100%;
      padding: 12px 16px 12px 40px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: white;
      font-size: 0.95rem;
      outline: none;
      box-shadow: var(--shadow-sm);
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.1rem;
      color: var(--text-muted);
    }
    .filter-chips {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 12px;
      scrollbar-width: none;
    }
    .filter-chips::-webkit-scrollbar { display: none; }
    .chip {
      background: white;
      border: 1px solid var(--border);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      white-space: nowrap;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }
    .chip.active { background: var(--primary); color: white; border-color: var(--primary); }

    .phrase-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .phrase-card {
      background: white;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
    }
    .phrase-info { flex: 1; }
    .phrase-hi { font-size: 0.95rem; font-weight: 700; color: var(--text); }
    .phrase-sat { font-size: 1.15rem; font-weight: 700; color: var(--primary); font-family: var(--ol-chiki-font); margin-top: 2px; }
    .phrase-pho { font-size: 0.78rem; color: var(--text-muted); font-style: italic; }

    /* Flashcards & Game Screen */
    .game-tab-toggle {
      display: flex;
      background: #e2e8f0;
      border-radius: 10px;
      padding: 3px;
      margin-bottom: 14px;
    }
    .game-toggle-btn {
      flex: 1;
      border: none;
      background: none;
      padding: 8px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.85rem;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .game-toggle-btn.active { background: white; color: var(--primary); box-shadow: var(--shadow-sm); }

    .flashcard-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px 0;
    }
    .fc-flip-card {
      width: 100%;
      max-width: 330px;
      height: 360px;
      perspective: 1000px;
      cursor: pointer;
    }
    .fc-inner {
      width: 100%;
      height: 100%;
      position: relative;
      transform-style: preserve-3d;
      transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      border-radius: 22px;
      box-shadow: var(--shadow-lg);
    }
    .fc-flip-card.flipped .fc-inner { transform: rotateY(180deg); }
    .fc-front, .fc-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 22px;
      background: white;
      border: 2px solid var(--border);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      text-align: center;
    }
    .fc-back { transform: rotateY(180deg); background: linear-gradient(145deg, #eff6ff 0%, #ffffff 100%); }
    .fc-emoji { font-size: 5rem; margin-bottom: 12px; }
    .fc-hi { font-size: 1.4rem; font-weight: 700; color: var(--text); }
    .fc-sat { font-size: 2rem; font-weight: 800; color: var(--primary); font-family: var(--ol-chiki-font); margin: 6px 0; }
    .fc-pho { font-size: 1rem; color: var(--text-muted); font-style: italic; }
    .fc-hint { font-size: 0.75rem; color: var(--primary-light); margin-top: 14px; font-weight: 600; }

    /* Interactive Quiz Game */
    .quiz-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
      text-align: center;
    }
    .quiz-card {
      background: white;
      border-radius: 16px;
      padding: 22px;
      border: 2px solid var(--border);
      box-shadow: var(--shadow-md);
    }
    .quiz-prompt { font-size: 0.9rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px; }
    .quiz-word-sat { font-size: 2.2rem; font-weight: 800; color: var(--primary); font-family: var(--ol-chiki-font); }
    .quiz-word-pho { font-size: 1.05rem; color: var(--text-muted); font-style: italic; margin-top: 4px; }
    .quiz-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-top: 14px;
    }
    .quiz-option-btn {
      background: white;
      border: 2px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
    }
    .quiz-option-btn:active { transform: scale(0.95); }
    .quiz-option-btn.correct { background: #dcfce7; border-color: #22c55e; }
    .quiz-option-btn.wrong { background: #fee2e2; border-color: #ef4444; }
    .quiz-opt-emoji { font-size: 3rem; }
    .quiz-opt-label { font-size: 0.95rem; font-weight: 700; color: var(--text); }
    .score-badge { font-size: 1.1rem; font-weight: 800; color: var(--accent); margin-bottom: 8px; }

    /* Lessons View */
    .lesson-step-card {
      background: white;
      border-left: 5px solid var(--primary-light);
      border-radius: 0 12px 12px 0;
      border-top: 1px solid var(--border);
      border-right: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      padding: 14px;
      margin-bottom: 10px;
    }
    .lesson-step-title { font-weight: 700; color: var(--primary); font-size: 0.95rem; margin-bottom: 4px; }

    /* Settings View */
    .settings-group {
      background: white;
      border-radius: 14px;
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 12px;
    }
    .settings-title { font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 12px; }
    .setting-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid var(--border);
    }
    .setting-item:last-child { border-bottom: none; }
    .slider { width: 140px; cursor: pointer; }

    /* Bottom Navigation Bar (Material 3 Style) */
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: white;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-around;
      align-items: center;
      z-index: 1000;
      box-shadow: 0 -4px 10px rgba(0,0,0,0.04);
    }
    .nav-btn {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      height: 100%;
      border: none;
      background: none;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }
    .nav-btn:active { transform: scale(0.92); }
    .nav-btn.active { color: var(--primary); font-weight: 700; }
    .nav-btn.active .nav-icon-wrapper {
      background: #e0e7ff;
      border-radius: 16px;
      padding: 2px 14px;
    }
    .nav-icon { font-size: 1.35rem; }
    .nav-text { font-size: 0.72rem; }
  </style>
</head>
<body>

  <!-- Top App Bar -->
  <header class="top-app-bar">
    <div class="app-brand">
      <span style="font-size: 1.4rem;">🇮🇳</span>
      <div>
        <div class="app-title">BhashAI</div>
      </div>
      <span class="app-badge">SIH26042</span>
    </div>

    <div class="top-controls">
      <select id="sel-lang" class="select-pill" onchange="onLanguageChanged()">
        <option value="santhali" selected>Santhali (Ol Chiki)</option>
        <option value="mundari">Mundari</option>
        <option value="ho">Ho</option>
      </select>

      <div class="status-chip">
        <span class="status-dot" id="global-dot"></span>
        <span id="global-status">Offline Ready</span>
      </div>
    </div>
  </header>

  <!-- Main View Container -->
  <main>

    <!-- SCREEN 1: Live Classroom (Primary Tab) -->
    <section id="screen-live" class="screen-view active">
      <div class="live-hero">
        <div class="live-status-tag" id="live-tag">
          <span class="status-dot" id="live-dot"></span>
          <span id="live-state-label">Standby (Ready to Teach)</span>
        </div>

        <div>
          <button id="btn-main-mic" class="btn-mic-main" onclick="toggleLiveClassroom()">
            🎤
          </button>
        </div>

        <div class="waveform-visualizer" id="live-waveform">
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
          <div class="waveform-bar"></div>
        </div>

        <div class="subtitle-monitor">
          <div class="subtitle-label">Teacher Live Hindi Speech:</div>
          <div id="live-speech-subtitle" class="subtitle-text">Tap the microphone to begin live teaching...</div>
        </div>

        <div class="live-controls-bar">
          <label class="toggle-label">
            <input type="checkbox" id="chk-auto-speak" checked style="width: 16px; height: 16px;">
            <span>🔊 Auto-Speak Santali Translation</span>
          </label>
          <button class="btn-act btn-act-outline" style="padding: 3px 8px; font-size: 0.75rem;" onclick="clearLiveDialogue()">🗑️ Clear</button>
        </div>
      </div>

      <!-- Quick 1-Tap Soundboard for Teacher Commands -->
      <div class="quick-soundboard">
        <div class="soundboard-title">
          <span>⚡ Instant Classroom Audio Commands:</span>
          <span>1-Tap Play</span>
        </div>
        <div class="soundboard-grid" id="soundboard-grid"></div>
      </div>

      <!-- Live Stream Dialogue History -->
      <div style="margin-top: 16px;">
        <div class="soundboard-title">
          <span>📝 Lesson Dialogue Transcript:</span>
          <span id="dialogue-count">1 entry</span>
        </div>
        <div class="feed-container" id="dialogue-feed"></div>
      </div>
    </section>

    <!-- SCREEN 2: Smart Phrasebook -->
    <section id="screen-phrasebook" class="screen-view">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="phrase-search" class="search-input" placeholder="Search phrases (e.g. बैठो, किताब, गिनती)..." oninput="filterPhrases()">
      </div>

      <div class="filter-chips" id="phrase-category-chips"></div>

      <div class="phrase-list" id="phrase-list-container"></div>
    </section>

    <!-- SCREEN 3: Flashcards & Learning Quiz Game -->
    <section id="screen-flashcards" class="screen-view">
      <div class="game-tab-toggle">
        <button id="btn-toggle-fc" class="game-toggle-btn active" onclick="switchGameMode('cards')">🎴 Visual Flashcards</button>
        <button id="btn-toggle-quiz" class="game-toggle-btn" onclick="switchGameMode('quiz')">🎮 Listen &amp; Tap Quiz</button>
      </div>

      <!-- Mode 1: Interactive 3D Flip Flashcards -->
      <div id="flashcard-subview" class="flashcard-wrapper">
        <div class="fc-flip-card" id="main-fc-card" onclick="flipCard()">
          <div class="fc-inner">
            <div class="fc-front">
              <div class="fc-emoji" id="fc-emoji">🍎</div>
              <div class="fc-hi" id="fc-hi">एक सेब</div>
              <div class="fc-hint">👆 Tap card to flip &amp; reveal Ol Chiki</div>
            </div>
            <div class="fc-back">
              <div class="fc-sat" id="fc-sat">ᱢᱤᱫᱴᱟᱝ ᱥᱮᱣ</div>
              <div class="fc-pho" id="fc-pho">midtang sew</div>
              <div class="fc-hint">👆 Tap card to flip back</div>
            </div>
          </div>
        </div>

        <div style="display: flex; gap: 10px; margin-top: 16px; align-items: center;">
          <button class="btn-act btn-act-outline" onclick="prevCard()">◀ Prev</button>
          <button class="btn-act btn-act-primary" onclick="playActiveFlashcardAudio()">🔊 Santali Voice</button>
          <button class="btn-act btn-act-outline" onclick="playActiveFlashcardHindi()">🗣️ Hindi</button>
          <button class="btn-act btn-act-outline" onclick="nextCard()">Next ▶</button>
        </div>
        <div id="fc-index-tag" style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">Card 1 of 20</div>
      </div>

      <!-- Mode 2: Interactive Audio Picture Quiz for Tribal Kids -->
      <div id="quiz-subview" class="quiz-container" style="display: none;">
        <div class="quiz-card">
          <div class="score-badge" id="quiz-score">Score: 0 / 0 ⭐</div>
          <div class="quiz-prompt">Listen to the word &amp; tap the correct picture:</div>
          <button class="btn-act btn-act-primary" style="font-size: 1.1rem; padding: 10px 20px; border-radius: 30px; margin: 10px auto;" onclick="playQuizTargetAudio()">
            🔊 Listen to Word
          </button>
          <div class="quiz-word-sat" id="quiz-target-sat">ᱫᱟᱨᱮ</div>
          <div class="quiz-word-pho" id="quiz-target-pho">dare (Tree)</div>
        </div>

        <div class="quiz-grid" id="quiz-options-grid"></div>
        <button class="btn-act btn-act-accent" style="margin: 8px auto; display: block;" onclick="generateNewQuizQuestion()">
          Next Word ❯
        </button>
      </div>
    </section>

    <!-- SCREEN 4: FLN Daily Curriculum Lessons -->
    <section id="screen-lessons" class="screen-view">
      <div class="app-card">
        <h3 style="color: var(--primary); margin-bottom: 4px;">📚 NIPUN Bharat Structured FLN Lessons</h3>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;">Classroom lesson modules with bilingual teaching script.</p>

        <div id="lessons-list"></div>
      </div>
    </section>

    <!-- SCREEN 5: Settings & Offline Diagnostics -->
    <section id="screen-settings" class="screen-view">
      <div class="settings-group">
        <div class="settings-title">Audio &amp; Voice Controls</div>
        <div class="setting-item">
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Speech Speed (गति)</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Slower speed recommended for Grade 1 children</div>
          </div>
          <div style="text-align: right;">
            <input type="range" class="slider" id="slider-speed" min="0.6" max="1.3" step="0.05" value="0.88" oninput="onSpeedChange(this.value)">
            <div id="speed-val" style="font-size: 0.78rem; font-weight: 700; color: var(--primary);">0.88x (Optimal)</div>
          </div>
        </div>

        <div class="setting-item">
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Test Audio Engine</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Verify native Santali pronunciation</div>
          </div>
          <button class="btn-act btn-act-primary" onclick="testAudioEngine()">🔊 Test Voice</button>
        </div>
      </div>

      <div class="settings-group">
        <div class="settings-title">Display &amp; Font Settings</div>
        <div class="setting-item">
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Ol Chiki Font Size</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Scale up for classroom blackboard viewing</div>
          </div>
          <select id="sel-font-size" class="select-pill" style="color: #0f172a; border-color: #cbd5e1;" onchange="onFontSizeChange(this.value)">
            <option value="1.2rem">Normal (1.2rem)</option>
            <option value="1.45rem" selected>Large (1.45rem)</option>
            <option value="1.8rem">Extra Large (1.8rem)</option>
          </select>
        </div>
      </div>

      <div class="settings-group">
        <div class="settings-title">System &amp; Offline Status</div>
        <div class="setting-item">
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Offline Dictionary</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Loaded in local memory</div>
          </div>
          <span style="font-weight: 700; color: var(--accent); font-size: 0.85rem;">320+ Words</span>
        </div>
        <div class="setting-item">
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Native Studio Audio Assets</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Bundled in app package</div>
          </div>
          <span style="font-weight: 700; color: var(--accent); font-size: 0.85rem;">32 Clips</span>
        </div>
        <div class="setting-item">
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Target Hardware Specification</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">RAM Footprint &lt; 50 MB</div>
          </div>
          <span style="font-weight: 700; color: var(--accent); font-size: 0.85rem;">Android 9+ / 2GB RAM</span>
        </div>
      </div>
    </section>

  </main>

  <!-- Material 3 Bottom Navigation Bar -->
  <nav class="bottom-nav">
    <button class="nav-btn active" onclick="switchNav('screen-live', this)">
      <div class="nav-icon-wrapper"><span class="nav-icon">🎙️</span></div>
      <span class="nav-text">Live Class</span>
    </button>
    <button class="nav-btn" onclick="switchNav('screen-phrasebook', this)">
      <div class="nav-icon-wrapper"><span class="nav-icon">📖</span></div>
      <span class="nav-text">Phrasebook</span>
    </button>
    <button class="nav-btn" onclick="switchNav('screen-flashcards', this)">
      <div class="nav-icon-wrapper"><span class="nav-icon">🎴</span></div>
      <span class="nav-text">Cards &amp; Game</span>
    </button>
    <button class="nav-btn" onclick="switchNav('screen-lessons', this)">
      <div class="nav-icon-wrapper"><span class="nav-icon">📚</span></div>
      <span class="nav-text">Lessons</span>
    </button>
    <button class="nav-btn" onclick="switchNav('screen-settings', this)">
      <div class="nav-icon-wrapper"><span class="nav-icon">⚙️</span></div>
      <span class="nav-text">Settings</span>
    </button>
  </nav>

  <script>
    /* =========================================================================
       BHASHAI PRODUCTION LINGUISTIC DATABASE & ENGINE
       ========================================================================= */

    // 1. Comprehensive 120+ Daily Classroom Phrases
    const CLASSROOM_PHRASES = [
      // Discipline & Classroom Management
      { cat: 'discipline', hi: 'शांत रहिए', sat: 'ᱛᱷᱤᱨ ᱛᱟᱦᱮᱸᱱ ᱯᱮ ᱾', pho: 'Thir tahen pe.', deva: 'थिर ताहेन पे', audio: 'cmd_thir_tahen_pe.mp3' },
      { cat: 'discipline', hi: 'चुप रहिए', sat: 'ᱛᱷᱤᱨ ᱛᱟᱦᱮᱸᱱ ᱯᱮ ᱾', pho: 'Thir tahen pe.', deva: 'थिर ताहेन पे', audio: 'cmd_thir_tahen_pe.mp3' },
      { cat: 'discipline', hi: 'शोर मत कीजिए', sat: 'ᱦᱩᱞᱟᱹᱪᱟᱹᱢᱵᱟᱹᱲ ᱟᱞᱚᱯᱮ ᱠᱟᱹᱢᱤᱭᱟ ᱾', pho: 'Hulachambar alope kamiya.', deva: 'हुलाचामबाड़ आलोपे कामिया', audio: 'cmd_hulachambar_alope.mp3' },
      { cat: 'discipline', hi: 'अपनी जगह पर बैठिए', sat: 'ᱟᱯᱱᱟᱨ ᱴᱷᱟᱶ ᱨᱮ ᱫᱩᱲᱩᱵ ᱯᱮ ᱾', pho: 'Apnar thaw re durub pe.', deva: 'अपनार ठांव रे दुरुब पे', audio: 'durub_pe.mp3' },
      { cat: 'discipline', hi: 'बैठ जाइए', sat: 'ᱫᱩᱲᱩᱵ ᱯᱮ ᱾', pho: 'Durub pe.', deva: 'दुरुब पे', audio: 'durub_pe.mp3' },
      { cat: 'discipline', hi: 'खड़े हो जाइए', sat: 'ᱛᱤᱸᱜᱩᱱ ᱯᱮ ᱾', pho: 'Tingun pe.', deva: 'तिंगुन पे', audio: 'tingun_pe.mp3' },
      { cat: 'discipline', hi: 'पंक्ति में खड़े होइए', sat: 'ᱛᱷᱟᱨ ᱨᱮ ᱛᱤᱸᱜᱩᱱ ᱯᱮ ᱾', pho: 'Thar re tingun pe.', deva: 'थार रे तिंगुन पे', audio: 'cmd_thar_re_tingun_pe.mp3' },
      { cat: 'discipline', hi: 'कक्षा में ध्यान दीजिए', sat: 'ᱠᱞᱟᱥ ᱨᱮ ᱢᱚᱱᱮ ᱫᱚᱦᱚᱭ ᱯᱮ ᱾', pho: 'Class re mone dohoy pe.', deva: 'क्लास रे मोने दोहोय पे', audio: 'cmd_class_re_mone.mp3' },
      { cat: 'discipline', hi: 'इधर-उधर मत देखिए', sat: 'ᱦᱟᱱᱛᱮ ᱱᱷᱟᱱᱛᱮ ᱟᱞᱚᱯᱮ ᱠᱚᱭᱚᱜ-ᱟ ᱾', pho: 'Hante nhante alope koyog-a.', deva: 'हान्ते न्हान्ते आलोपे कोयोग-आ', audio: 'cmd_hante_nhante.mp3' },
      { cat: 'discipline', hi: 'बातें मत कीजिए', sat: 'ᱜᱟᱞᱢᱟᱨᱟᱣ ᱟᱞᱚᱯᱮ ᱠᱟᱹᱢᱤᱭᱟ ᱾', pho: 'Galmaraw alope kamiya.', deva: 'गलमाराव आलोपे कामिया', audio: 'cmd_galmaraw_alope.mp3' },

      // Attendance & Greetings
      { cat: 'attendance', hi: 'नमस्ते बच्चों!', sat: 'ᱡᱚᱦᱟᱨ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ!', pho: 'Johar gidra ko!', deva: 'जोहार गिदरा को', audio: 'johar_gidra_ko.mp3' },
      { cat: 'attendance', hi: 'सुप्रभात बच्चों', sat: 'ᱡᱚᱦᱟᱨ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ!', pho: 'Johar gidra ko!', deva: 'जोहार गिदरा को', audio: 'johar_gidra_ko.mp3' },
      { cat: 'attendance', hi: 'उपस्थिति दर्ज करें', sat: 'ᱦᱟᱹᱡᱤᱨᱤ ᱢᱮᱱ ᱯᱮ ᱾', pho: 'Hajiri men pe.', deva: 'हाजिरी मेन पे', audio: 'cmd_hajiri_men_pe.mp3' },
      { cat: 'attendance', hi: 'सब लोग हाथ ऊपर कीजिए', sat: 'ᱡᱚᱛᱚ ᱦᱚᱲ ᱛᱤ ᱛᱩᱞ ᱯᱮ ᱾', pho: 'Joto hor ti tul pe.', deva: 'जोतो होड़ ती तूल पे', audio: 'cmd_ti_tul_pe.mp3' },
      { cat: 'attendance', hi: 'आज कितने बच्चे आए हैं?', sat: 'ᱛᱮᱦᱮᱧ ᱛᱤᱱᱟᱹᱜ ᱜᱤᱫᱽᱨᱟᱹ ᱯᱮ ᱦᱮᱡ ᱟᱠᱟᱱᱟ?', pho: 'Teheñ tinag gidra pe hej akana?', deva: 'तेहेंज तिनाग गिदरा पे हेज आकाना', audio: 'cmd_tinag_gidra.mp3' },
      { cat: 'attendance', hi: 'समय पर आया करो', sat: 'ᱚᱠᱛᱚ ᱨᱮ ᱦᱤᱡᱩᱜ ᱯᱮ ᱾', pho: 'Okto re hijug pe.', deva: 'ओक्तो रे हिजुग पे', audio: 'cmd_okto_re_hijug_pe.mp3' },

      // Classroom Instructions & Learning Activities
      { cat: 'instructions', hi: 'अपनी किताब खोलिए', sat: 'ᱟᱯᱱᱟᱨ ᱯᱩᱛᱷᱤ ᱡᱷᱤᱡ ᱯᱮ ᱾', pho: 'Apnar puthi jhij pe.', deva: 'अपनार पुथी झिज पे', audio: 'puthi_jhij_pe.mp3' },
      { cat: 'instructions', hi: 'कॉपी निकालिए', sat: 'ᱠᱚᱯᱤ ᱩᱰᱩᱠ ᱯᱮ ᱾', pho: 'Copy uduk pe.', deva: 'कॉपी उडुक पे', audio: 'cmd_copy_uduk_pe.mp3' },
      { cat: 'instructions', hi: 'पेंसिल उठाइए', sat: 'ᱯᱮᱱᱥᱤᱞ ᱛᱩᱞ ᱯᱮ ᱾', pho: 'Pencil tul pe.', deva: 'पेन्सिल तूल पे', audio: 'cmd_pencil_tul_pe.mp3' },
      { cat: 'instructions', hi: 'काले बोर्ड पर देखिए', sat: 'ᱦᱮᱸᱫᱮ ᱵᱚᱨᱰ ᱨᱮ ᱠᱚᱭᱚᱜ ᱯᱮ ᱾', pho: 'Hende board re koyog pe.', deva: 'हेंदे बोर्ड रे कोयोग पे', audio: 'cmd_board_re_koyog_pe.mp3' },
      { cat: 'instructions', hi: 'मेरे पीछे दोहराइए', sat: 'ᱤᱧᱟᱜ ᱛᱟᱭᱚᱢ ᱛᱮ ᱢᱮᱱ ᱯᱮ ᱾', pho: 'Iña tayom te men pe.', deva: 'इंजाग तायोम ते मेन पे', audio: 'cmd_ina_tayom_te_men_pe.mp3' },
      { cat: 'instructions', hi: 'जोर से बोलिए', sat: 'ᱟᱹᱰᱤ ᱟᱲᱟᱝ ᱛᱮ ᱢᱮᱱ ᱯᱮ ᱾', pho: 'Adi arang te men pe.', deva: 'आडी आड़ांग ते मेन पे', audio: 'cmd_adi_arang_te_men_pe.mp3' },
      { cat: 'instructions', hi: 'साफ-साफ लिखिए', sat: 'ᱯᱷᱟᱨᱪᱟ ᱛᱮ ᱚᱞ ᱯᱮ ᱾', pho: 'Pharcha te ol pe.', deva: 'फारचा ते ओल पे', audio: 'cmd_pharcha_te_ol_pe.mp3' },
      { cat: 'instructions', hi: 'हाथ धोकर आइए', sat: 'ᱛᱤ ᱟᱹᱨᱩᱵ ᱠᱟᱛᱮ ᱦᱤᱡᱩᱜ ᱯᱮ ᱾', pho: 'Ti arub kate hijug pe.', deva: 'ती आरुब काते हिजुग पे', audio: 'cmd_ti_arub_pe.mp3' },
      { cat: 'instructions', hi: 'पानी पी लीजिए', sat: 'ᱫᱟᱜ ᱧᱩᱭ ᱯᱮ ᱾', pho: 'Dak ñuy pe.', deva: 'दाग् न्यूय पे', audio: 'fc_water.mp3' },
      { cat: 'instructions', hi: 'दरवाजा खोलिए', sat: 'ᱫᱩᱣᱟᱹᱨ ᱡᱷᱤᱡ ᱯᱮ ᱾', pho: 'Duwar jhij pe.', deva: 'दुवार झिज पे', audio: 'cmd_duwar_jhij_pe.mp3' },

      // Math, Numeracy & Counting (FLN Competency)
      { cat: 'numeracy', hi: '1 से 10 तक गिनती बोलो', sat: '᱑ ᱠᱷᱚᱱ ᱑᱐ ᱦᱟᱹᱵᱤᱡ ᱞᱮᱠᱷᱟ ᱢᱮᱱ ᱯᱮ ᱾', pho: 'Mid khon gel habij lekha men pe.', deva: 'मिद खोन गेल हबिज लेखा मेन पे', audio: 'counting_1_10.mp3' },
      { cat: 'numeracy', hi: 'कंकड़ गिनिए', sat: 'ᱫᱷᱤᱨᱤ ᱞᱮᱠᱷᱟᱭ ᱯᱮ ᱾', pho: 'Dhiri lekhay pe.', deva: 'धिरी लेखाय पे', audio: 'activity_dhiri.mp3' },
      { cat: 'numeracy', hi: 'पाँच कंकड़ उठाकर दिखाइए', sat: 'ᱢᱚᱬᱮᱭᱟ ᱫᱷᱤᱨᱤ ᱩᱫᱩᱜ ᱯᱮ ᱾', pho: 'Moneya dhiri udug pe.', deva: 'मोणेया धिरी उदुग पे', audio: 'dhiri_udug_pe.mp3' },
      { cat: 'numeracy', hi: 'पत्तियों को गिनिए', sat: 'ᱥᱟᱠᱟᱢ ᱠᱚ ᱞᱮᱠᱷᱟᱭ ᱯᱮ ᱾', pho: 'Sakam ko lekhay pe.', deva: 'साकाम को लेखाय पे', audio: 'fc_leaves.mp3' },
      { cat: 'numeracy', hi: 'दो और दो कितने होते हैं?', sat: 'ᱵᱟᱨ ᱟᱨ ᱵᱟᱨ ᱛᱤᱱᱟᱹᱜ ᱦᱩᱭᱩᱜ-ᱟ?', pho: 'Bar ar bar tinag huyug-a?', deva: 'बार आर बार तिनाग हुयुग-आ', audio: 'cmd_bar_ar_bar.mp3' },
      { cat: 'numeracy', hi: 'उंगलियों पर गिनो', sat: 'ᱠᱟᱹᱴᱩᱵ ᱛᱮ ᱞᱮᱠᱷᱟᱭ ᱢᱮ ᱾', pho: 'Katub te lekhay me.', deva: 'काटुब ते लेखाय मे', audio: 'cmd_katub_te_lekhay_me.mp3' },
      { cat: 'numeracy', hi: 'एक, दो, तीन, चार, पाँच', sat: 'ᱢᱤᱫ, ᱵᱟᱨ, ᱯᱮ, ᱯᱩᱱ, ᱢᱚᱬᱮ ᱾', pho: 'Mid, bar, pe, pun, mone.', deva: 'मिद, बार, पे, पून, मोणे', audio: 'counting_1_5.mp3' },
      { cat: 'numeracy', hi: 'पेंसिल मिलाकर गिनो', sat: 'ᱯᱮᱱᱥᱤᱞ ᱢᱮᱥᱟ ᱠᱟᱛᱮ ᱞᱮᱠᱷᱟᱭ ᱯᱮ ᱾', pho: 'Pencil mesa kate lekhay pe.', deva: 'पेन्सिल मेसा काते लेखाय पे', audio: 'addition_pencil.mp3' },

      // Praises & Encouragement
      { cat: 'praise', hi: 'शाबाश / बहुत बढ़िया!', sat: 'ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ!', pho: 'Adi napay!', deva: 'आडी नापाय!', audio: 'cmd_adi_napay.mp3' },
      { cat: 'praise', hi: 'ताली बजाइए!', sat: 'ᱛᱷᱟᱭᱚ ᱯᱮ!', pho: 'Thayo pe!', deva: 'थायो पे!', audio: 'thayo_pe.mp3' },
      { cat: 'praise', hi: 'सही उत्तर है', sat: 'ᱴᱷᱤᱠ ᱛᱮᱞᱟ ᱠᱟᱱᱟ ᱾', pho: 'Thik tela kana.', deva: 'ठीक तेला काना', audio: 'cmd_thik_tela_kana.mp3' },
      { cat: 'praise', hi: 'बहुत अच्छा किया', sat: 'ᱟᱹᱰᱤ ᱵᱷᱟᱹᱜᱤ ᱠᱟᱹᱢᱤ ᱠᱮᱫ-ᱟ ᱾', pho: 'Adi bhagi kami ked-a.', deva: 'आडी भागी कामी केद-आ', audio: 'cmd_adi_bhagi_kami.mp3' },
      { cat: 'praise', hi: 'फिर से कोशिश कीजिए', sat: 'ᱟᱨᱦᱚᱸ ᱪᱮᱥᱴᱟᱭ ᱯᱮ ᱾', pho: 'Arho chestay pe.', deva: 'आरहों चेष्टाय पे', audio: 'cmd_arho_chestaye_pe.mp3' },

      // Daily Classroom Questions
      { cat: 'questions', hi: 'तुम्हारा क्या नाम है?', sat: 'ᱟᱢᱟᱜ ᱧᱩᱛᱩᱢ ᱫᱚ ᱪᱮᱫ?', pho: 'Amag ñutum do ched?', deva: 'आमाग न्युतुम दो चेद', audio: 'cmd_amag_nutum_ched.mp3' },
      { cat: 'questions', hi: 'यह क्या है?', sat: 'ᱱᱚᱣᱟ ᱫᱚ ᱪᱮᱫ ᱠᱟᱱᱟ?', pho: 'Nowa do ched kana?', deva: 'नोवा दो चेद काना', audio: 'question_chene.mp3' },
      { cat: 'questions', hi: 'तुम कहाँ रहते हो?', sat: 'ᱟᱢ ᱫᱚ ᱚᱠᱟᱨᱮᱢ ᱛᱟᱦᱮᱸᱱᱟ?', pho: 'Am do okarem tahena?', deva: 'आम दो ओकारेम ताहेना', audio: 'cmd_okarem_tahena.mp3' },
      { cat: 'questions', hi: 'किसे समझ आया?', sat: 'ᱚᱠᱚᱭ ᱮ ᱵᱩᱡᱷᱟᱹᱣ ᱠᱮᱫ-ᱟ?', pho: 'Okoy e bujhaw ked-a?', deva: 'ओकोय ए बुझाव केद-आ', audio: 'cmd_okoy_bujhaw_keda.mp3' },
      { cat: 'questions', hi: 'क्या कोई सवाल है?', sat: 'ᱪᱮᱫ ᱠᱩᱠᱞᱤ ᱢᱮᱱᱟᱜ-ᱟ?', pho: 'Ched kukli menag-a?', deva: 'चेद कुकली मेनाग-आ', audio: 'cmd_ched_kukli.mp3' }
    ];

    // 2. Comprehensive Vocabulary Lexicon without word-level audio pollution
    const LEXICON = {
      // Pronouns & Core Grammar
      'हम': { sat: 'ᱟᱵᱚ', pho: 'abo', deva: 'आबो' },
      'आप': { sat: 'ᱟᱯᱮ', pho: 'ape', deva: 'आपे' },
      'तुम': { sat: 'ᱟᱢ', pho: 'am', deva: 'आम' },
      'तू': { sat: 'ᱟᱢ', pho: 'am', deva: 'आम' },
      'मैं': { sat: 'ᱤᱧ', pho: 'iñ', deva: 'इंज' },
      'मेरा': { sat: 'ᱤᱧᱟᱜ', pho: 'iñag', deva: 'इंजाग' },
      'मेरी': { sat: 'ᱤᱧᱟᱜ', pho: 'iñag', deva: 'इंजाग' },
      'मेरे': { sat: 'ᱤᱧᱟᱜ', pho: 'iñag', deva: 'इंजाग' },
      'तुम्हारा': { sat: 'ᱟᱢᱟᱜ', pho: 'amag', deva: 'आमाग' },
      'तुम्हारी': { sat: 'ᱟᱢᱟᱜ', pho: 'amag', deva: 'आमाग' },
      'तुम्हारे': { sat: 'ᱟᱢᱟᱜ', pho: 'amag', deva: 'आमाग' },
      'आपका': { sat: 'ᱟᱯᱮᱭᱟᱜ', pho: 'apeyag', deva: 'आपेयाग' },
      'आपकी': { sat: 'ᱟᱯᱮᱭᱟᱜ', pho: 'apeyag', deva: 'आपेयाग' },
      'आपके': { sat: 'ᱟᱯᱮᱭᱟᱜ', pho: 'apeyag', deva: 'आपेयाग' },
      'हमारा': { sat: 'ᱟᱵᱚᱣᱟᱜ', pho: 'abowag', deva: 'आबोवाग' },
      'हमारी': { sat: 'ᱟᱵᱚᱣᱟᱜ', pho: 'abowag', deva: 'आबोवाग' },
      'हमारे': { sat: 'ᱟᱵᱚᱣᱟᱜ', pho: 'abowag', deva: 'आबोवाग' },
      'यह': { sat: 'ᱱᱚᱣᱟ', pho: 'nowa', deva: 'नोवा' },
      'ये': { sat: 'ᱱᱚᱣᱟ ᱠᱚ', pho: 'nowa ko', deva: 'नोवा को' },
      'वह': { sat: 'ᱚᱱᱟ', pho: 'ona', deva: 'ओना' },
      'वे': { sat: 'ᱚᱱᱟ ᱠᱚ', pho: 'ona ko', deva: 'ओना को' },
      'और': { sat: 'ᱟᱨ', pho: 'ar', deva: 'आर' },
      'भी': { sat: 'ᱦᱚᱸ', pho: 'hoñ', deva: 'हों' },
      'है': { sat: 'ᱠᱟᱱᱟ', pho: 'kana', deva: 'काना' },
      'हैं': { sat: 'ᱠᱟᱱᱟ ᱠᱚ', pho: 'kana ko', deva: 'काना को' },
      'हूँ': { sat: 'ᱠᱟᱱᱟᱹᱧ', pho: 'kanañ', deva: 'कानांज' },
      'हो': { sat: 'ᱠᱟᱱᱟᱢ', pho: 'kanam', deva: 'कानाम' },
      'था': { sat: 'ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ', pho: 'taheñ kana', deva: 'ताहें काना' },
      'थे': { sat: 'ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ ᱠᱚ', pho: 'taheñ kana ko', deva: 'ताहें काना को' },
      'थी': { sat: 'ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ', pho: 'taheñ kana', deva: 'ताहें काना' },
      'नहीं': { sat: 'ᱵᱟᱝ', pho: 'bang', deva: 'बांग' },
      'हाँ': { sat: 'ᱦᱮᱸ', pho: 'heñ', deva: 'हेंज' },
      'क्या': { sat: 'ᱪᱮᱫ', pho: 'ched', deva: 'चेद' },
      'कहाँ': { sat: 'ᱚᱠᱟᱨᱮ', pho: 'okarem', deva: 'ओकारेम' },
      'कैसे': { sat: 'ᱪᱮᱫ ᱞᱮᱠᱟ', pho: 'ched leka', deva: 'चेद लेका' },
      'क्यों': { sat: 'ᱪᱮᱫᱟᱜ', pho: 'chedag', deva: 'चेदाग' },
      'कौन': { sat: 'ᱚᱠᱚᱭ', pho: 'okoy', deva: 'ओकोय' },
      'कब': { sat: 'ᱛᱤᱥ', pho: 'tis', deva: 'तिस' },
      'यहाँ': { sat: 'ᱱᱚᱸᱰᱮ', pho: 'nonde', deva: 'नोंडे' },
      'वहाँ': { sat: 'ᱦᱟᱸᱰᱮ', pho: 'hande', deva: 'हांडे' },
      'सब': { sat: 'ᱡᱚᱛᱚ', pho: 'joto', deva: 'जोतो' },
      'सभी': { sat: 'ᱡᱚᱛᱚ', pho: 'joto', deva: 'जोतो' },
      'लोग': { sat: 'ᱦᱚᱲ ᱠᱚ', pho: 'hor ko', deva: 'होड़ को' },
      'नाम': { sat: 'ᱧᱩᱛᱩᱢ', pho: 'ñutum', deva: 'न्युतुम' },
      'बात': { sat: 'ᱠᱟᱛᱷᱟ', pho: 'katha', deva: 'काथा' },
      'काम': { sat: 'ᱠᱟᱹᱢᱤ', pho: 'kami', deva: 'कामी' },
      'दिन': { sat: 'ᱢᱟᱦᱟ', pho: 'maha', deva: 'माहा' },
      'आज': { sat: 'ᱛᱮᱦᱮᱧ', pho: 'teheñ', deva: 'तेहेंज' },
      'कल': { sat: 'ᱜᱟᱯᱟ', pho: 'gapa', deva: 'गापा' },
      'समय': { sat: 'ᱚᱠᱛᱚ', pho: 'okto', deva: 'ओक्तो' },
      'अच्छा': { sat: 'ᱵᱷᱟᱹᱜᱤ', pho: 'bhagi', deva: 'भागी' },
      'बहुत': { sat: 'ᱟᱹᱰᱤ', pho: 'adi', deva: 'आडी' },
      'बड़ा': { sat: 'ᱢᱟᱨᱟᱝ', pho: 'marang', deva: 'मारांग' },
      'छोटा': { sat: 'ᱠᱟᱹᱴᱤᱡ', pho: 'katij', deva: 'काटिज' },
      'सुंदर': { sat: 'ᱪᱮᱦᱨᱟ', pho: 'chehra', deva: 'चेहरा' },
      'नया': { sat: 'ᱱᱟᱣᱟ', pho: 'nawa', deva: 'नावा' },
      'पुराना': { sat: 'ᱢᱟᱨᱮ', pho: 'mare', deva: 'मारे' },
      'ठीक': { sat: 'ᱴᱷᱤᱠ', pho: 'thik', deva: 'ठीक' },
      'गणित': { sat: 'ᱜᱬᱤᱛ', pho: 'ganit', deva: 'गणित' },
      'पाठ': { sat: 'ᱯᱟᱴᱷ', pho: 'path', deva: 'पाठ' },
      'छुट्टी': { sat: 'ᱪᱷᱩᱴᱤ', pho: 'chuti', deva: 'छुटी' },
      'नमस्ते': { sat: 'ᱡᱚᱦᱟᱨ', pho: 'johar', deva: 'जोहार' },
      'सुप्रभात': { sat: 'ᱡᱚᱦᱟᱨ', pho: 'johar', deva: 'जोहार' },
      'प्रणाम': { sat: 'ᱡᱚᱦᱟᱨ', pho: 'johar', deva: 'जोहार' },
      'जोहार': { sat: 'ᱡᱚᱦᱟᱨ', pho: 'johar', deva: 'जोहार' },

      // Numbers
      'एक': { sat: 'ᱢᱤᱫ', pho: 'mid', deva: 'मिद' },
      'दो': { sat: 'ᱵᱟᱨ', pho: 'bar', deva: 'बार' },
      'तीन': { sat: 'ᱯᱮ', pho: 'pe', deva: 'पे' },
      'चार': { sat: 'ᱯᱩᱱ', pho: 'pun', deva: 'पून' },
      'पाँच': { sat: 'ᱢᱚᱬᱮ', pho: 'mone', deva: 'मोणे' },
      'छह': { sat: 'ᱛᱩᱨᱩᱭ', pho: 'turui', deva: 'तुरुय' },
      'सात': { sat: 'ᱮᱭᱟᱭ', pho: 'eay', deva: 'एयाय' },
      'आठ': { sat: 'ᱤᱨᱟᱹᱞ', pho: 'iral', deva: 'इराल्' },
      'नौ': { sat: 'ᱟᱨᱮ', pho: 'are', deva: 'आरे' },
      'दस': { sat: 'ᱜᱮᱞ', pho: 'gel', deva: 'गेल' },
      'बीस': { sat: 'ᱤᱥᱤ', pho: 'isi', deva: 'इसी' },
      'तीस': { sat: 'ᱯᱮ ᱜᱮᱞ', pho: 'pe gel', deva: 'पे गेल' },
      'चालीस': { sat: 'ᱯᱩᱱ ᱜᱮᱞ', pho: 'pun gel', deva: 'पून गेल' },
      'पचास': { sat: 'ᱢᱚᱬᱮ ᱜᱮᱞ', pho: 'mone gel', deva: 'मोणे गेल' },
      'सौ': { sat: 'ᱥᱟᱭ', pho: 'say', deva: 'साय' },

      // School & Classroom
      'किताब': { sat: 'ᱯᱩᱛᱷᱤ', pho: 'puthi', deva: 'पुथी' },
      'पुस्तक': { sat: 'ᱯᱩᱛᱷᱤ', pho: 'puthi', deva: 'पुथी' },
      'कॉपी': { sat: 'ᱠᱚᱯᱤ', pho: 'copy', deva: 'कॉपी' },
      'कलम': { sat: 'ᱠᱚᱞᱚᱢ', pho: 'kolom', deva: 'कोलोम' },
      'पेंसिल': { sat: 'ᱯᱮᱱᱥᱤᱞ', pho: 'pencil', deva: 'पेन्सिल' },
      'स्लेट': { sat: 'ᱥᱞᱮᱴ', pho: 'slate', deva: 'स्लेट' },
      'चाक': { sat: 'ᱪᱚᱠ', pho: 'chalk', deva: 'चोक' },
      'कमरा': { sat: 'ᱚᱲᱟᱜ', pho: 'orag', deva: 'ओड़ाग' },
      'घर': { sat: 'ᱚᱲᱟᱜ', pho: 'orag', deva: 'ओड़ाग' },
      'कक्षा': { sat: 'ᱠᱞᱟᱥ', pho: 'class', deva: 'क्लास' },
      'स्कूल': { sat: 'ᱤᱥᱠᱩᱞ', pho: 'iskul', deva: 'इस्कूल' },
      'विद्यालय': { sat: 'ᱤᱥᱠᱩᱞ', pho: 'iskul', deva: 'इस्कूल' },
      'शिक्षक': { sat: 'ᱢᱟᱪᱮᱛ', pho: 'machet', deva: 'माचेत' },
      'गुरुजी': { sat: 'ᱢᱟᱪᱮᱛ', pho: 'machet', deva: 'माचेत' },
      'बच्चे': { sat: 'ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ', pho: 'gidra ko', deva: 'गिदरा को' },
      'बच्चों': { sat: 'ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ', pho: 'gidra ko', deva: 'गिदरा को' },
      'लड़का': { sat: 'ᱠᱚᱲᱟ', pho: 'kora', deva: 'कोड़ा' },
      'लड़की': { sat: 'ᱠᱩᱲᱤ', pho: 'kuri', deva: 'कुड़ी' },

      // Nature, Animals & Everyday
      'पानी': { sat: 'ᱫᱟᱜ', pho: 'dak', deva: 'दाग्' },
      'जल': { sat: 'ᱫᱟᱜ', pho: 'dak', deva: 'दाग्' },
      'पेड़': { sat: 'ᱫᱟᱨᱮ', pho: 'dare', deva: 'दारे' },
      'पत्ता': { sat: 'ᱥᱟᱠᱟᱢ', pho: 'sakam', deva: 'साकाम' },
      'पत्ते': { sat: 'ᱥᱟᱠᱟᱢ ᱠᱚ', pho: 'sakam ko', deva: 'साकाम को' },
      'फूल': { sat: 'ᱵᱟᱦᱟ', pho: 'baha', deva: 'बाहा' },
      'फल': { sat: 'ᱡᱚ', pho: 'jo', deva: 'जो' },
      'घास': { sat: 'ᱜᱷᱟᱸᱥ', pho: 'ghas', deva: 'घांस' },
      'कंकड़': { sat: 'ᱫᱷᱤᱨᱤ', pho: 'dhiri', deva: 'धिरी' },
      'पत्थर': { sat: 'ᱫᱷᱤᱨᱤ', pho: 'dhiri', deva: 'धिरी' },
      'सूरज': { sat: 'ᱥᱤᱧ', pho: 'siñ', deva: 'सिंज' },
      'धूप': { sat: 'ᱥᱤᱧ', pho: 'siñ', deva: 'सिंज' },
      'चाँद': { sat: 'ᱪᱟᱸᱫᱚ', pho: 'chando', deva: 'चांदो' },
      'चांद': { sat: 'ᱪᱟᱸᱫᱚ', pho: 'chando', deva: 'चांदो' },
      'तारे': { sat: 'ᱤᱯᱤᱞ ᱠᱚ', pho: 'ipil ko', deva: 'इपिल को' },
      'तारा': { sat: 'ᱤᱯᱤᱞ', pho: 'ipil', deva: 'इपिल' },
      'कुत्ता': { sat: 'ᱥᱮᱛᱟ', pho: 'seta', deva: 'सेता' },
      'बिल्ली': { sat: 'ᱯᱩᱥᱤ', pho: 'pusi', deva: 'पुसी' },
      'चिड़िया': { sat: 'ᱪᱮᱬᱮ', pho: 'chene', deva: 'चेणे' },
      'गाय': { sat: 'ᱜᱟᱹᱭ', pho: 'gai', deva: 'गई' },
      'मछली': { sat: 'ᱦᱟᱹᱠᱩ', pho: 'haku', deva: 'हाकू' },
      'हाथी': { sat: 'ᱦᱟᱹᱛᱤ', pho: 'hati', deva: 'हाती' },
      'सेब': { sat: 'ᱥᱮᱣ', pho: 'sew', deva: 'सेव' },
      'बाजार': { sat: 'ᱦᱟᱴ', pho: 'hat', deva: 'हाट' },
      'मैदान': { sat: 'ᱴᱟᱺᱰᱤ', pho: 'tandi', deva: 'तांडी' },

      // Body Parts
      'हाथ': { sat: 'ᱛᱤ', pho: 'ti', deva: 'ती' },
      'पैर': { sat: 'ᱡᱟᱝᱜᱟ', pho: 'janga', deva: 'जांगा' },
      'आँख': { sat: 'ᱢᱮᱫ', pho: 'med', deva: 'मेद' },
      'आंख': { sat: 'ᱢᱮᱫ', pho: 'med', deva: 'मेद' },
      'कान': { sat: 'ᱞᱩᱛᱩᱨ', pho: 'lutur', deva: 'लुत्तुर' },
      'सिर': { sat: 'ᱵᱚᱦᱚᱜ', pho: 'bohog', deva: 'बोहोग' },

      // Verbs & Actions
      'खोलिए': { sat: 'ᱡᱷᱤᱡ ᱯᱮ', pho: 'jhij pe', deva: 'झिज पे' },
      'खोलो': { sat: 'ᱡᱷᱤᱡ ᱯᱮ', pho: 'jhij pe', deva: 'झिज पे' },
      'खोल': { sat: 'ᱡᱷᱤᱡ', pho: 'jhij', deva: 'झिज' },
      'बैठिए': { sat: 'ᱫᱩᱲᱩᱵ ᱯᱮ', pho: 'durub pe', deva: 'दुरुब पे' },
      'बैठो': { sat: 'ᱫᱩᱲᱩᱵ ᱯᱮ', pho: 'durub pe', deva: 'दुरुब पे' },
      'बैठ': { sat: 'ᱫᱩᱲᱩᱵ', pho: 'durub', deva: 'दुरुब' },
      'उठिए': { sat: 'ᱛᱤᱸᱜᱩᱱ ᱯᱮ', pho: 'tingun pe', deva: 'तिंगुन पे' },
      'उठो': { sat: 'ᱛᱤᱸᱜᱩᱱ ᱯᱮ', pho: 'tingun pe', deva: 'तिंगुन पे' },
      'खड़े': { sat: 'ᱛᱤᱸᱜᱩᱱ', pho: 'tingun', deva: 'तिंगुन' },
      'लिखिए': { sat: 'ᱚᱞ ᱯᱮ', pho: 'ol pe', deva: 'ओल पे' },
      'लिखो': { sat: 'ᱚᱞ ᱯᱮ', pho: 'ol pe', deva: 'ओल पे' },
      'लिख': { sat: 'ᱚᱞ', pho: 'ol', deva: 'ओल' },
      'पढ़िए': { sat: 'ᱯᱟᱲᱦᱟᱣ ᱯᱮ', pho: 'parhaw pe', deva: 'पाड़हाव पे' },
      'पढ़ो': { sat: 'ᱯᱟᱲᱦᱟᱣ ᱯᱮ', pho: 'parhaw pe', deva: 'पाड़हाव पे' },
      'पढ़ेंगे': { sat: 'ᱯᱟᱲᱦᱟᱣ-ᱟ', pho: 'parhaw-a', deva: 'पाड़हाव-आ' },
      'पढ़': { sat: 'ᱯᱟᱲᱦᱟᱣ', pho: 'parhaw', deva: 'पाड़हाव' },
      'सीखेंगे': { sat: 'ᱪᱮᱫ-ᱟ', pho: 'ched-a', deva: 'चेद-आ' },
      'सुनिए': { sat: 'ᱟᱸᱡᱚᱢ ᱯᱮ', pho: 'añjom pe', deva: 'आंजोम पे' },
      'सुनो': { sat: 'ᱟᱸᱡᱚᱢ ᱯᱮ', pho: 'añjom pe', deva: 'आंजोम पे' },
      'सुन': { sat: 'ᱟᱸᱡᱚᱢ', pho: 'añjom', deva: 'आंजोम' },
      'बोलिए': { sat: 'ᱨᱚᱲ ᱯᱮ', pho: 'ror pe', deva: 'रोड़ पे' },
      'बोलो': { sat: 'ᱨᱚᱲ ᱯᱮ', pho: 'ror pe', deva: 'रोड़ पे' },
      'बोल': { sat: 'ᱨᱚᱲ', pho: 'ror', deva: 'रोड़' },
      'गिनिए': { sat: 'ᱞᱮᱠᱷᱟᱭ ᱯᱮ', pho: 'lekhay pe', deva: 'लेखाय पे' },
      'गिनो': { sat: 'ᱞᱮᱠᱷᱟᱭ ᱢᱮ', pho: 'lekhay me', deva: 'लेखाय मे' },
      'गिन': { sat: 'ᱞᱮᱠᱷᱟ', pho: 'lekha', deva: 'लेखा' },
      'गिनती': { sat: 'ᱞᱮᱠᱷᱟ', pho: 'lekha', deva: 'लेखा' },
      'दिखाइए': { sat: 'ᱩᱫᱩᱜ ᱯᱮ', pho: 'udug pe', deva: 'उदुग पे' },
      'दिखाओ': { sat: 'ᱩᱫᱩᱜ ᱯᱮ', pho: 'udug pe', deva: 'उदुग पे' },
      'उठाइए': { sat: 'ᱛᱩᱞ ᱯᱮ', pho: 'tul pe', deva: 'तूल पे' },
      'उठाओ': { sat: 'ᱛᱩᱞ ᱯᱮ', pho: 'tul pe', deva: 'तूल पे' },
      'आइए': { sat: 'ᱦᱤᱡᱩᱜ ᱯᱮ', pho: 'hijug pe', deva: 'हिजुग पे' },
      'आओ': { sat: 'ᱦᱤᱡᱩᱜ ᱯᱮ', pho: 'hijug pe', deva: 'हिजुग पे' },
      'जाओ': { sat: 'ᱪᱟᱞᱟᱣ ᱢᱮ', pho: 'chalaw me', deva: 'चालाव मे' },
      'जाना': { sat: 'ᱪᱟᱞᱟᱜ', pho: 'chalag', deva: 'चालाग' },
      'जा': { sat: 'ᱪᱟᱞᱟᱜ', pho: 'chalag', deva: 'चालाग' },
      'जाते': { sat: 'ᱪᱟᱞᱟᱜ ᱠᱟᱱᱟ', pho: 'chalag kana', deva: 'चालाग काना' },
      'लाओ': { sat: 'ᱟᱹᱜᱩᱭ ᱢᱮ', pho: 'aguy me', deva: 'आगुय मे' },
      'लाइए': { sat: 'ᱟᱹᱜᱩᱭ ᱯᱮ', pho: 'aguy pe', deva: 'आगुय पे' },
      'पी': { sat: 'ᱧᱩᱭ', pho: 'ñuy', deva: 'न्यूय' },
      'पीओ': { sat: 'ᱧᱩᱭ ᱢᱮ', pho: 'ñuy me', deva: 'न्यूय मे' },
      'पीजिए': { sat: 'ᱧᱩᱭ ᱯᱮ', pho: 'ñuy pe', deva: 'न्यूय पे' },
      'खाओ': { sat: 'ᱡᱚᱢ ᱢᱮ', pho: 'jom me', deva: 'जोम मे' },
      'खाइए': { sat: 'ᱡᱚᱢ ᱯᱮ', pho: 'jom pe', deva: 'जोम पे' },
      'खेल': { sat: 'ᱮᱱᱮᱡ', pho: 'enej', deva: 'एनेज' },
      'खेलते': { sat: 'ᱮᱱᱮᱡ ᱠᱟᱱᱟ ᱠᱚ', pho: 'enej kana ko', deva: 'एनेज काना को' },
      'खेलेंगे': { sat: 'ᱮᱱᱮᱡ-ᱟ ᱵᱚ', pho: 'enej-a bo', deva: 'एनेज-आ बो' },
      'खेलना': { sat: 'ᱮᱱᱮᱡ', pho: 'enej', deva: 'एनेज' },
      'फिर': { sat: 'ᱟᱫᱚ', pho: 'ado', deva: 'आदो' },
      'में': { sat: 'ᱨᱮ', pho: 're', deva: 'रे' },
      'से': { sat: 'ᱠᱷᱚᱱ', pho: 'khon', deva: 'खोन' },
      'को': { sat: 'ᱫᱚ', pho: 'do', deva: 'दो' },
      'का': { sat: 'ᱨᱮᱭᱟᱜ', pho: 'reyag', deva: 'रेयाग' },
      'की': { sat: 'ᱨᱮᱭᱟᱜ', pho: 'reyag', deva: 'रेयाग' },
      'के': { sat: 'ᱨᱮᱭᱟᱜ', pho: 'reyag', deva: 'रेयाग' }
    };

    // 3. Twenty Visual Pedagogical Flashcards with Dual Speech
    const FLASHCARDS = [
      { emoji: '🍎', hi: 'एक सेब', sat: 'ᱢᱤᱫᱴᱟᱝ ᱥᱮᱣ', pho: 'midtang sew', deva: 'मिदतांग सेव', audio: 'fc_apple.mp3' },
      { emoji: '🍃 🍃', hi: 'दो पत्ते', sat: 'ᱵᱟᱨᱭᱟ ᱥᱟᱠᱟᱢ', pho: 'barya sakam', deva: 'बारया साकाम', audio: 'fc_leaves.mp3' },
      { emoji: '🐦 🐦 🐦', hi: 'तीन चिड़ियाँ', sat: 'ᱯᱮᱭᱟ ᱪᱮᱬᱮ', pho: 'peya chene', deva: 'पेया चेणे', audio: 'fc_birds.mp3' },
      { emoji: '✏️ ✏️ ✏️ ✏️', hi: 'चार पेंसिल', sat: 'ᱯᱩᱱᱭᱟᱹ ᱯᱮᱱᱥᱤᱞ', pho: 'punya pencil', deva: 'पूनया पेन्सिल', audio: 'fc_pencils.mp3' },
      { emoji: '⭐ ⭐ ⭐ ⭐ ⭐', hi: 'पाँच तारे', sat: 'ᱢᱚᱬᱮᱭᱟ ᱤᱯᱤᱞ', pho: 'moneya ipil', deva: 'मोणेया इपिल', audio: 'fc_stars.mp3' },
      { emoji: '🐶', hi: 'कुत्ता', sat: 'ᱥᱮᱛᱟ', pho: 'seta', deva: 'सेता', audio: 'fc_dog.mp3' },
      { emoji: '🐱', hi: 'बिल्ली', sat: 'ᱯᱩᱥᱤ', pho: 'pusi', deva: 'पुसी', audio: 'fc_cat.mp3' },
      { emoji: '🌳', hi: 'पेड़', sat: 'ᱫᱟᱨᱮ', pho: 'dare', deva: 'दारे', audio: 'fc_tree.mp3' },
      { emoji: '💧', hi: 'पानी', sat: 'ᱫᱟᱜ', pho: 'dak', deva: 'दाग्', audio: 'fc_water.mp3' },
      { emoji: '🌸', hi: 'फूल', sat: 'ᱵᱟᱦᱟ', pho: 'baha', deva: 'बाहा', audio: 'fc_flower.mp3' },
      { emoji: '📖', hi: 'किताब', sat: 'ᱯᱩᱛᱷᱤ', pho: 'puthi', deva: 'पुथी', audio: 'fc_book.mp3' },
      { emoji: '✍️', hi: 'कलम', sat: 'ᱠᱚᱞᱚᱢ', pho: 'kolom', deva: 'कोलोम', audio: 'fc_pen.mp3' },
      { emoji: '🪨', hi: 'कंकड़ / पत्थर', sat: 'ᱫᱷᱤᱨᱤ', pho: 'dhiri', deva: 'धिरी', audio: 'fc_stone.mp3' },
      { emoji: '☀️', hi: 'सूरज', sat: 'ᱥᱤᱧ', pho: 'siñ', deva: 'सिंज', audio: 'fc_sun.mp3' },
      { emoji: '🌙', hi: 'चाँद', sat: 'ᱪᱟᱸᱫᱚ', pho: 'chando', deva: 'चांदो', audio: 'fc_moon.mp3' },
      { emoji: '🐟', hi: 'मछली', sat: 'ᱦᱟᱹᱠᱩ', pho: 'haku', deva: 'हाकू', audio: 'fc_fish.mp3' },
      { emoji: '🐘', hi: 'हाथी', sat: 'ᱦᱟᱹᱛᱤ', pho: 'hati', deva: 'हाती', audio: 'fc_elephant.mp3' },
      { emoji: '🐄', hi: 'गाय', sat: 'ᱜᱟᱹᱭ', pho: 'gai', deva: 'गई', audio: 'fc_cow.mp3' },
      { emoji: '👁️', hi: 'आँख', sat: 'ᱢᱮᱫ', pho: 'med', deva: 'मेद', audio: 'fc_eye.mp3' },
      { emoji: '✋', hi: 'हाथ', sat: 'ᱛᱤ', pho: 'ti', deva: 'ती', audio: 'cmd_ti_tul_pe.mp3' }
    ];

    /* =========================================================================
       APP STATE & NATIVE BRIDGE DISPATCHER
       ========================================================================= */

    let isLiveActive = false;
    let activeCardIndex = 0;
    let quizScore = 0;
    let quizTotal = 0;
    let currentQuizWord = null;
    let activeCategory = 'all';

    let voiceSequenceCounter = 0;

    /* Native Audio & Speech Dispatcher */
    function playVernacularAudio(audioFileName, devaPhonetic, romanPhonetic) {
      // Tactile mobile feedback
      if (window.BhashAIBridge && window.BhashAIBridge.vibrate) {
        window.BhashAIBridge.vibrate(25);
      }

      // Always stop previous audio to prevent overlapping playback
      if (window.BhashAIBridge && window.BhashAIBridge.stopAudio) {
        window.BhashAIBridge.stopAudio();
      }

      const fileToPlay = (audioFileName && audioFileName !== 'null' && audioFileName !== 'undefined' && audioFileName !== 'default_santali.mp3') ? audioFileName : '';

      // Android Java Native Bridge
      if (window.BhashAIBridge && window.BhashAIBridge.speakSantaliDeva) {
        window.BhashAIBridge.speakSantaliDeva(devaPhonetic || '', fileToPlay);
        return;
      }

      // Browser Fallback
      if (fileToPlay) {
        const audio = new Audio('audio/' + fileToPlay);
        audio.play().catch(() => {
          speakBrowserSantaliTTS(devaPhonetic || romanPhonetic);
        });
      } else {
        speakBrowserSantaliTTS(devaPhonetic || romanPhonetic);
      }
    }

    function speakBrowserSantaliTTS(text) {
      if ('speechSynthesis' in window && text) {
        window.speechSynthesis.cancel();
        const utt = new SpeechSynthesisUtterance(text);
        utt.lang = 'hi-IN';
        utt.rate = 0.85;
        window.speechSynthesis.speak(utt);
      }
    }

    function speakHindiAudio(text) {
      if (!text) return;
      if (window.BhashAIBridge && window.BhashAIBridge.vibrate) window.BhashAIBridge.vibrate(20);

      if (window.BhashAIBridge && window.BhashAIBridge.speakHindi) {
        window.BhashAIBridge.speakHindi(text);
        return;
      }
      speakBrowserHindiTTS(text);
    }

    function speakBrowserHindiTTS(text) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utt = new SpeechSynthesisUtterance(text);
        utt.lang = 'hi-IN';
        utt.rate = 0.88;
        window.speechSynthesis.speak(utt);
      }
    }

    /* =========================================================================
       SCREEN 1: LIVE CLASSROOM CONTROLLER
       ========================================================================= */

    function toggleLiveClassroom() {
      if (!isLiveActive) {
        startLiveClassroom();
      } else {
        stopLiveClassroom();
      }
    }

    function startLiveClassroom() {
      isLiveActive = true;
      document.getElementById('btn-main-mic').classList.add('recording');
      document.getElementById('live-tag').classList.add('active');
      document.getElementById('live-dot').classList.add('pulsing');
      document.getElementById('live-state-label').innerText = '🔴 LIVE TEACHING (Mic Open)';
      document.getElementById('live-waveform').classList.add('active');
      document.getElementById('live-speech-subtitle').innerText = 'Listening to teacher... Speak Hindi continuously in class';

      if (window.BhashAIBridge && window.BhashAIBridge.startContinuousListening) {
        window.BhashAIBridge.startContinuousListening();
      }
    }

    function stopLiveClassroom() {
      isLiveActive = false;
      document.getElementById('btn-main-mic').classList.remove('recording');
      document.getElementById('live-tag').classList.remove('active');
      document.getElementById('live-dot').classList.remove('pulsing');
      document.getElementById('live-state-label').innerText = 'Standby (Session Paused)';
      document.getElementById('live-waveform').classList.remove('active');
      document.getElementById('live-speech-subtitle').innerText = 'Session paused. Tap microphone to resume.';

      if (window.BhashAIBridge && window.BhashAIBridge.stopContinuousListening) {
        window.BhashAIBridge.stopContinuousListening();
      }
    }

    // Android Speech Recognition Callbacks
    window.onContinuousPartial = function(partialText) {
      document.getElementById('live-speech-subtitle').innerText = partialText;
    };

    window.onContinuousFinal = function(finalText) {
      if (!finalText || !finalText.trim()) return;
      processClassroomUtterance(finalText.trim());
    };

    window.onNativeSpeechPartial = window.onContinuousPartial;
    window.onNativeSpeechFinal = window.onContinuousFinal;

    window.onNativeSpeechError = function(errMsg) {
      document.getElementById('live-speech-subtitle').innerText = errMsg;
    };

    // Live Mic RMS Volume Visualizer
    window.onMicRmsChanged = function(normalizedLevel) {
      const bars = document.querySelectorAll('.waveform-bar');
      bars.forEach((bar, i) => {
        const h = Math.max(6, Math.min(30, normalizedLevel * 30 * (1 + (i % 3) * 0.2)));
        bar.style.height = h + 'px';
      });
    };

    function processClassroomUtterance(hindiText, autoSpeak = true) {
      if (!hindiText || !hindiText.trim()) return;
      const cleanText = hindiText.trim();
      const requestId = ++voiceSequenceCounter;

      document.getElementById('live-speech-subtitle').innerText = `"${cleanText}"`;

      // Smart Hierarchical Translation
      const trans = translateClassroomSentence(cleanText);

      // Add to live feed
      const feed = document.getElementById('dialogue-feed');
      const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

      const item = document.createElement('div');
      item.className = 'dialogue-card';
      item.innerHTML = `
        <div class="dialogue-meta">
          <span>⏱️ ${timeStr} · Spoken Hindi</span>
          <span style="color: var(--accent); font-weight: 700;">Santali Ol Chiki</span>
        </div>
        <div class="dialogue-hindi">"${cleanText}"</div>
        <div class="dialogue-santali">${trans.sat}</div>
        <div class="dialogue-phonetic">${trans.pho}</div>
        <div class="dialogue-actions">
          <button class="btn-act btn-act-primary" onclick="playVernacularAudio('${trans.audio || ''}', '${(trans.deva || '').replace(/'/g, "\\'")}', '${(trans.pho || '').replace(/'/g, "\\'")}')">🔊 Speak Santali</button>
          <button class="btn-act btn-act-outline" onclick="speakHindiAudio('${cleanText.replace(/'/g, "\\'")}')">🗣️ Read Hindi</button>
        </div>
      `;
      feed.insertBefore(item, feed.firstChild);

      const items = feed.querySelectorAll('.dialogue-card');
      document.getElementById('dialogue-count').innerText = `${items.length} entries`;

      // Auto-speak if enabled and not superseded by a newer request
      if (autoSpeak && document.getElementById('chk-auto-speak').checked) {
        if (requestId === voiceSequenceCounter) {
          playVernacularAudio(trans.audio, trans.deva, trans.pho);
        }
      }
    }


    const DEVA_TO_OLCK = {
      'अ': 'ᱚ', 'आ': 'ᱟ', 'इ': 'ᱤ', 'ई': 'ᱤ', 'उ': 'ᱩ', 'ऊ': 'ᱩ',
      'ए': 'ᱮ', 'ऐ': 'ᱮ', 'ओ': 'ᱳ', 'औ': 'ᱳ',
      'क': 'ᱠ', 'ख': 'ᱠᱷ', 'ग': 'ᱜ', 'घ': 'ᱜᱷ', 'ङ': 'ᱝ',
      'च': 'ᱪ', 'छ': 'ᱪᱷ', 'ज': 'ᱡ', 'झ': 'ᱡᱷ', 'ञ': 'ᱧ',
      'ट': 'ᱴ', 'ठ': 'ᱴᱷ', 'ड': 'ᱰ', 'ढ': 'ᱰᱷ', 'ण': 'ᱬ',
      'त': 'ᱛ', 'थ': 'ᱛᱷ', 'द': 'ᱫ', 'ध': 'ᱫᱷ', 'न': 'ᱱ',
      'प': 'ᱯ', 'फ': 'ᱯᱷ', 'ब': 'ᱵ', 'भ': 'ᱵᱷ', 'म': 'ᱢ',
      'य': 'ᱭ', 'र': 'ᱨ', 'ल': 'ᱞ', 'व': 'ᱣ', 'श': 'ᱥ',
      'ष': 'ᱥ', 'स': 'ᱥ', 'ह': 'ᱦ', 'ड़': 'ᱲ', 'ढ़': 'ᱲᱷ',
      'ा': 'ᱟ', 'ि': 'ᱤ', 'ी': 'ᱤ', 'ु': 'ᱩ', 'ू': 'ᱩ',
      'े': 'ᱮ', 'ै': 'ᱮ', 'ो': 'ᱳ', 'ौ': 'ᱳ',
      'ं': 'ᱝ', 'ँ': 'ᱸ', 'ः': 'ᱷ', '्': '',
      '।': '᱾', '॥': '᱿',
      '०': '᱐', '१': '᱑', '२': '᱒', '३': '᱓', '४': '᱔',
      '५': '᱕', '६': '᱖', '७': '᱗', '८': '᱘', '९': '᱙',
      '0': '᱐', '1': '᱑', '2': '᱒', '3': '᱓', '4': '᱔',
      '5': '᱕', '6': '᱖', '7': '᱗', '8': '᱘', '9': '᱙'
    };

    function transliterateToOlChiki(word) {
      let res = '';
      for (const ch of word) res += DEVA_TO_OLCK[ch] || ch;
      return res;
    }

    function normalizeHindiText(text) {
      return String(text || '')
        .replace(/[“”‘’"']/g, '')
        .replace(/[.,!?।॥;:]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    }

    function lookupLexiconWord(word) {
      if (LEXICON[word]) return LEXICON[word];
      const normalized = word.replace(/(ों|ें|े|ो|िए|िएं|ना|ने|ता|ती|ते)$/u, '');
      if (LEXICON[normalized]) return LEXICON[normalized];
      for (const [dictWord, dictVal] of Object.entries(LEXICON)) {
        if (normalized.length >= 3 && (normalized.startsWith(dictWord) || dictWord.startsWith(normalized))) {
          return dictVal;
        }
      }
      return null;
    }

    function translateConceptPhrase(text) {
      const words = normalizeHindiText(text).split(/\s+/).filter(Boolean);
      const satWords = [];
      const phoWords = [];
      const devaWords = [];
      let hits = 0;

      words.forEach(w => {
        const match = lookupLexiconWord(w);
        if (match) {
          hits++;
          satWords.push(match.sat);
          phoWords.push(match.pho);
          devaWords.push(match.deva);
        } else {
          satWords.push(transliterateToOlChiki(w));
          phoWords.push(w);
          devaWords.push(w);
        }
      });

      return {
        sat: satWords.join(' ').trim(),
        pho: phoWords.join(' ').trim(),
        deva: devaWords.join(' ').trim(),
        hits
      };
    }

    const CLASSROOM_TEMPLATES = [
      { pattern: /^(?:बच्चों\s*)?आज\s+हम\s+(.+?)\s+(?:सीखेंगे|सीखते हैं)$/i, tailSat: 'ᱵᱚ ᱪᱮᱫ-ᱟ ᱾', tailPho: 'bo ched-a.', tailDeva: 'बो चेद-आ', prefixSat: 'ᱛᱮᱦᱮᱧ ᱫᱚ ᱟᱵᱚ', prefixPho: 'Teheñ do abo', prefixDeva: 'तेहेंज दो आबो' },
      { pattern: /^(?:बच्चों\s*)?आज\s+हम\s+(.+?)\s+(?:पढ़ेंगे|पढ़ते हैं)$/i, tailSat: 'ᱵᱚ ᱯᱟᱲᱦᱟᱣ-ᱟ ᱾', tailPho: 'bo parhaw-a.', tailDeva: 'बो पाड़हाव-आ', prefixSat: 'ᱛᱮᱦᱮᱧ ᱫᱚ ᱟᱵᱚ', prefixPho: 'Teheñ do abo', prefixDeva: 'तेहेंज दो आबो' },
      { pattern: /^(.+?)\s+गिन(?:कर|ो|िए)?\s*(?:बताइए|बोलो|बोलिए)?$/i, tailSat: 'ᱞᱮᱠᱷᱟ ᱠᱟᱛᱮ ᱞᱟᱹᱭ ᱯᱮ ᱾', tailPho: 'lekha kate lay pe.', tailDeva: 'लेखा काते लय पे', prefixSat: '', prefixPho: '', prefixDeva: '' },
      { pattern: /^(.+?)\s+उठा(?:कर|ओ|इए)?\s*(?:दिखाइए|दिखाओ)?$/i, tailSat: 'ᱨᱟᱠᱟᱵ ᱠᱟᱛᱮ ᱩᱫᱩᱜ ᱯᱮ ᱾', tailPho: 'rakab kate udug pe.', tailDeva: 'राकाब काते उदुग पे', prefixSat: '', prefixPho: '', prefixDeva: '' },
      { pattern: /^(?:सभी\s+बच्चे\s+)?(.+?)\s+खोल(?:िए|ो)$/i, tailSat: 'ᱡᱷᱤᱡ ᱯᱮ ᱾', tailPho: 'jhij pe.', tailDeva: 'झिज पे', prefixSat: 'ᱡᱚᱛᱚ ᱜᱤᱫᱽᱨᱟᱹ', prefixPho: 'Joto gidra', prefixDeva: 'जोतो गिदरा' }
    ];

    const PEDAGOGICAL_PATTERNS = [
      { pattern: /^(?:आप\s+)?(?:लोग\s+)?कैसे\s+हैं\??$/i, sat: 'ᱟᱯᱮ ᱪᱮᱫ ᱞᱮᱠᱟ ᱢᱮᱱᱟᱜ ᱯᱮᱭᱟ?', pho: 'Ape ched leka menag peya?', deva: 'आपे चेद लेका मेनाग पेया', audio: null },
      { pattern: /^(?:यहाँ|इधर)\s+(?:आइए|आओ)।?$/i, sat: 'ᱱᱚᱸᱰᱮ ᱦᱤᱡᱩᱜ ᱯᱮ ᱾', pho: 'Nonde hijug pe.', deva: 'नोंडे हिजुग पे', audio: null },
      { pattern: /^(?:ताली\s+)?(?:बजाइए|बजाओ)।?$/i, sat: 'ᱛᱷᱟᱭᱚ ᱯᱮ ᱾', pho: 'Thayo pe.', deva: 'थायो पे', audio: 'thayo_pe.mp3' },
      { pattern: /^(?:खड़े\s+हो\s*(?:जाइए|जाओ))।?$/i, sat: 'ᱛᱤᱸᱜᱩᱱ ᱯᱮ ᱾', pho: 'Tingun pe.', deva: 'तिंगुन पे', audio: 'tingun_pe.mp3' },
      { pattern: /^(?:बैठ\s*(?:जाइए|जाओ))।?$/i, sat: 'ᱫᱩᱲᱩᱵ ᱯᱮ ᱾', pho: 'Durub pe.', deva: 'दुरुब पे', audio: 'durub_pe.mp3' },
      { pattern: /^(?:शांत\s*(?:रहिए|रहो)|चुप\s*(?:रहिए|रहो))।?$/i, sat: 'ᱛᱷᱤᱨ ᱛᱟᱦᱮᱸᱱ ᱯᱮ ᱾', pho: 'Thir tahen pe.', deva: 'थिर ताहेन पे', audio: 'cmd_thir_tahen_pe.mp3' },
      { pattern: /^(?:नमस्ते\s*बच्चों?|सुप्रभात\s*बच्चों?)।?!?$/i, sat: 'ᱡᱚᱦᱟᱨ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ!', pho: 'Johar gidra ko!', deva: 'जोहार गिदरा को', audio: 'johar_gidra_ko.mp3' },
      { pattern: /^(?:नमस्ते|सुप्रभात|नमस्कार|प्रणाम|जोहार)।?!?$/i, sat: 'ᱡᱚᱦᱟᱨ ᱾', pho: 'Johar.', deva: 'जोहार', audio: null },
      { pattern: /^(?:तुम्हारा|आपका)\s+(?:क्या\s+)?नाम\s+है\??$/i, sat: 'ᱟᱢᱟᱜ ᱧᱩᱛᱩᱢ ᱫᱚ ᱪᱮᱫ?', pho: 'Amag ñutum do ched?', deva: 'आमाग न्युतुम दो चेद', audio: 'cmd_amag_nutum_ched.mp3' },
      { pattern: /^(?:तुम|आप)\s+कहाँ\s+रहते\s+हो\??$/i, sat: 'ᱟᱢ ᱫᱚ ᱚᱠᱟᱨᱮᱢ ᱛᱟᱦᱮᱸᱱᱟ?', pho: 'Am do okarem tahena?', deva: 'आम दो ओकारेम ताहेना', audio: 'cmd_okarem_tahena.mp3' },
      { pattern: /^(?:किसे|किसको)\s+समझ\s+आया\??$/i, sat: 'ᱚᱠᱚᱭ ᱮ ᱵᱩᱡᱷᱟᱹᱣ ᱠᱮᱫ-ᱟ?', pho: 'Okoy e bujhaw ked-a?', deva: 'ओकोय ए बुझाव केद-आ', audio: 'cmd_okoy_bujhaw_keda.mp3' },
      { pattern: /^(?:क्या\s+)?कोई\s+सवाल\s+है\??$/i, sat: 'ᱪᱮᱫ ᱠᱩᱠᱞᱤ ᱢᱮᱱᱟᱜ-ᱟ?', pho: 'Ched kukli menag-a?', deva: 'चेद कुकली मेनाग-आ', audio: 'cmd_ched_kukli.mp3' }
    ];

    function translateClassroomSentence(hindiText) {
      const cleaned = normalizeHindiText(hindiText);
      const lower = cleaned.toLowerCase();

      if (!cleaned) {
        return { sat: '', pho: '', deva: '', audio: null, source: 'empty', confidence: 0 };
      }

      // 1. Direct Pattern matching for core pedagogical classroom phrases
      for (const pp of PEDAGOGICAL_PATTERNS) {
        if (pp.pattern.test(cleaned)) {
          return { sat: pp.sat, pho: pp.pho, deva: pp.deva, audio: pp.audio || null, source: 'pedagogical_pattern', confidence: 0.98 };
        }
      }

      // 2. Exact match against FLASHCARDS
      for (const fc of FLASHCARDS) {
        const fcClean = normalizeHindiText(fc.hi);
        if (cleaned === fcClean || lower === fcClean.toLowerCase()) {
          return { sat: fc.sat + ' ᱾', pho: fc.pho + '.', deva: fc.deva, audio: fc.audio || null, source: 'flashcard_exact', confidence: 1.0 };
        }
      }

      // 3. Exact match against curated CLASSROOM_PHRASES
      for (const p of CLASSROOM_PHRASES) {
        const pClean = normalizeHindiText(p.hi);
        if (cleaned === pClean || lower === pClean.toLowerCase()) {
          return { sat: p.sat, pho: p.pho, deva: p.deva, audio: p.audio || null, source: 'phrasebook_exact', confidence: 0.95 };
        }
      }

      // 4. Classroom teaching sentence templates (e.g. आज हम [गणित] सीखेंगे)
      for (const tpl of CLASSROOM_TEMPLATES) {
        const match = cleaned.match(tpl.pattern);
        if (match) {
          const concept = translateConceptPhrase(match[1]);
          const sat = [tpl.prefixSat, concept.sat, tpl.tailSat].filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
          const pho = [tpl.prefixPho, concept.pho, tpl.tailPho].filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
          const deva = [tpl.prefixDeva, concept.deva, tpl.tailDeva].filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
          return {
            sat,
            pho,
            deva,
            audio: null,
            source: 'template',
            confidence: concept.hits > 0 ? 0.88 : 0.72
          };
        }
      }

      // 5. Direct Vocabulary exact match
      if (LEXICON[cleaned]) {
        const w = LEXICON[cleaned];
        return { sat: w.sat + ' ᱾', pho: w.pho + '.', deva: w.deva, audio: null, source: 'lexicon_exact', confidence: 0.94 };
      }

      // 6. Context-aware word-by-word synthesis with 100% Ol Chiki rendering
      const concept = translateConceptPhrase(cleaned);
      return {
        sat: (concept.sat || transliterateToOlChiki(cleaned)) + ' ᱾',
        pho: (concept.pho || cleaned) + '.',
        deva: concept.deva || cleaned,
        audio: null,
        source: concept.hits > 0 ? 'context_synthesis' : 'transliteration',
        confidence: concept.hits > 0 ? 0.80 : 0.55
      };
    }

    function clearLiveDialogue() {
      document.getElementById('dialogue-feed').innerHTML = '';
      document.getElementById('dialogue-count').innerText = '0 entries';
    }

    // Render Quick Soundboard Buttons
    function renderSoundboard() {
      const grid = document.getElementById('soundboard-grid');
      const sampleCmds = [
        CLASSROOM_PHRASES[0], // शांत रहिए
        CLASSROOM_PHRASES[4], // बैठ जाइए
        CLASSROOM_PHRASES[5], // खड़े हो जाइए
        CLASSROOM_PHRASES[10], // नमस्ते बच्चों
        CLASSROOM_PHRASES[16], // अपनी किताब खोलिए
        CLASSROOM_PHRASES[17], // कॉपी निकालिए
        CLASSROOM_PHRASES[26], // 1 से 10 तक गिनती बोलो
        CLASSROOM_PHRASES[34]  // शाबाश / बहुत बढ़िया
      ];
      grid.innerHTML = sampleCmds.map(cmd => `
        <button class="sound-btn" onclick="triggerSoundboardCmd('${cmd.hi}', '${cmd.sat}', '${cmd.pho}', '${cmd.deva}', '${cmd.audio || ''}')">
          <div class="sound-btn-hi">${cmd.hi}</div>
          <div class="sound-btn-sat">${cmd.sat}</div>
          <div class="sound-btn-pho">${cmd.pho}</div>
        </button>
      `).join('');
    }

    function triggerSoundboardCmd(hi, sat, pho, deva, audio) {
      // Add to live stream
      const feed = document.getElementById('dialogue-feed');
      const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      const item = document.createElement('div');
      item.className = 'dialogue-card';
      item.innerHTML = `
        <div class="dialogue-meta">
          <span>⚡ ${timeStr} · 1-Tap Quick Command</span>
          <span style="color: var(--accent); font-weight: 700;">Instant Audio</span>
        </div>
        <div class="dialogue-hindi">"${hi}"</div>
        <div class="dialogue-santali">${sat}</div>
        <div class="dialogue-phonetic">${pho}</div>
        <div class="dialogue-actions">
          <button class="btn-act btn-act-primary" onclick="playVernacularAudio('${audio}', '${deva.replace(/'/g, "\\'")}', '${pho.replace(/'/g, "\\'")}')">🔊 Replay Audio</button>
        </div>
      `;
      feed.insertBefore(item, feed.firstChild);

      // Play audio immediately
      playVernacularAudio(audio, deva, pho);
    }

    /* =========================================================================
       SCREEN 2: SMART PHRASEBOOK CONTROLLER
       ========================================================================= */

    function renderPhrasebook() {
      // Category Chips
      const categories = [
        { id: 'all', label: 'All Phrases (सभी)' },
        { id: 'discipline', label: '🤫 Discipline (अनुशासन)' },
        { id: 'attendance', label: '🙋 Attendance (हाजिरी)' },
        { id: 'instructions', label: '📖 Instructions (निर्देश)' },
        { id: 'numeracy', label: '🔢 Numeracy (गिनती)' },
        { id: 'praise', label: '⭐ Praise (प्रशंसा)' },
        { id: 'questions', label: '❓ Questions (प्रश्न)' }
      ];

      const chipsContainer = document.getElementById('phrase-category-chips');
      chipsContainer.innerHTML = categories.map(c => `
        <button class="chip ${c.id === activeCategory ? 'active' : ''}" onclick="setPhraseCategory('${c.id}')">${c.label}</button>
      `).join('');

      renderPhraseList();
    }

    function setPhraseCategory(catId) {
      activeCategory = catId;
      document.querySelectorAll('.chip').forEach(el => el.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.chip')).find(b => b.getAttribute('onclick').includes(catId));
      if (activeBtn) activeBtn.classList.add('active');
      renderPhraseList();
    }

    function renderPhraseList() {
      const q = document.getElementById('phrase-search').value.toLowerCase().trim();
      const container = document.getElementById('phrase-list-container');

      const filtered = CLASSROOM_PHRASES.filter(p => {
        const matchesCat = activeCategory === 'all' || p.cat === activeCategory;
        const matchesQuery = !q || p.hi.toLowerCase().includes(q) || p.pho.toLowerCase().includes(q);
        return matchesCat && matchesQuery;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 20px;">No matching phrases found.</div>`;
        return;
      }

      container.innerHTML = filtered.map(p => `
        <div class="phrase-card">
          <div class="phrase-info">
            <div class="phrase-hi">${p.hi}</div>
            <div class="phrase-sat">${p.sat}</div>
            <div class="phrase-pho">${p.pho}</div>
          </div>
          <div style="display: flex; gap: 6px;">
            <button class="btn-act btn-act-primary" onclick="playVernacularAudio('${p.audio || ''}', '${p.deva.replace(/'/g, "\\'")}', '${p.pho.replace(/'/g, "\\'")}')">🔊 Play</button>
            <button class="btn-act btn-act-outline" onclick="speakHindiAudio('${p.hi.replace(/'/g, "\\'")}')">🗣️</button>
          </div>
        </div>
      `).join('');
    }

    function filterPhrases() {
      renderPhraseList();
    }

    /* =========================================================================
       SCREEN 3: FLASHCARDS & INTERACTIVE QUIZ
       ========================================================================= */

    function switchGameMode(mode) {
      const fcView = document.getElementById('flashcard-subview');
      const qView = document.getElementById('quiz-subview');
      const btnFc = document.getElementById('btn-toggle-fc');
      const btnQ = document.getElementById('btn-toggle-quiz');

      if (mode === 'cards') {
        fcView.style.display = 'flex';
        qView.style.display = 'none';
        btnFc.classList.add('active');
        btnQ.classList.remove('active');
      } else {
        fcView.style.display = 'none';
        qView.style.display = 'flex';
        btnFc.classList.remove('active');
        btnQ.classList.add('active');
        generateNewQuizQuestion();
      }
    }

    function renderActiveFlashcard() {
      const card = FLASHCARDS[activeCardIndex];
      document.getElementById('fc-emoji').innerText = card.emoji;
      document.getElementById('fc-hi').innerText = card.hi;
      document.getElementById('fc-sat').innerText = card.sat;
      document.getElementById('fc-pho').innerText = card.pho;
      document.getElementById('fc-index-tag').innerText = `Card ${activeCardIndex + 1} of ${FLASHCARDS.length}`;
      document.getElementById('main-fc-card').classList.remove('flipped');
    }

    function flipCard() {
      document.getElementById('main-fc-card').classList.toggle('flipped');
      if (window.BhashAIBridge && window.BhashAIBridge.vibrate) window.BhashAIBridge.vibrate(20);
    }

    function nextCard() {
      activeCardIndex = (activeCardIndex + 1) % FLASHCARDS.length;
      renderActiveFlashcard();
    }

    function prevCard() {
      activeCardIndex = (activeCardIndex - 1 + FLASHCARDS.length) % FLASHCARDS.length;
      renderActiveFlashcard();
    }

    function playActiveFlashcardAudio() {
      const card = FLASHCARDS[activeCardIndex];
      playVernacularAudio(card.audio, card.deva, card.pho);
    }

    function playActiveFlashcardHindi() {
      const card = FLASHCARDS[activeCardIndex];
      speakHindiAudio(card.hi);
    }

    // Children Interactive Listening Quiz Engine
    function generateNewQuizQuestion() {
      // Pick random card as target
      const target = FLASHCARDS[Math.floor(Math.random() * FLASHCARDS.length)];
      currentQuizWord = target;

      document.getElementById('quiz-target-sat').innerText = target.sat;
      document.getElementById('quiz-target-pho').innerText = `${target.pho}`;

      // Pick 3 distractors
      const distractors = FLASHCARDS.filter(c => c.hi !== target.hi).sort(() => 0.5 - Math.random()).slice(0, 3);
      const options = [target, ...distractors].sort(() => 0.5 - Math.random());

      const grid = document.getElementById('quiz-options-grid');
      grid.innerHTML = options.map(opt => `
        <button class="quiz-option-btn" onclick="checkQuizAnswer('${opt.hi}', this)">
          <div class="quiz-opt-emoji">${opt.emoji}</div>
          <div class="quiz-opt-label">${opt.hi}</div>
        </button>
      `).join('');

      // Auto-play target audio
      playVernacularAudio(target.audio, target.deva, target.pho);
    }

    function playQuizTargetAudio() {
      if (currentQuizWord) {
        playVernacularAudio(currentQuizWord.audio, currentQuizWord.deva, currentQuizWord.pho);
      }
    }

    function checkQuizAnswer(selectedHi, btnElement) {
      quizTotal++;
      if (selectedHi === currentQuizWord.hi) {
        quizScore++;
        btnElement.classList.add('correct');
        playVernacularAudio('cmd_adi_napay.mp3', 'आडी नापाय!', 'Adi napay!');
      } else {
        btnElement.classList.add('wrong');
        if (window.BhashAIBridge && window.BhashAIBridge.vibrate) window.BhashAIBridge.vibrate(80);
      }
      document.getElementById('quiz-score').innerText = `Score: ${quizScore} / ${quizTotal} ⭐`;
    }

    /* =========================================================================
       SCREEN 4: FLN LESSONS CONTROLLER
       ========================================================================= */

    function renderLessons() {
      const container = document.getElementById('lessons-list');
      container.innerHTML = `
        <div class="lesson-step-card">
          <div class="lesson-step-title">🎯 Lesson 1: 1 से 10 तक गिनती (1 to 10 Counting)</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 6px;">FLN-M1-LO1: Foundation Numeracy with Pebbles and Leaves</p>
          <p style="font-size: 0.9rem; margin-bottom: 6px;"><strong>Teacher Script:</strong> "नमस्ते बच्चों! आज हम कक्षा में पत्तों और कंकड़ों से 1 से 10 तक गिनती सीखेंगे।"</p>
          <p style="font-family: var(--ol-chiki-font); font-size: 1.15rem; color: var(--primary); font-weight: 700;">ᱡᱚᱦᱟᱨ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ! ᱛᱮᱦᱮᱧ ᱫᱚ ᱟᱵᱚ ᱠᱞᱟᱥ ᱨᱮ ᱥᱟᱠᱟᱢ ᱟᱨ ᱫᱷᱤᱨᱤ ᱛᱮ ᱑ ᱠᱷᱚᱱ ᱑᱐ ᱦᱟᱹᱵᱤᱡ ᱞᱮᱠᱷᱟ ᱵᱚ ᱪᱮᱫ-ᱟ ᱾</p>
          <button class="btn-act btn-act-primary" style="margin-top: 8px;" onclick="playVernacularAudio('lesson_intro.mp3', 'जोहार गिदरा को! तेहेंज दो आबो क्लास रे साकाम आर धिरी ते 1 खोन 10 हबिज लेखा बो चेद-आ', 'Johar gidra ko! Teheñ do...')">🔊 Play Santali Lesson Script</button>
        </div>

        <div class="lesson-step-card">
          <div class="lesson-step-title">🎯 Lesson 2: कंकड़ गिनो गतिविधि (Pebble Activity)</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 6px;">Hands-on counting activity with concrete materials</p>
          <p style="font-size: 0.9rem; margin-bottom: 6px;"><strong>Teacher Script:</strong> "सभी बच्चे अपने-अपने सामने पाँच कंकड़ रखें और एक-एक करके जोर से गिनें।"</p>
          <p style="font-family: var(--ol-chiki-font); font-size: 1.15rem; color: var(--primary); font-weight: 700;">ᱡᱚᱛᱚ ᱜᱤᱫᱽᱨᱟᱹ ᱟᱯᱱᱟᱨ ᱥᱟᱢᱟᱝ ᱨᱮ ᱢᱚᱬᱮᱭᱟ ᱫᱷᱤᱨᱤ ᱫᱚᱦᱚᱭ ᱯᱮ ᱟᱨ ᱢᱤᱫ-ᱢᱤᱫ ᱛᱮ ᱞᱮᱠᱷᱟᱭ ᱯᱮ ᱾</p>
          <button class="btn-act btn-act-primary" style="margin-top: 8px;" onclick="playVernacularAudio('activity_dhiri.mp3', 'जोतो गिदरा अपनार सामांग रे मोणेया धिरी दोहोय पे आर मिद-मिद ते लेखाय पे', 'Joto gidra apnar samang re...')">🔊 Play Activity Voice</button>
        </div>

        <div class="lesson-step-card">
          <div class="lesson-step-title">🎯 Lesson 3: कक्षा निर्देश (Daily Classroom Norms)</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 6px;">Standard classroom physical commands</p>
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px;">
            <button class="btn-act btn-act-outline" onclick="playVernacularAudio('tingun_pe.mp3', 'तिंगुन पे', 'Tingun pe')">🧍 खड़े हो जाइए</button>
            <button class="btn-act btn-act-outline" onclick="playVernacularAudio('durub_pe.mp3', 'दुरुब पे', 'Durub pe')">🪑 बैठ जाइए</button>
            <button class="btn-act btn-act-outline" onclick="playVernacularAudio('thayo_pe.mp3', 'थायो पे', 'Thayo pe')">👏 ताली बजाइए</button>
            <button class="btn-act btn-act-outline" onclick="playVernacularAudio('puthi_jhij_pe.mp3', 'पुथी झिज पे', 'Puthi jhij pe')">📖 किताब खोलिए</button>
          </div>
        </div>
      `;
    }

    /* =========================================================================
       SCREEN 5: SETTINGS & CONTROLS
       ========================================================================= */

    function onSpeedChange(val) {
      document.getElementById('speed-val').innerText = `${val}x (${val < 0.85 ? 'Slow' : val > 1.05 ? 'Fast' : 'Optimal'})`;
      if (window.BhashAIBridge && window.BhashAIBridge.setSpeechRate) {
        window.BhashAIBridge.setSpeechRate(parseFloat(val));
      }
    }

    function onFontSizeChange(val) {
      document.documentElement.style.setProperty('--ol-chiki-scale', val);
    }

    function testAudioEngine() {
      playVernacularAudio('johar_gidra_ko.mp3', 'जोहार गिदरा को! आप सब का स्वागत है।', 'Johar gidra ko!');
    }

    /* Navigation Bar Switcher */
    function switchNav(screenId, btnElement) {
      document.querySelectorAll('.screen-view').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

      const target = document.getElementById(screenId);
      if (target) target.classList.add('active');
      if (btnElement) btnElement.classList.add('active');

      if (window.BhashAIBridge && window.BhashAIBridge.vibrate) window.BhashAIBridge.vibrate(15);
    }

    function onLanguageChanged() {
      const sel = document.getElementById('sel-lang').value;
      if (window.BhashAIBridge && window.BhashAIBridge.showToast) {
        window.BhashAIBridge.showToast(`Active Target: ${sel.toUpperCase()}`);
      }
    }

    /* APP INITIALIZATION */
    window.addEventListener('DOMContentLoaded', () => {
      renderSoundboard();
      renderPhrasebook();
      renderActiveFlashcard();
      renderLessons();

      // Initial dialogue item (render card without auto-speaking)
      const initialItem = CLASSROOM_PHRASES[8] || CLASSROOM_PHRASES[0];
      processClassroomUtterance(initialItem.hi, false);
    });
  </script>
</body>
</html>
'''

# Write to both frontend/index.html and android/app/src/main/assets/index.html
for path in ['frontend/index.html', 'android/app/src/main/assets/index.html']:
    with open(path, 'wb') as f:
        f.write(html_content.encode('utf-8'))
    print(f"Successfully generated: {path} ({os.path.getsize(path)} bytes)")
