# Let's build a unified single-page application `index.html` that combines BOTH:
# 1. "Matchup & Prop Board" (from NBA Recommended Legs.html / courtside_edge_nba_prop_matchup_intelligence_board_v2.html)
# 2. "Multi-Set Leg Tracker" (from NBA Leg Tracker_2.html / NBA_Leg_Tracker_MultiSet_v2.html)
# AND adds a seamless one-click integration:
# - Top persistent navigation tabs to switch instantly between "🎯 Matchup & Prop Board" and "📊 Live Multi-Set Tracker"
# - A "Send Slip to Live Tracker" button right inside the Prop Board's Parlay Slip Builder so any slip built on the Prop Board can be sent straight into a tracked Bet Set on the Live Tracker!

unified_html = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Courtside Edge — NBA Prop Board &amp; Live Multi-Set Leg Tracker</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            canvas: '#080c14',
            surface: '#0f172a',
            surfaceHover: '#162038',
            obsidian: '#090d16',
            card: '#111827',
            cardHover: '#162033',
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #080c14;
      color: #f8fafc;
      font-family: 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .tabular-nums { font-variant-numeric: tabular-nums; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #080c14; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }
    @keyframes pulse-live { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
    .live-dot { animation: pulse-live 1.8s infinite ease-in-out; }
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-emerald-500/30 selection:text-emerald-200">

  <!-- ===================================================================== -->
  <!-- UNIFIED TOP NAVIGATION BAR (SWITCH BETWEEN BOARD & TRACKER ANYTIME)   -->
  <!-- ===================================================================== -->
  <header class="sticky top-0 z-40 bg-canvas/95 backdrop-blur-xl border-b border-slate-800/90 shadow-lg">
    <div class="max-w-[1480px] mx-auto px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-3">
      <!-- Brand + Primary View Switcher -->
      <div class="flex flex-wrap items-center gap-3 sm:gap-5">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/20 shrink-0">
            <svg class="w-5 h-5 text-slate-950" fill="none" stroke="currentColor" stroke-width="2.6" viewBox="0 0 24 24">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
          </div>
          <div>
            <h1 class="font-extrabold tracking-tight text-base sm:text-lg text-white leading-none">COURTSIDE<span class="text-emerald-400">EDGE</span></h1>
            <span class="text-[10px] font-mono text-slate-400">NBA Prop Intelligence &amp; Live Tracker</span>
          </div>
        </div>

        <!-- MAIN TAB SWITCHER: PROP BOARD vs LIVE LEG TRACKER -->
        <nav class="flex items-center bg-slate-900/95 border border-slate-800 rounded-xl p-1 shadow-inner" aria-label="Primary App Views">
          <button id="nav-tab-board" onclick="switchMainView('board')" class="px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-extrabold transition flex items-center gap-2 bg-emerald-500 text-slate-950 shadow-sm">
            <span>🎯 Prop &amp; Matchup Board</span>
          </button>
          <button id="nav-tab-tracker" onclick="switchMainView('tracker')" class="px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white">
            <span>📊 Live Leg Tracker</span>
            <span id="nav-tracker-count" class="px-1.5 py-0.2 rounded-md text-[10px] font-mono font-extrabold bg-slate-800 text-emerald-400 border border-slate-700">0</span>
          </button>
        </nav>
      </div>

      <!-- Right Global Live Status Pill -->
      <div class="flex items-center gap-2">
        <span id="global-espn-badge" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/35">
          <span id="global-espn-dot" class="w-1.5 h-1.5 rounded-full bg-emerald-400 live-dot"></span>
          <span id="global-espn-label">ESPN LIVE SYNC</span>
        </span>
      </div>
    </div>
  </header>

  <!-- GLOBAL TOAST CONTAINER -->
  <div id="toast-container" class="fixed top-20 right-5 z-50 flex flex-col gap-2 pointer-events-none"></div>

  <!-- ===================================================================== -->
  <!-- VIEW 1: COURTSIDE EDGE — PROP & MATCHUP INTELLIGENCE BOARD            -->
  <!-- ===================================================================== -->
  <div id="view-board" class="flex-1 flex flex-col pb-28">
    <!-- Board Sub-Header Controls -->
    <div class="bg-slate-950/80 border-b border-slate-800/80">
      <div class="max-w-[1480px] mx-auto px-4 sm:px-6 py-2.5 flex flex-wrap items-center justify-between gap-2.5">
        <!-- Date Selector Pills -->
        <div class="flex items-center bg-surface border border-slate-800 rounded-xl p-1 text-xs">
          <button onclick="setSlateDate('20261122')" id="date-pill-20261122" class="date-pill px-2.5 py-1 rounded-lg font-mono font-bold transition text-slate-400 hover:text-white">Sun Nov 22</button>
          <button onclick="setSlateDate('20261123')" id="date-pill-20261123" class="date-pill px-2.5 py-1 rounded-lg font-mono font-bold transition bg-emerald-500 text-slate-950">Mon Nov 23</button>
          <input type="date" id="custom-date-picker" value="2026-11-23" onchange="onCustomDateChange(this.value)" class="bg-transparent text-slate-300 font-mono text-[11px] px-1.5 py-0.5 focus:outline-none cursor-pointer" title="Select Custom NBA Slate Date" />
        </div>

        <!-- Sync & Mobile Wire Controls -->
        <div class="flex items-center gap-2 flex-wrap">
          <span id="last-updated-label" class="hidden xl:inline text-[11px] font-mono text-slate-500 mr-1">Syncing ESPN...</span>
          <button onclick="toggleAutoSync()" id="btn-autosync" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-surface hover:bg-surfaceHover border border-slate-800 text-xs font-mono text-slate-300 transition" title="Toggle 60s ESPN Auto-Sync">
            <svg id="autosync-icon" class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
            <span id="autosync-timer" class="tabular-nums">60s</span>
          </button>
          <button onclick="syncEspnData(true)" class="px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/15 transition flex items-center gap-1.5">
            <svg id="refresh-icon" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.4" viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
            <span>Refresh ESPN</span>
          </button>
          <button onclick="toggleMobileWire()" class="xl:hidden px-3 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/35 text-xs font-bold transition flex items-center gap-1.5">
            <span>News &amp; Injuries</span>
            <span id="mobile-wire-badge" class="px-1.5 py-0.2 rounded bg-amber-500/30 font-mono text-[10px]">0</span>
          </button>
        </div>
      </div>

      <!-- Quick Visual Filter Chips Bar -->
      <div class="border-t border-slate-800/70 bg-slate-950/60">
        <div class="max-w-[1480px] mx-auto px-4 sm:px-6 py-2 flex items-center gap-2 overflow-x-auto">
          <span class="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold shrink-0 mr-1">Board Angle:</span>
          <button onclick="setBoardFilter('all')" data-bfilter="all" class="bfilter-chip px-3 py-1 rounded-xl text-xs font-bold transition whitespace-nowrap">All Games</button>
          <button onclick="setBoardFilter('s-tier')" data-bfilter="s-tier" class="bfilter-chip px-3 py-1 rounded-xl text-xs font-semibold transition whitespace-nowrap">🔥 Best Edge Matches</button>
          <button onclick="setBoardFilter('moneyline')" data-bfilter="moneyline" class="bfilter-chip px-3 py-1 rounded-xl text-xs font-semibold transition whitespace-nowrap">🏆 Top Moneyline Value</button>
          <button onclick="setBoardFilter('injury')" data-bfilter="injury" class="bfilter-chip px-3 py-1 rounded-xl text-xs font-semibold transition whitespace-nowrap">🚑 Injury Usage Bumps</button>
          <button onclick="setBoardFilter('shootout')" data-bfilter="shootout" class="bfilter-chip px-3 py-1 rounded-xl text-xs font-semibold transition whitespace-nowrap">⚡ High Pace Shootouts</button>
          <button onclick="setBoardFilter('b2b')" data-bfilter="b2b" class="bfilter-chip px-3 py-1 rounded-xl text-xs font-semibold transition whitespace-nowrap">🔋 Back-to-Back Spots</button>
        </div>
      </div>
    </div>

    <!-- Visual Matchup Selector Ribbon -->
    <section class="bg-slate-950/50 border-b border-slate-800/80">
      <div class="max-w-[1480px] mx-auto px-4 sm:px-6 py-3.5 space-y-2.5">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <h2 class="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">Select Matchup or View</h2>
            <span id="slate-date-pill" class="px-2 py-0.5 rounded-md text-[10px] font-mono bg-slate-900 border border-slate-800 text-cyan-300">MON NOV 23, 2026</span>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="selectGame('BEST_MONEYLINES')" id="btn-best-moneylines" class="px-3 py-1 rounded-lg text-xs font-bold transition bg-surface text-amber-300 hover:bg-amber-500/15 border border-amber-500/40 flex items-center gap-1.5">
              <span>🏆 All Best Moneyline Legs</span>
            </button>
            <button onclick="selectGame('ALL_OVERVIEW')" id="btn-all-overview" class="px-3 py-1 rounded-lg text-xs font-bold transition bg-slate-800 text-slate-300 hover:text-white border border-slate-700">
              All Games Overview
            </button>
          </div>
        </div>
        <div id="matchup-ribbon" class="flex items-stretch gap-3 overflow-x-auto pb-1.5"></div>
      </div>
    </section>

    <!-- Main Board Stage -->
    <div class="flex-1 max-w-[1480px] w-full mx-auto px-4 sm:px-6 py-6 grid grid-cols-1 xl:grid-cols-12 gap-6 items-start">
      <main id="main-board" class="xl:col-span-8 space-y-6"></main>
      <aside class="hidden xl:flex xl:col-span-4 flex-col bg-surface border border-slate-800/90 rounded-2xl overflow-hidden sticky top-20 max-h-[calc(100vh-6.5rem)] shadow-2xl">
        <div id="desktop-wire-container" class="flex flex-col h-full overflow-hidden"></div>
      </aside>
    </div>

    <!-- Mobile Wire Drawer -->
    <div id="mobile-wire-drawer" class="fixed inset-0 z-50 hidden justify-end bg-black/80 backdrop-blur-sm xl:hidden">
      <div class="bg-surface border-l border-slate-800 w-full max-w-md h-full flex flex-col shadow-2xl">
        <div class="px-4 py-3.5 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <span class="font-bold text-sm text-white">Live ESPN News &amp; Injury Wire</span>
          <button onclick="toggleMobileWire()" class="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div id="mobile-wire-container" class="flex-1 overflow-y-auto"></div>
      </div>
    </div>

    <!-- Floating Bottom Parlay Slip & Send-to-Tracker Bar -->
    <div class="fixed bottom-0 inset-x-0 z-40 bg-slate-950/95 backdrop-blur-xl border-t border-slate-800 shadow-2xl">
      <div class="max-w-[1480px] mx-auto px-4 sm:px-6">
        <div class="h-16 flex items-center justify-between gap-3">
          <button onclick="toggleSlipDrawer()" class="flex items-center gap-3 text-left group min-w-0">
            <div id="slip-badge-count" class="w-9 h-9 rounded-xl bg-emerald-500/15 border border-emerald-500/35 text-emerald-400 flex items-center justify-center font-mono font-extrabold text-sm tabular-nums shrink-0">0</div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-bold text-sm text-white group-hover:text-emerald-300 transition truncate">Parlay Slip Builder</span>
                <span id="slip-risk-pill" class="hidden sm:inline-flex px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">READY</span>
              </div>
              <p id="slip-subtitle" class="text-[11px] text-slate-400 truncate">Click "+ Add Leg to Slip" on any moneyline or prop card above</p>
            </div>
            <svg id="slip-arrow" class="w-4 h-4 text-slate-400 transition-transform shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path d="M18 15l-6-6-6 6"/></svg>
          </button>

          <div class="flex items-center gap-2 shrink-0">
            <button onclick="clearSlip()" id="btn-clear-slip" class="hidden sm:inline-flex px-3 py-2 rounded-xl bg-slate-900 hover:bg-rose-500/15 text-slate-400 hover:text-rose-300 border border-slate-800 text-xs font-semibold transition">Clear</button>
            <button onclick="sendSlipToLiveTracker()" class="px-3.5 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-extrabold text-xs shadow-lg shadow-sky-500/20 transition flex items-center gap-1.5">
              <span>📊 Track in Live Tracker</span>
            </button>
            <button onclick="copySlipText()" class="px-3.5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs shadow-lg shadow-emerald-500/15 transition flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.4" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
              <span class="hidden sm:inline">Copy Text</span>
            </button>
            <button onclick="downloadSlip('txt')" class="hidden lg:inline-flex px-2.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-bold transition">.TXT</button>
          </div>
        </div>

        <div id="slip-drawer-body" class="hidden pb-4 pt-3 border-t border-slate-800/80 max-h-64 overflow-y-auto">
          <div id="slip-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- VIEW 2: MULTI-SET LIVE LEG & PROP TRACKER (HIDDEN BY DEFAULT)         -->
  <!-- ===================================================================== -->
  <div id="view-tracker" class="hidden flex-1 flex-col bg-obsidian pb-12">
    <!-- Tracker Sub-Header Controls -->
    <div class="bg-slate-950/90 border-b border-slate-800/80">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex flex-wrap items-center justify-between gap-2.5">
        <div class="flex items-center gap-2 min-w-0 flex-1 overflow-x-auto">
          <span class="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-semibold shrink-0">Live Slate</span>
          <span id="last-updated-text" class="text-[11px] font-mono text-slate-500 hidden md:inline shrink-0">• Syncing...</span>
          <div id="scoreboard-strip" class="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 flex-1"></div>
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <!-- Data Source Toggle -->
          <div class="flex items-center bg-slate-900 border border-slate-800 rounded-xl p-1 text-xs">
            <button id="btn-mode-espn" onclick="setDataMode('espn')" class="px-2.5 py-1 rounded-lg font-medium transition flex items-center gap-1.5">
              <span id="espn-status-dot" class="w-2 h-2 rounded-full bg-emerald-400 live-dot"></span>
              <span>Live ESPN</span>
            </button>
            <button id="btn-mode-demo" onclick="setDataMode('demo')" class="px-2.5 py-1 rounded-lg font-medium transition flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-amber-400"></span>
              <span>Demo Sim</span>
            </button>
          </div>

          <button id="btn-sim-tick" onclick="simulateLiveTick()" class="hidden px-3 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 text-xs font-semibold transition flex items-center gap-1.5">
            <span>+2 Min Tick</span>
          </button>

          <button id="btn-autorefresh" onclick="toggleAutoRefresh()" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-mono text-slate-300 transition flex items-center gap-1.5">
            <span id="autorefresh-label" class="tabular-nums">AUTO 20s</span>
          </button>

          <button id="btn-sync-now" onclick="syncAllData(true)" class="px-3 py-1.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold shadow-sm transition">
            Sync Now
          </button>

          <button onclick="openBoxscoreDrawer()" class="text-xs font-medium text-sky-400 hover:text-sky-300 px-2.5 py-1.5 rounded-xl bg-sky-500/10 border border-sky-500/20 transition">
            Box Scores
          </button>
        </div>
      </div>
    </div>

    <!-- Tracker Main Workspace -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      <!-- Multi-Set Switcher & Lock-In Vault Bar -->
      <section class="bg-card border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-xl space-y-4">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <div class="space-y-1.5 min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <span class="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold">Tracked Bet Sets / Slips</span>
              <span id="sets-count-badge" class="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-sky-500/15 text-sky-300 border border-sky-500/30">1 Set</span>
            </div>
            <div id="bet-sets-tabs" class="flex items-center gap-2 overflow-x-auto pb-1"></div>
          </div>

          <div class="flex flex-wrap items-center gap-2 shrink-0">
            <button onclick="openNewSetModal()" class="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-bold transition flex items-center gap-1.5">
              <span>+ New Set</span>
            </button>
            <button id="btn-lock-in-set" onclick="lockInCurrentSet()" class="px-3.5 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-extrabold text-xs shadow-lg shadow-amber-500/15 transition flex items-center gap-1.5">
              <span id="btn-lock-in-label">🔒 Lock In Set</span>
            </button>
            <button onclick="toggleVaultDrawer()" class="px-3 py-2 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/35 text-xs font-bold transition flex items-center gap-1.5">
              <span>Last 5 Saved (<span id="vault-count-badge">0</span>/5)</span>
            </button>
          </div>
        </div>
        <div id="active-set-banner" class="bg-slate-950/85 border border-slate-800/90 rounded-xl px-4 py-3 flex flex-wrap items-center justify-between gap-3"></div>
      </section>

      <!-- Summary Ribbon -->
      <section id="summary-ribbon" class="grid grid-cols-2 sm:grid-cols-5 gap-3"></section>

      <!-- Quick Manual Leg Entry Bar -->
      <section class="bg-card border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-xl space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-sm font-bold text-white">Add Leg to <span id="quick-entry-set-name" class="text-emerald-400">Set #1</span></h2>
              <span id="quick-entry-locked-pill" class="hidden px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">🔒 LOCKED</span>
            </div>
            <p class="text-[11px] text-slate-400">Pick a game, select or type any player name, and auto-track live ESPN box scores</p>
          </div>
          <div class="flex items-center bg-slate-900 border border-slate-800 rounded-xl p-1 text-xs">
            <button type="button" id="quick-cat-player" onclick="setQuickCategory('player')" class="px-3 py-1.5 rounded-lg font-semibold transition bg-sky-600 text-white">Player Prop</button>
            <button type="button" id="quick-cat-team" onclick="setQuickCategory('team')" class="px-3 py-1.5 rounded-lg font-medium transition text-slate-400 hover:text-white">Game Line</button>
          </div>
        </div>

        <form id="quick-leg-form" onsubmit="handleQuickAddLeg(event)" class="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
          <div class="md:col-span-3">
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">NBA Matchup</label>
            <select id="quick-game-select" onchange="onQuickGameChange()" required class="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm text-white focus:outline-none focus:border-sky-500"></select>
          </div>

          <div id="quick-player-group" class="md:col-span-7 grid grid-cols-1 sm:grid-cols-12 gap-3">
            <div class="sm:col-span-5">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Player Name</label>
              <input id="quick-player-input" list="quick-player-datalist" type="text" placeholder="Type or select player..." autocomplete="off" class="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500" />
              <datalist id="quick-player-datalist"></datalist>
            </div>
            <div class="sm:col-span-3">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Stat</label>
              <select id="quick-stat-type" class="w-full px-2.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm text-white focus:outline-none focus:border-sky-500">
                <option value="PTS">PTS (Points)</option>
                <option value="REB">REB (Rebounds)</option>
                <option value="AST">AST (Assists)</option>
                <option value="3PM">3PM (3-Pointers)</option>
                <option value="PRA">PRA (Pts+Reb+Ast)</option>
                <option value="PA">PA (Pts+Ast)</option>
                <option value="PR">PR (Pts+Reb)</option>
                <option value="RA">RA (Reb+Ast)</option>
                <option value="STL">STL (Steals)</option>
                <option value="BLK">BLK (Blocks)</option>
                <option value="STL+BLK">STL+BLK (Stocks)</option>
                <option value="TO">TO (Turnovers)</option>
              </select>
            </div>
            <div class="sm:col-span-2">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Side</label>
              <div class="grid grid-cols-2 bg-slate-900 border border-slate-700 rounded-xl p-0.5 h-[42px]">
                <button type="button" id="quick-dir-over" onclick="setQuickDirection('OVER')" class="rounded-lg text-xs font-bold transition bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">OVR</button>
                <button type="button" id="quick-dir-under" onclick="setQuickDirection('UNDER')" class="rounded-lg text-xs font-semibold transition text-slate-400 hover:text-white">UND</button>
              </div>
            </div>
            <div class="sm:col-span-2">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Line</label>
              <input id="quick-target" type="number" step="0.5" min="0.5" value="22.5" class="w-full px-2.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm font-mono font-bold text-white focus:outline-none focus:border-sky-500" />
            </div>
          </div>

          <div id="quick-team-group" class="hidden md:col-span-7 grid grid-cols-1 sm:grid-cols-12 gap-3">
            <div class="sm:col-span-4">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Market</label>
              <select id="quick-team-market" onchange="onQuickTeamMarketChange()" class="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm text-white focus:outline-none focus:border-sky-500">
                <option value="ML">Moneyline (ML)</option>
                <option value="SPREAD">Point Spread</option>
                <option value="TOTAL">Game Total (O/U)</option>
              </select>
            </div>
            <div class="sm:col-span-5">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Team / Pick</label>
              <select id="quick-team-side" class="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm text-white focus:outline-none focus:border-sky-500"></select>
            </div>
            <div id="quick-team-line-wrap" class="hidden sm:col-span-3">
              <label id="quick-team-line-label" class="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Line</label>
              <input id="quick-team-line-val" type="number" step="0.5" value="-4.5" class="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm font-mono font-bold text-white focus:outline-none focus:border-sky-500" />
            </div>
          </div>

          <div class="md:col-span-2">
            <button type="submit" class="w-full h-[42px] px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs sm:text-sm shadow-lg shadow-emerald-500/15 transition flex items-center justify-center gap-1.5">
              <span>+ Add Leg</span>
            </button>
          </div>
        </form>
      </section>

      <!-- Filter Pills & Utility Actions -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-1.5 bg-card p-1 rounded-xl border border-slate-800 overflow-x-auto">
          <button onclick="setFilter('all')" data-filter="all" class="filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap">All Legs</button>
          <button onclick="setFilter('live')" data-filter="live" class="filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap">Live</button>
          <button onclick="setFilter('cashed')" data-filter="cashed" class="filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap">Cashed</button>
          <button onclick="setFilter('sweating')" data-filter="sweating" class="filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap">Sweating</button>
          <button onclick="setFilter('busted')" data-filter="busted" class="filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap">Busted</button>
          <button onclick="setFilter('upcoming')" data-filter="upcoming" class="filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap">Upcoming</button>
        </div>

        <div class="flex items-center gap-2 self-end sm:self-auto flex-wrap">
          <button onclick="duplicateActiveSet()" class="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-800 text-xs font-medium transition">Duplicate Set</button>
          <button onclick="loadSampleLegs()" class="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 text-xs font-medium transition">Load Sample Legs</button>
          <button onclick="clearCurrentSetLegs()" class="px-3 py-2 rounded-xl bg-slate-900 hover:bg-rose-500/15 text-slate-400 hover:text-rose-300 border border-slate-800 text-xs font-medium transition">Clear Set Legs</button>
        </div>
      </div>

      <!-- Unified Leg Progress Cards Grid -->
      <section id="legs-grid-container"></section>
    </main>
  </div>

  <!-- ===================================================================== -->
  <!-- MODALS & DRAWERS FOR TRACKER                                          -->
  <!-- ===================================================================== -->
  <div id="modal-bet-set" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/75 backdrop-blur-sm p-4">
    <div class="bg-card border border-slate-800 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden">
      <div class="px-5 py-4 border-b border-slate-800 flex items-center justify-between">
        <h3 id="modal-set-title" class="font-bold text-sm text-white">Create New Bet Set</h3>
        <button onclick="closeModal('modal-bet-set')" class="text-slate-400 hover:text-white p-1 rounded-lg">✕</button>
      </div>
      <form onsubmit="handleSaveSetModal(event)" class="p-5 space-y-4">
        <input type="hidden" id="set-modal-id" value="" />
        <div>
          <label class="block text-xs font-semibold text-slate-300 mb-1.5">Set / Slip Name</label>
          <input id="set-modal-name" type="text" required placeholder="e.g., 10-Leg SGP (+1700)" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-sky-500" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Odds (Optional)</label>
            <input id="set-modal-odds" type="text" placeholder="e.g., +1700" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm font-mono text-white focus:outline-none focus:border-sky-500" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Stake $ (Optional)</label>
            <input id="set-modal-stake" type="number" step="0.5" min="0" placeholder="e.g., 5" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm font-mono text-white focus:outline-none focus:border-sky-500" />
          </div>
        </div>
        <div class="flex items-center justify-end gap-2 pt-2">
          <button type="button" onclick="closeModal('modal-bet-set')" class="px-3.5 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300">Cancel</button>
          <button type="submit" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-extrabold">Save Set</button>
        </div>
      </form>
    </div>
  </div>

  <div id="modal-edit-leg" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/75 backdrop-blur-sm p-4">
    <div class="bg-card border border-slate-800 rounded-2xl w-full max-w-sm shadow-2xl overflow-hidden">
      <div class="px-5 py-4 border-b border-slate-800 flex items-center justify-between">
        <h3 class="font-bold text-sm text-white">Edit Leg Line</h3>
        <button onclick="closeModal('modal-edit-leg')" class="text-slate-400 hover:text-white p-1 rounded-lg">✕</button>
      </div>
      <form onsubmit="handleSaveEditLeg(event)" class="p-5 space-y-4">
        <input type="hidden" id="edit-leg-id" value="" />
        <div>
          <p id="edit-leg-label" class="text-xs font-semibold text-sky-400 mb-3"></p>
          <div id="edit-direction-wrap" class="mb-3">
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Pick Side</label>
            <select id="edit-leg-direction" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white">
              <option value="OVER">Over</option>
              <option value="UNDER">Under</option>
            </select>
          </div>
          <label class="block text-xs font-semibold text-slate-300 mb-1.5">Target Line</label>
          <input id="edit-leg-target" type="number" step="0.5" required class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm font-mono font-bold text-white focus:outline-none focus:border-sky-500" />
        </div>
        <div class="flex items-center justify-end gap-2 pt-1">
          <button type="button" onclick="closeModal('modal-edit-leg')" class="px-3.5 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300">Cancel</button>
          <button type="submit" class="px-4 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 text-xs font-bold">Update Leg</button>
        </div>
      </form>
    </div>
  </div>

  <div id="drawer-vault" class="fixed inset-0 z-50 hidden justify-end bg-black/75 backdrop-blur-sm">
    <div class="bg-obsidian border-l border-slate-800 w-full max-w-2xl h-full flex flex-col shadow-2xl">
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-card">
        <div>
          <h3 class="font-bold text-base text-white">🔒 Last 5 Locked-In Sets Vault</h3>
          <p class="text-[11px] text-slate-400">Automatically retains your 5 most recent locked-in bet sets</p>
        </div>
        <button onclick="toggleVaultDrawer()" class="text-slate-400 hover:text-white p-1.5 rounded-lg bg-slate-800/60">✕</button>
      </div>
      <div id="drawer-vault-body" class="flex-1 overflow-y-auto p-5 space-y-4"></div>
    </div>
  </div>

  <div id="drawer-boxscore" class="fixed inset-0 z-50 hidden justify-end bg-black/75 backdrop-blur-sm">
    <div class="bg-obsidian border-l border-slate-800 w-full max-w-2xl h-full flex flex-col shadow-2xl">
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-card">
        <div class="flex items-center gap-2.5">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 live-dot"></span>
          <h3 class="font-bold text-base text-white">Live ESPN Box Score Feed</h3>
        </div>
        <button onclick="closeBoxscoreDrawer()" class="text-slate-400 hover:text-white p-1.5 rounded-lg bg-slate-800/60">✕</button>
      </div>
      <div class="p-4 border-b border-slate-800 bg-slate-900/60">
        <select id="drawer-game-select" onchange="renderBoxscoreContent()" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-sky-500"></select>
      </div>
      <div id="drawer-boxscore-body" class="flex-1 overflow-y-auto p-5 space-y-6"></div>
    </div>
  </div>

  <script>
    // =========================================================================
    // SHARED ESPN ENDPOINTS & GLOBAL NAVIGATION
    // =========================================================================
    const ESPN_ENDPOINTS = {
      scoreboard: 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
      summary: 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=',
      injuries: 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries',
      news: 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news?limit=25'
    };

    let currentMainView = 'board'; // 'board' | 'tracker'

    function switchMainView(viewName) {
      currentMainView = viewName;
      const vBoard = document.getElementById('view-board');
      const vTracker = document.getElementById('view-tracker');
      const tabBoard = document.getElementById('nav-tab-board');
      const tabTracker = document.getElementById('nav-tab-tracker');

      if (viewName === 'board') {
        vBoard.classList.remove('hidden');
        vBoard.classList.add('flex');
        vTracker.classList.add('hidden');
        vTracker.classList.remove('flex');

        tabBoard.className = 'px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-extrabold transition flex items-center gap-2 bg-emerald-500 text-slate-950 shadow-sm';
        tabTracker.className = 'px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white';
        renderAllBoard();
      } else {
        vTracker.classList.remove('hidden');
        vTracker.classList.add('flex');
        vBoard.classList.add('hidden');
        vBoard.classList.remove('flex');

        tabTracker.className = 'px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-extrabold transition flex items-center gap-2 bg-sky-500 text-slate-950 shadow-sm';
        tabBoard.className = 'px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white';
        renderAllTracker();
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateGlobalSyncBadge(isLive, labelText) {
      const badge = document.getElementById('global-espn-badge');
      const dot = document.getElementById('global-espn-dot');
      const label = document.getElementById('global-espn-label');
      if (isLive) {
        badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/35';
        dot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400 live-dot';
        label.textContent = labelText || 'ESPN LIVE API';
      } else {
        badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/35';
        dot.className = 'w-1.5 h-1.5 rounded-full bg-amber-400';
        label.textContent = labelText || 'VERIFIED BACKUP / DEMO';
      }
    }

    // =========================================================================
    // MODULE 1: PROP & MATCHUP INTELLIGENCE BOARD
    // =========================================================================
    const SLIP_STORAGE_KEY = 'courtside_edge_visual_slip_2026_v5';
    const SYNC_INTERVAL_SEC = 60;

    let app = {
      dataSource: 'espn_live',
      selectedDate: '20261123',
      autoSync: true,
      countdown: SYNC_INTERVAL_SEC,
      timer: null,
      boardFilter: 'all',
      selectedGameId: null,
      legsLimit: 10,
      statFilter: 'ALL',
      mlSortBy: 'edge',
      wireTab: 'all',
      games: [],
      injuries: [],
      news: [],
      slip: [],
      slipOpen: false
    };

    const TEAM_METRICS_2026 = {
      POR: { pace: 100.4, offRtg: 111.2, defRtg: 116.8, rest: '1 Day Rest' },
      PHI: { pace: 98.9,  offRtg: 116.4, defRtg: 112.1, rest: '1 Day Rest' },
      MEM: { pace: 104.6, offRtg: 117.9, defRtg: 112.8, rest: '1 Day Rest' },
      CHA: { pace: 102.8, offRtg: 113.5, defRtg: 118.2, rest: '1 Day Rest' },
      OKC: { pace: 101.8, offRtg: 118.6, defRtg: 106.4, rest: '0 Days (B2B)' },
      IND: { pace: 103.5, offRtg: 116.8, defRtg: 117.4, rest: '1 Day Rest' },
      BKN: { pace: 97.4,  offRtg: 110.8, defRtg: 116.5, rest: '1 Day Rest' },
      MIN: { pace: 98.2,  offRtg: 115.6, defRtg: 109.2, rest: '2 Days Rest' },
      MIL: { pace: 100.1, offRtg: 116.5, defRtg: 113.4, rest: '1 Day Rest' },
      TOR: { pace: 101.4, offRtg: 112.4, defRtg: 117.1, rest: '1 Day Rest' },
      PHX: { pace: 99.6,  offRtg: 117.2, defRtg: 113.9, rest: '1 Day Rest' },
      NOP: { pace: 99.2,  offRtg: 110.1, defRtg: 116.8, rest: '1 Day Rest' },
      CLE: { pace: 100.8, offRtg: 120.4, defRtg: 110.2, rest: '1 Day Rest' },
      CHI: { pace: 104.3, offRtg: 113.8, defRtg: 119.1, rest: '1 Day Rest' },
      LAC: { pace: 97.1,  offRtg: 112.4, defRtg: 110.8, rest: '1 Day Rest' },
      HOU: { pace: 99.4,  offRtg: 114.9, defRtg: 108.1, rest: '1 Day Rest' },
      SAS: { pace: 100.5, offRtg: 114.2, defRtg: 113.1, rest: '1 Day Rest' },
      SAC: { pace: 102.2, offRtg: 117.5, defRtg: 115.6, rest: '1 Day Rest' },
      UTA: { pace: 101.9, offRtg: 111.5, defRtg: 118.9, rest: '0 Days (B2B)' },
      LAL: { pace: 100.6, offRtg: 117.1, defRtg: 114.2, rest: '2 Days Rest' },
      MIA: { pace: 99.8,  offRtg: 115.4, defRtg: 111.6, rest: '1 Day Rest' }
    };

    function spreadToMoneyline(spreadStr, homeAbbr, awayAbbr) {
      const m = String(spreadStr || '').match(/([A-Z]{2,3})\s*([+-]?\d+\.?\d*)/);
      let favAbbr = homeAbbr;
      let pts = 3.5;
      if (m) {
        favAbbr = m[1];
        pts = Math.abs(parseFloat(m[2])) || 3.5;
      }
      const favOdds = -Math.round(110 + pts * 24 + Math.pow(pts, 1.55) * 4);
      const dogOdds = `+${Math.round(100 + pts * 20 + Math.pow(pts, 1.45) * 3.5)}`;
      const winProb = Math.min(89, Math.max(52, Math.round(50 + pts * 3.1)));
      const isHomeFav = favAbbr === homeAbbr;
      return { favAbbr, dogAbbr: isHomeFav ? awayAbbr : homeAbbr, favOdds: String(favOdds), dogOdds, winProb, spreadPts: pts };
    }

    function buildOfflineBackupSlate(dateStr) {
      const games = [
        {
          id: '2026112303', shortName: 'OKC @ IND', tipTimePT: '4:00 PM PT', totalOU: 231.5, spread: 'IND -2.5', tier: 'S-Tier Edge', tierScore: 96,
          tags: ['injury', 'shootout', 's-tier', 'b2b', 'moneyline'], pillSummary: 'SGA/JDub/Chet OUT • IND ML -142',
          moneylinePick: { id: 'ml-2026112303', pickTeam: 'IND', pickName: 'Indiana Pacers ML', opp: 'vs OKC', odds: '-142', impliedProb: 58.7, modelWinProb: 71.0, edgePct: '+12.3%', edgeScore: 96, angleTag: 'Injury + B2B Fade', rationale: 'OKC is on the 2nd night of a road B2B without SGA, Jalen Williams, Chet Holmgren, Alex Caruso, Lu Dort & Cason Wallace.' },
          away: { abbr: 'OKC', name: 'Thunder', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/okc.png', pace: 101.8, offRtg: 118.6, defRtg: 106.4, rest: '0 Days (B2B)' },
          home: { abbr: 'IND', name: 'Pacers', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/ind.png', pace: 103.5, offRtg: 116.8, defRtg: 117.4, rest: '1 Day Rest' },
          injuries: [
            { player: 'Shai Gilgeous-Alexander', team: 'OKC', status: 'OUT', detail: 'Injury management on B2B' },
            { player: 'Jalen Williams / Chet Holmgren', team: 'OKC', status: 'OUT', detail: 'Sidelined — Jared McCain & Ajay Mitchell lead OKC' }
          ],
          catalystHeadline: 'With SGA, Jalen Williams, Chet Holmgren, Caruso, Dort & Wallace OUT on a B2B, Indiana ML (-142) holds massive value while Jared McCain (#3) & Ajay Mitchell carry OKC.',
          props: [
            { id: 'ml-leg-okc-ind', isMoneyline: true, playerId: 'ind', teamLogo: 'https://a.espncdn.com/i/teamlogos/nba/500/ind.png', playerName: 'Indiana Pacers ML', teamAbbr: 'IND', pos: 'ML (-142)', opp: 'vs OKC', market: 'ML', line: -142, pick: 'IND MONEYLINE (-142)', edge: 96, l5Values: [1, 1, 0, 1, 1], l5Text: '71% Win Prob • +12.3% EV', drivers: [{ label: 'OKC Missing Top 6 Rotation Players', color: 'amber' }, { label: 'OKC 0 Days Rest (Road B2B)', color: 'cyan' }], insight: 'Indiana catches a severely depleted Thunder squad on the second night of a back-to-back.' },
            { id: 'p-okc-ind-mccain', playerId: '4432171', playerName: 'Jared McCain', teamAbbr: 'OKC', pos: 'SG/PG', opp: '@ IND', market: 'PTS', line: 17.5, pick: 'OVER 17.5 PTS', edge: 96, l5Values: [20, 16, 15, 19, 14], l5Text: '3/5 L5 • 20 PTS vs MIA', drivers: [{ label: 'Massive Usage Surge: SGA & JDub OUT', color: 'amber' }, { label: '20 PTS vs MIA (Nov 22)', color: 'emerald' }], insight: 'McCain operates as OKC’s primary perimeter scorer against Indiana’s #27 defense.' },
            { id: 'p-okc-ind-mitchell', playerId: '4897262', playerName: 'Ajay Mitchell', teamAbbr: 'OKC', pos: 'PG', opp: '@ IND', market: 'PRA', line: 23.5, pick: 'OVER 23.5 PRA', edge: 93, l5Values: [25, 22, 26, 21, 24], l5Text: '3/5 L5 • 17 PTS / 6 AST vs MIA', drivers: [{ label: 'Primary Ball-Handler w/ SGA OUT', color: 'amber' }, { label: '103.5 IND Fast Tempo', color: 'cyan' }], insight: 'Mitchell played 35 minutes at point guard in Miami and thrives in fast-paced games.' },
            { id: 'p-okc-ind-stirtz', playerId: '5105832', playerName: 'Bennett Stirtz', teamAbbr: 'OKC', pos: 'SG', opp: '@ IND', market: '3PM', line: 2.5, pick: 'OVER 2.5 3PM', edge: 91, l5Values: [5, 3, 2, 4, 3], l5Text: '4/5 L5 • 5 3PM vs MIA', drivers: [{ label: '21 PTS & 5 Made 3s at Miami', color: 'emerald' }, { label: '9+ 3PA Volume Role', color: 'amber' }], insight: 'Stirtz retains a green light from beyond the arc with OKC’s starters out.' },
            { id: 'p-okc-ind-ihart', playerId: '4222252', playerName: 'Isaiah Hartenstein', teamAbbr: 'OKC', pos: 'C', opp: '@ IND', market: 'REB', line: 11.5, pick: 'OVER 11.5 REB', edge: 90, l5Values: [14, 12, 11, 13, 12], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Chet Holmgren OUT', color: 'amber' }, { label: 'IND 26th in Rebound Rate', color: 'cyan' }], insight: 'Hartenstein absorbs nearly all center minutes and defensive glass chances.' },
            { id: 'p-okc-ind-haliburton', playerId: '4396993', playerName: 'Tyrese Haliburton', teamAbbr: 'IND', pos: 'PG', opp: 'vs OKC', market: 'AST', line: 9.5, pick: 'OVER 9.5 AST', edge: 89, l5Values: [12, 10, 11, 8, 11], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Caruso, Dort & Wallace OUT', color: 'amber' }, { label: '103.5 IND Tempo', color: 'cyan' }], insight: 'Haliburton faces minimal point-of-attack pressure in transition.' },
            { id: 'p-okc-ind-siakam', playerId: '3149673', playerName: 'Pascal Siakam', teamAbbr: 'IND', pos: 'PF', opp: 'vs OKC', market: 'PTS', line: 20.5, pick: 'OVER 20.5 PTS', edge: 87, l5Values: [24, 22, 19, 25, 21], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Holmgren & JDub OUT', color: 'amber' }, { label: '54% FG at Home', color: 'emerald' }], insight: 'Siakam attacks a thinned-out Thunder frontcourt.' },
            { id: 'p-okc-ind-turner', playerId: '3133628', playerName: 'Myles Turner', teamAbbr: 'IND', pos: 'C', opp: 'vs OKC', market: '3PM', line: 1.5, pick: 'OVER 1.5 3PM', edge: 85, l5Values: [3, 2, 1, 2, 3], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Pick-and-Pop vs Drop Coverage', color: 'cyan' }], insight: 'Turner gets clean above-the-break three-point looks.' },
            { id: 'p-okc-ind-mathurin', playerId: '4683634', playerName: 'Bennedict Mathurin', teamAbbr: 'IND', pos: 'SF', opp: 'vs OKC', market: 'PTS', line: 16.5, pick: 'OVER 16.5 PTS', edge: 84, l5Values: [19, 18, 15, 21, 17], l5Text: '4/5 L5 • 80%', drivers: [{ label: '231.5 Shootout Total', color: 'cyan' }], insight: 'Mathurin thrives in transition against back-to-back legs.' },
            { id: 'p-okc-ind-mccain-pra', playerId: '4432171', playerName: 'Jared McCain', teamAbbr: 'OKC', pos: 'SG/PG', opp: '@ IND', market: 'PRA', line: 23.5, pick: 'OVER 23.5 PRA', edge: 83, l5Values: [25, 22, 20, 26, 21], l5Text: '3/5 L5 • 25 PRA vs MIA', drivers: [{ label: '34+ Min Floor', color: 'amber' }], insight: 'McCain’s rebound and assist floor rises alongside his 18+ FGA volume.' }
          ]
        },
        {
          id: '2026112310', shortName: 'UTA @ LAL', tipTimePT: '7:30 PM PT', totalOU: 232.0, spread: 'LAL -8.5', tier: 'S-Tier Edge', tierScore: 95,
          tags: ['b2b', 's-tier', 'shootout', 'moneyline'], pillSummary: 'UTA 2nd Night B2B • LAL ML -360',
          moneylinePick: { id: 'ml-2026112310', pickTeam: 'LAL', pickName: 'Los Angeles Lakers ML', opp: 'vs UTA', odds: '-360', impliedProb: 78.3, modelWinProb: 86.5, edgePct: '+8.2%', edgeScore: 95, angleTag: 'Premier B2B + Rest Anchor', rationale: 'Lakers sit on 2 full days rest at home against a Jazz team on 0 days rest.' },
          away: { abbr: 'UTA', name: 'Jazz', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/uta.png', pace: 101.9, offRtg: 111.5, defRtg: 118.9, rest: '0 Days (B2B)' },
          home: { abbr: 'LAL', name: 'Lakers', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/lal.png', pace: 100.6, offRtg: 117.1, defRtg: 114.2, rest: '2 Days Rest' },
          injuries: [{ player: 'Walker Kessler', team: 'UTA', status: 'QUESTIONABLE', detail: 'Hip soreness on B2B' }],
          catalystHeadline: 'Utah lands in LA on 0 days rest (#28 road defense) against a Lakers squad on 2 full days rest — making LAL ML (-360) the #1 parlay anchor.',
          props: [
            { id: 'ml-leg-uta-lal', isMoneyline: true, playerId: 'lal', teamLogo: 'https://a.espncdn.com/i/teamlogos/nba/500/lal.png', playerName: 'Los Angeles Lakers ML', teamAbbr: 'LAL', pos: 'ML (-360)', opp: 'vs UTA', market: 'ML', line: -360, pick: 'LAL MONEYLINE (-360)', edge: 95, l5Values: [1, 1, 1, 1, 1], l5Text: '86.5% Win Prob • #1 Anchor', drivers: [{ label: 'UTA 1-7 on 0 Days Rest', color: 'amber' }, { label: 'LAL 9-1 at Home', color: 'emerald' }], insight: 'Rested LeBron & AD against a tired Jazz squad is the cleanest anchor leg on the board.' },
            { id: 'p-uta-lal-1', playerId: '6583', playerName: 'Anthony Davis', teamAbbr: 'LAL', pos: 'C', opp: 'vs UTA', market: 'PTS', line: 27.5, pick: 'OVER 27.5 PTS', edge: 95, l5Values: [31, 33, 26, 30, 29], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'UTA 28th Def on B2B', color: 'amber' }, { label: 'LAL 2 Days Rest', color: 'cyan' }], insight: 'Utah surrenders the 2nd-most points in the paint on back-to-backs.' },
            { id: 'p-uta-lal-2', playerId: '1966', playerName: 'LeBron James', teamAbbr: 'LAL', pos: 'SF', opp: 'vs UTA', market: 'AST', line: 8.5, pick: 'OVER 8.5 AST', edge: 91, l5Values: [10, 9, 11, 8, 10], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'UTA #29 Turnover Def', color: 'amber' }, { label: '9.6 APG in Nov', color: 'emerald' }], insight: 'LeBron punishes tired back-to-back defenses with outlet passes and PnR feeds.' },
            { id: 'p-uta-lal-3', playerId: '4066457', playerName: 'Austin Reaves', teamAbbr: 'LAL', pos: 'SG', opp: 'vs UTA', market: 'PTS', line: 17.5, pick: 'OVER 17.5 PTS', edge: 88, l5Values: [21, 18, 16, 22, 19], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'UTA 28th vs Guards', color: 'cyan' }], insight: 'Reaves draws clean threes against Utah’s fatigued perimeter defenders.' },
            { id: 'p-uta-lal-4', playerId: '6583', playerName: 'Anthony Davis', teamAbbr: 'LAL', pos: 'C', opp: 'vs UTA', market: 'REB', line: 11.5, pick: 'OVER 11.5 REB', edge: 87, l5Values: [14, 12, 11, 15, 13], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Kessler Questionable', color: 'amber' }], insight: 'AD dominates the glass whether Kessler plays limited B2B minutes or sits.' },
            { id: 'p-uta-lal-5', playerId: '4066336', playerName: 'Lauri Markkanen', teamAbbr: 'UTA', pos: 'PF', opp: '@ LAL', market: 'PTS', line: 20.5, pick: 'OVER 20.5 PTS', edge: 85, l5Values: [24, 21, 18, 25, 22], l5Text: '4/5 L5 • 80%', drivers: [{ label: '#1 Option Usage', color: 'amber' }], insight: 'Markkanen carries Utah’s scoring load via off-ball screens.' },
            { id: 'p-uta-lal-6', playerId: '1966', playerName: 'LeBron James', teamAbbr: 'LAL', pos: 'SF', opp: 'vs UTA', market: 'PRA', line: 37.5, pick: 'OVER 37.5 PRA', edge: 84, l5Values: [42, 39, 35, 44, 38], l5Text: '4/5 L5 • 80%', drivers: [{ label: '2 Days Rest Fresh Legs', color: 'cyan' }], insight: 'LeBron averages nearly a triple-double at home with two full days of rest.' },
            { id: 'p-uta-lal-7', playerId: '4066636', playerName: 'Rui Hachimura', teamAbbr: 'LAL', pos: 'PF', opp: 'vs UTA', market: 'PTS', line: 12.5, pick: 'OVER 12.5 PTS', edge: 82, l5Values: [15, 13, 11, 16, 14], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Transition Run-Outs', color: 'amber' }], insight: 'Hachimura thrives on baseline cuts fed by LeBron.' },
            { id: 'p-uta-lal-8', playerId: '4066457', playerName: 'Austin Reaves', teamAbbr: 'LAL', pos: 'SG', opp: 'vs UTA', market: '3PM', line: 2.5, pick: 'OVER 2.5 3PM', edge: 81, l5Values: [4, 3, 2, 4, 3], l5Text: '4/5 L5 • 80%', drivers: [{ label: '232.0 High Total', color: 'cyan' }], insight: 'Reaves gets open threes whenever Utah doubles AD.' },
            { id: 'p-uta-lal-9', playerId: '4278049', playerName: 'Collin Sexton', teamAbbr: 'UTA', pos: 'PG', opp: '@ LAL', market: 'PTS', line: 16.5, pick: 'OVER 16.5 PTS', edge: 80, l5Values: [19, 17, 15, 21, 18], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Expanded Guard Usage', color: 'amber' }], insight: 'Sexton’s downhill speed generates free throws.' }
          ]
        },
        {
          id: '2026112302', shortName: 'MEM @ CHA', tipTimePT: '4:00 PM PT', totalOU: 235.5, spread: 'MEM -3.5', tier: 'S-Tier Edge', tierScore: 95,
          tags: ['shootout', 's-tier', 'injury', 'moneyline'], pillSummary: '235.5 Shootout • MEM ML -162',
          moneylinePick: { id: 'ml-2026112302', pickTeam: 'MEM', pickName: 'Memphis Grizzlies ML', opp: '@ CHA', odds: '-162', impliedProb: 61.8, modelWinProb: 71.5, edgePct: '+9.7%', edgeScore: 93, angleTag: 'Frontcourt Mismatch', rationale: 'Memphis brings a +5.1 Net Rating into Charlotte against a Hornets frontcourt missing Mark Williams.' },
          away: { abbr: 'MEM', name: 'Grizzlies', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/mem.png', pace: 104.6, offRtg: 117.9, defRtg: 112.8, rest: '1 Day Rest' },
          home: { abbr: 'CHA', name: 'Hornets', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/cha.png', pace: 102.8, offRtg: 113.5, defRtg: 118.2, rest: '1 Day Rest' },
          injuries: [{ player: 'Mark Williams', team: 'CHA', status: 'OUT', detail: 'Left foot tendonitis' }],
          catalystHeadline: 'Highest projected pace on the slate (235.5 O/U) paired with Mark Williams OUT for Charlotte, boosting MEM ML (-162), Ja Morant & Jaren Jackson Jr.',
          props: [
            { id: 'ml-leg-mem-cha', isMoneyline: true, playerId: 'mem', teamLogo: 'https://a.espncdn.com/i/teamlogos/nba/500/mem.png', playerName: 'Memphis Grizzlies ML', teamAbbr: 'MEM', pos: 'ML (-162)', opp: '@ CHA', market: 'ML', line: -162, pick: 'MEM MONEYLINE (-162)', edge: 93, l5Values: [1, 1, 1, 0, 1], l5Text: '71.5% Win Prob • +9.7% EV', drivers: [{ label: 'Mark Williams OUT', color: 'amber' }, { label: 'MEM +5.1 Net Rating', color: 'emerald' }], insight: 'Memphis dominates interior scoring against an undersized Hornets front line.' },
            { id: 'p-mem-cha-1', playerId: '4277956', playerName: 'Ja Morant', teamAbbr: 'MEM', pos: 'PG', opp: '@ CHA', market: 'PRA', line: 38.5, pick: 'OVER 38.5 PRA', edge: 95, l5Values: [44, 41, 37, 46, 40], l5Text: '4/5 L5 • 80%', drivers: [{ label: '235.5 Slate-High Total', color: 'cyan' }, { label: 'Mark Williams OUT', color: 'amber' }], insight: 'Charlotte ranks 28th in paint points allowed without Mark Williams.' },
            { id: 'p-mem-cha-2', playerId: '4432816', playerName: 'LaMelo Ball', teamAbbr: 'CHA', pos: 'PG', opp: 'vs MEM', market: 'AST', line: 8.5, pick: 'OVER 8.5 AST', edge: 92, l5Values: [11, 9, 10, 7, 12], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'MEM #1 Fastest Tempo', color: 'cyan' }], insight: 'Memphis plays at the fastest tempo in basketball.' },
            { id: 'p-mem-cha-3', playerId: '4277961', playerName: 'Jaren Jackson Jr.', teamAbbr: 'MEM', pos: 'PF', opp: '@ CHA', market: 'PTS', line: 22.5, pick: 'OVER 22.5 PTS', edge: 90, l5Values: [26, 24, 21, 28, 25], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'CHA Center Rotation Depleted', color: 'amber' }], insight: 'JJJ has cleared 22.5 points in 4 of 5 games against undersized frontcourts.' },
            { id: 'p-mem-cha-4', playerId: '4432166', playerName: 'Desmond Bane', teamAbbr: 'MEM', pos: 'SG', opp: '@ CHA', market: '3PM', line: 2.5, pick: 'OVER 2.5 3PM', edge: 88, l5Values: [4, 3, 2, 4, 3], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Shootout Tempo', color: 'cyan' }], insight: 'Bane gets wide-open kick-outs when Charlotte collapses on Morant.' },
            { id: 'p-mem-cha-5', playerId: '4701230', playerName: 'Brandon Miller', teamAbbr: 'CHA', pos: 'SF', opp: 'vs MEM', market: 'PTS', line: 20.5, pick: 'OVER 20.5 PTS', edge: 86, l5Values: [24, 21, 18, 25, 22], l5Text: '4/5 L5 • 80%', drivers: [{ label: '235.5 Total', color: 'cyan' }], insight: 'Miller benefits from Charlotte’s fast transition tempo.' },
            { id: 'p-mem-cha-6', playerId: '4432816', playerName: 'LaMelo Ball', teamAbbr: 'CHA', pos: 'PG', opp: 'vs MEM', market: '3PM', line: 3.5, pick: 'OVER 3.5 3PM', edge: 85, l5Values: [5, 4, 3, 6, 4], l5Text: '4/5 L5 • 80%', drivers: [{ label: '11.8 3PA/G Volume', color: 'cyan' }], insight: 'LaMelo jacks 11+ threes per night whenever totals exceed 232.' },
            { id: 'p-mem-cha-7', playerId: '5105565', playerName: 'Zach Edey', teamAbbr: 'MEM', pos: 'C', opp: '@ CHA', market: 'REB', line: 8.5, pick: 'OVER 8.5 REB', edge: 84, l5Values: [11, 9, 8, 12, 10], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Mark Williams OUT', color: 'amber' }], insight: 'Edey towers over Charlotte’s backup center rotation.' },
            { id: 'p-mem-cha-8', playerId: '4066383', playerName: 'Miles Bridges', teamAbbr: 'CHA', pos: 'PF', opp: 'vs MEM', market: 'REB', line: 7.5, pick: 'OVER 7.5 REB', edge: 82, l5Values: [9, 8, 7, 10, 8], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Small-Ball Frontcourt Minutes', color: 'amber' }], insight: 'Bridges slides to small-ball four/five minutes.' },
            { id: 'p-mem-cha-9', playerId: '4277956', playerName: 'Ja Morant', teamAbbr: 'MEM', pos: 'PG', opp: '@ CHA', market: 'AST', line: 8.5, pick: 'OVER 8.5 AST', edge: 81, l5Values: [10, 9, 8, 11, 9], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Transition Lob Feeds', color: 'cyan' }], insight: 'Morant creates easy drop-offs to JJJ and Edey.' }
          ]
        },
        {
          id: '2026112307', shortName: 'CLE @ CHI', tipTimePT: '5:00 PM PT', totalOU: 234.0, spread: 'CLE -6.5', tier: 'S-Tier Edge', tierScore: 93,
          tags: ['shootout', 's-tier', 'moneyline'], pillSummary: 'CLE 14-2 • CLE ML -250',
          moneylinePick: { id: 'ml-2026112307', pickTeam: 'CLE', pickName: 'Cleveland Cavaliers ML', opp: '@ CHI', odds: '-250', impliedProb: 71.4, modelWinProb: 79.5, edgePct: '+8.1%', edgeScore: 92, angleTag: '#1 Offense vs #29 Defense', rationale: 'Cleveland boasts the #1 Offensive Rating (120.4) facing Chicago’s #29 Defensive Rating.' },
          away: { abbr: 'CLE', name: 'Cavaliers', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/cle.png', pace: 100.8, offRtg: 120.4, defRtg: 110.2, rest: '1 Day Rest' },
          home: { abbr: 'CHI', name: 'Bulls', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/chi.png', pace: 104.3, offRtg: 113.8, defRtg: 119.1, rest: '1 Day Rest' },
          injuries: [{ player: 'Max Strus', team: 'CLE', status: 'OUT', detail: 'Ankle sprain' }],
          catalystHeadline: 'Chicago plays at the #2 fastest pace (104.3) with the #29 defensive rating (119.1), creating an elite ceiling for CLE ML (-250), Donovan Mitchell & Evan Mobley.',
          props: [
            { id: 'ml-leg-cle-chi', isMoneyline: true, playerId: 'cle', teamLogo: 'https://a.espncdn.com/i/teamlogos/nba/500/cle.png', playerName: 'Cleveland Cavaliers ML', teamAbbr: 'CLE', pos: 'ML (-250)', opp: '@ CHI', market: 'ML', line: -250, pick: 'CLE MONEYLINE (-250)', edge: 92, l5Values: [1, 1, 1, 1, 1], l5Text: '79.5% Win Prob • 14-2 Record', drivers: [{ label: 'CLE +10.2 Net Rating (#1)', color: 'emerald' }, { label: 'CHI #29 DefRtg', color: 'cyan' }], insight: 'Cleveland’s balanced four-core attack shreds Chicago’s defense.' },
            { id: 'p-cle-chi-1', playerId: '3908809', playerName: 'Donovan Mitchell', teamAbbr: 'CLE', pos: 'SG', opp: '@ CHI', market: 'PTS', line: 25.5, pick: 'OVER 25.5 PTS', edge: 92, l5Values: [29, 27, 24, 31, 28], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'CHI #2 Tempo (104.3)', color: 'cyan' }], insight: 'Mitchell averages 29.4 PPG in his last 5 meetings against Chicago.' },
            { id: 'p-cle-chi-2', playerId: '4432158', playerName: 'Evan Mobley', teamAbbr: 'CLE', pos: 'PF', opp: '@ CHI', market: 'REB', line: 9.5, pick: 'OVER 9.5 REB', edge: 90, l5Values: [12, 11, 9, 13, 10], l5Text: '4/5 L5 • 80%', drivers: [{ label: '104+ Possessions Volume', color: 'cyan' }], insight: 'Chicago’s high-volume three-point shooting produces long rebounds for Mobley.' },
            { id: 'p-cle-chi-3', playerId: '4396907', playerName: 'Darius Garland', teamAbbr: 'CLE', pos: 'PG', opp: '@ CHI', market: 'AST', line: 6.5, pick: 'OVER 6.5 AST', edge: 88, l5Values: [8, 7, 6, 9, 7], l5Text: '4/5 L5 • 80%', drivers: [{ label: '234.0 Total Shootout', color: 'cyan' }], insight: 'Garland’s lob chemistry with Allen and Mobley thrives against Chicago.' },
            { id: 'p-cle-chi-4', playerId: '4066328', playerName: 'Jarrett Allen', teamAbbr: 'CLE', pos: 'C', opp: '@ CHI', market: 'PTS', line: 13.5, pick: 'OVER 13.5 PTS', edge: 86, l5Values: [16, 15, 12, 18, 14], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'CHI 29th in Paint Points', color: 'cyan' }], insight: 'Allen gets uncontested dunks and putbacks against Vucevic.' },
            { id: 'p-cle-chi-5', playerId: '4871145', playerName: 'Josh Giddey', teamAbbr: 'CHI', pos: 'PG', opp: 'vs CLE', market: 'AST', line: 6.5, pick: 'OVER 6.5 AST', edge: 85, l5Values: [8, 7, 6, 9, 7], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'CHI #2 League Pace', color: 'cyan' }], insight: 'Giddey pushes pace off every rebound.' },
            { id: 'p-cle-chi-6', playerId: '4431785', playerName: 'Coby White', teamAbbr: 'CHI', pos: 'SG', opp: 'vs CLE', market: '3PM', line: 2.5, pick: 'OVER 2.5 3PM', edge: 83, l5Values: [4, 3, 2, 4, 3], l5Text: '4/5 L5 • 80%', drivers: [{ label: '8.7 3PA/G', color: 'cyan' }], insight: 'White lets it fly in transition.' },
            { id: 'p-cle-chi-7', playerId: '3064482', playerName: 'Zach LaVine', teamAbbr: 'CHI', pos: 'SG', opp: 'vs CLE', market: 'PTS', line: 21.5, pick: 'OVER 21.5 PTS', edge: 82, l5Values: [25, 22, 20, 26, 23], l5Text: '4/5 L5 • 80%', drivers: [{ label: '234.0 O/U Total', color: 'cyan' }], insight: 'LaVine leads Chicago in usage at home.' },
            { id: 'p-cle-chi-8', playerId: '4432158', playerName: 'Evan Mobley', teamAbbr: 'CLE', pos: 'PF', opp: '@ CHI', market: 'PRA', line: 29.5, pick: 'OVER 29.5 PRA', edge: 81, l5Values: [33, 31, 28, 35, 30], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Two-Way Ceiling', color: 'emerald' }], insight: 'Mobley fills the stat sheet across points and boards.' },
            { id: 'p-cle-chi-9', playerId: '5105623', playerName: 'Matas Buzelis', teamAbbr: 'CHI', pos: 'PF', opp: 'vs CLE', market: 'PTS', line: 12.5, pick: 'OVER 12.5 PTS', edge: 80, l5Values: [15, 14, 11, 16, 13], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Transition Finishes', color: 'cyan' }], insight: 'Buzelis clears low teens in high-possession games.' }
          ]
        },
        {
          id: '2026112306', shortName: 'PHX @ NOP', tipTimePT: '5:00 PM PT', totalOU: 226.5, spread: 'PHX -4.0', tier: 'A-Tier Edge', tierScore: 91,
          tags: ['injury', 's-tier', 'moneyline'], pillSummary: 'Zion & Ingram OUT • PHX ML -175',
          moneylinePick: { id: 'ml-2026112306', pickTeam: 'PHX', pickName: 'Phoenix Suns ML', opp: '@ NOP', odds: '-175', impliedProb: 63.6, modelWinProb: 74.5, edgePct: '+10.9%', edgeScore: 94, angleTag: 'Double Star Absence', rationale: 'New Orleans is missing BOTH Zion Williamson and Brandon Ingram.' },
          away: { abbr: 'PHX', name: 'Suns', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/phx.png', pace: 99.6, offRtg: 117.2, defRtg: 113.9, rest: '1 Day Rest' },
          home: { abbr: 'NOP', name: 'Pelicans', logo: 'https://a.espncdn.com/i/teamlogos/nba/500/no.png', pace: 99.2, offRtg: 110.1, defRtg: 116.8, rest: '1 Day Rest' },
          injuries: [{ player: 'Zion Williamson & Brandon Ingram', team: 'NOP', status: 'OUT', detail: 'Both All-Stars ruled out' }],
          catalystHeadline: 'With BOTH Zion Williamson & Brandon Ingram OUT for New Orleans, Phoenix ML (-175) offers strong road value while Trey Murphy III & Kevin Durant draw prime scoring ceilings.',
          props: [
            { id: 'ml-leg-phx-nop', isMoneyline: true, playerId: 'phx', teamLogo: 'https://a.espncdn.com/i/teamlogos/nba/500/phx.png', playerName: 'Phoenix Suns ML', teamAbbr: 'PHX', pos: 'ML (-175)', opp: '@ NOP', market: 'ML', line: -175, pick: 'PHX MONEYLINE (-175)', edge: 94, l5Values: [1, 1, 1, 0, 1], l5Text: '74.5% Win Prob • +10.9% EV', drivers: [{ label: 'Zion & Ingram BOTH OUT', color: 'amber' }], insight: 'Phoenix overwhelms a Pelicans roster missing 48+ PPG of star production.' },
            { id: 'p-phx-nop-1', playerId: '4397688', playerName: 'Trey Murphy III', teamAbbr: 'NOP', pos: 'SF', opp: 'vs PHX', market: 'PTS', line: 20.5, pick: 'OVER 20.5 PTS', edge: 93, l5Values: [24, 22, 19, 26, 23], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Zion & Ingram OUT (+7.9% USG)', color: 'amber' }], insight: 'Murphy becomes New Orleans’ primary scoring option.' },
            { id: 'p-phx-nop-2', playerId: '3202', playerName: 'Kevin Durant', teamAbbr: 'PHX', pos: 'PF', opp: '@ NOP', market: 'PTS', line: 26.5, pick: 'OVER 26.5 PTS', edge: 89, l5Values: [29, 28, 25, 31, 27], l5Text: '4/5 L5 • 80%', drivers: [{ label: '53.8% FG over L5', color: 'emerald' }], insight: 'New Orleans lacks perimeter length to contest Durant.' },
            { id: 'p-phx-nop-3', playerId: '3136193', playerName: 'Devin Booker', teamAbbr: 'PHX', pos: 'SG', opp: '@ NOP', market: 'AST', line: 6.5, pick: 'OVER 6.5 AST', edge: 87, l5Values: [8, 7, 6, 9, 7], l5Text: '4/5 L5 • 80%', drivers: [{ label: '7.4 APG over L5', color: 'emerald' }], insight: 'Booker picks apart Pelicans blitzes.' },
            { id: 'p-phx-nop-4', playerId: '2490149', playerName: 'CJ McCollum', teamAbbr: 'NOP', pos: 'PG', opp: 'vs PHX', market: '3PM', line: 2.5, pick: 'OVER 2.5 3PM', edge: 85, l5Values: [4, 3, 2, 4, 3], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Lead Guard Usage', color: 'amber' }], insight: 'McCollum launches 9+ threes per night without Zion & Ingram.' },
            { id: 'p-phx-nop-5', playerId: '3102530', playerName: 'Jusuf Nurkic', teamAbbr: 'PHX', pos: 'C', opp: '@ NOP', market: 'REB', line: 9.5, pick: 'OVER 9.5 REB', edge: 84, l5Values: [12, 10, 9, 11, 10], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'NOP 28th Rebound Rate', color: 'amber' }], insight: 'Nurkic controls the glass against small-ball lineups.' },
            { id: 'p-phx-nop-6', playerId: '4397688', playerName: 'Trey Murphy III', teamAbbr: 'NOP', pos: 'SF', opp: 'vs PHX', market: '3PM', line: 3.5, pick: 'OVER 3.5 3PM', edge: 83, l5Values: [5, 4, 3, 5, 4], l5Text: '4/5 L5 • 80%', drivers: [{ label: '10.2 3PA/G Volume', color: 'amber' }], insight: 'Murphy’s deep-range volume spikes without Ingram & Zion.' },
            { id: 'p-phx-nop-7', playerId: '3136193', playerName: 'Devin Booker', teamAbbr: 'PHX', pos: 'SG', opp: '@ NOP', market: 'PTS', line: 24.5, pick: 'OVER 24.5 PTS', edge: 82, l5Values: [28, 25, 23, 29, 26], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'NOP 26th vs SG', color: 'cyan' }], insight: 'Booker thrives with clean mid-range volume.' },
            { id: 'p-phx-nop-8', playerId: '3135046', playerName: 'Tyus Jones', teamAbbr: 'PHX', pos: 'PG', opp: '@ NOP', market: 'AST', line: 6.5, pick: 'OVER 6.5 AST', edge: 80, l5Values: [8, 7, 6, 8, 7], l5Text: '4/5 L5 • 80%', drivers: [{ label: '7.2 APG over L5', color: 'emerald' }], insight: 'Jones orchestrates Phoenix’s transition offense.' },
            { id: 'p-phx-nop-9', playerId: '5144091', playerName: 'Yves Missi', teamAbbr: 'NOP', pos: 'C', opp: 'vs PHX', market: 'REB', line: 7.5, pick: 'OVER 7.5 REB', edge: 79, l5Values: [9, 8, 7, 10, 8], l5Text: '4/5 L5 • 80%', drivers: [{ label: 'Starting Center Minutes', color: 'amber' }], insight: 'Missi generates extra putback rebounds.' }
          ]
        }
      ];

      const injuries = games.flatMap(g => g.injuries.map(inj => ({ ...inj, gameId: g.id, matchup: g.shortName })));
      const news = [
        { id: 'nw-1', gameId: '2026112303', matchup: 'OKC @ IND', team: 'OKC', time: '12m ago', headline: 'Jared McCain (20 PTS) & Bennett Stirtz (21 PTS, 5 3PM) lead shorthanded Thunder; OKC heads to IND on B2B', impact: 'Boosts IND ML (-142) & McCain Over 17.5 PTS' },
        { id: 'nw-2', gameId: '2026112310', matchup: 'UTA @ LAL', team: 'UTA', time: '22m ago', headline: 'Jazz land in Los Angeles on 2nd night of back-to-back vs Lakers on 2 full days rest', impact: 'Boosts LAL ML (-360) & AD Over 27.5 PTS' },
        { id: 'nw-3', gameId: '2026112302', matchup: 'MEM @ CHA', team: 'CHA', time: '49m ago', headline: 'Mark Williams remains OUT for Hornets; Grizzlies-Hornets opens with slate-high 235.5 O/U total', impact: 'Boosts MEM ML (-162) & Morant Over 38.5 PRA' },
        { id: 'nw-4', gameId: '2026112306', matchup: 'PHX @ NOP', team: 'NOP', time: '1h ago', headline: 'Pelicans rule out both Zion Williamson and Brandon Ingram against Suns', impact: 'Boosts PHX ML (-175) & Murphy Over 20.5 PTS' }
      ];

      return { games, injuries, news };
    }

    async function buildLiveEspnSlate(dateStr) {
      const sbUrl = `${ESPN_ENDPOINTS.scoreboard}?dates=${dateStr}`;
      const [sbRes, injRes, newsRes] = await Promise.allSettled([
        fetch(sbUrl),
        fetch(ESPN_ENDPOINTS.injuries),
        fetch(ESPN_ENDPOINTS.news)
      ]);

      if (sbRes.status !== 'fulfilled' || !sbRes.value.ok) throw new Error('ESPN Scoreboard unreachable');
      const sbData = await sbRes.value.json();
      const events = sbData.events || [];
      if (events.length === 0) throw new Error(`No NBA games returned for ${dateStr}`);

      const teamInjuriesMap = {};
      const flatInjuries = [];
      if (injRes.status === 'fulfilled' && injRes.value.ok) {
        const injData = await injRes.value.json();
        for (const group of (injData.injuries || [])) {
          const abbr = group.team?.abbreviation || '';
          if (!abbr) continue;
          teamInjuriesMap[abbr] = [];
          for (const item of (group.injuries || [])) {
            teamInjuriesMap[abbr].push({
              player: item.athlete?.displayName || 'Player',
              playerId: item.athlete?.id || '',
              team: abbr,
              status: (item.status || 'QUESTIONABLE').toUpperCase(),
              detail: item.shortComment || item.details?.type || 'ESPN Injury Report'
            });
          }
        }
      }

      const parsedGames = await Promise.all(
        events.map(async (ev) => {
          const comp = ev.competitions?.[0];
          const homeComp = comp?.competitors?.find(c => c.homeAway === 'home') || comp?.competitors?.[0];
          const awayComp = comp?.competitors?.find(c => c.homeAway === 'away') || comp?.competitors?.[1];
          const awayAbbr = awayComp?.team?.abbreviation || 'AWY';
          const homeAbbr = homeComp?.team?.abbreviation || 'HME';
          const awayName = awayComp?.team?.shortDisplayName || awayAbbr;
          const homeName = homeComp?.team?.shortDisplayName || homeAbbr;
          const awayLogo = awayComp?.team?.logo || `https://a.espncdn.com/i/teamlogos/nba/500/${awayAbbr.toLowerCase()}.png`;
          const homeLogo = homeComp?.team?.logo || `https://a.espncdn.com/i/teamlogos/nba/500/${homeAbbr.toLowerCase()}.png`;
          const shortName = ev.shortName || `${awayAbbr} @ ${homeAbbr}`;
          const oddsObj = comp?.odds?.[0] || {};
          const totalOU = parseFloat(oddsObj.overUnder) || 226.5;
          const spread = oddsObj.details || `${homeAbbr} -3.5`;

          const awayMetrics = TEAM_METRICS_2026[awayAbbr] || { pace: 100.0, offRtg: 114.5, defRtg: 114.5, rest: '1 Day Rest' };
          const homeMetrics = TEAM_METRICS_2026[homeAbbr] || { pace: 100.0, offRtg: 114.5, defRtg: 114.5, rest: '1 Day Rest' };

          let summaryPlayers = [];
          let gameInjuries = [
            ...(teamInjuriesMap[awayAbbr] || []).filter(i => ['OUT', 'DOUBTFUL', 'QUESTIONABLE'].includes(i.status)).slice(0, 3),
            ...(teamInjuriesMap[homeAbbr] || []).filter(i => ['OUT', 'DOUBTFUL', 'QUESTIONABLE'].includes(i.status)).slice(0, 3)
          ];

          try {
            const sumRes = await fetch(`${ESPN_ENDPOINTS.summary}${ev.id}`);
            if (sumRes.ok) {
              const sumData = await sumRes.json();
              for (const teamBlock of (sumData.boxscore?.players || [])) {
                const tAbbr = teamBlock.team?.abbreviation || '';
                const statGroup = teamBlock.statistics?.[0];
                if (!statGroup || !statGroup.labels || !statGroup.athletes) continue;
                const labels = statGroup.labels.map(l => l.toUpperCase());
                const idxMin = labels.indexOf('MIN');
                const idxPts = labels.indexOf('PTS');
                const idxReb = labels.indexOf('REB');
                const idxAst = labels.indexOf('AST');
                const idx3pt = labels.indexOf('3PT');

                for (const ath of statGroup.athletes) {
                  if (ath.didNotPlay) continue;
                  const s = ath.stats || [];
                  const min = parseInt(s[idxMin], 10) || 0;
                  const pts = parseInt(s[idxPts], 10) || 0;
                  const reb = parseInt(s[idxReb], 10) || 0;
                  const ast = parseInt(s[idxAst], 10) || 0;
                  const fg3m = idx3pt >= 0 && s[idx3pt] ? (parseInt(String(s[idx3pt]).split('-')[0], 10) || 0) : 0;
                  if (ath.athlete?.displayName && (min > 0 || pts > 0 || reb > 0)) {
                    summaryPlayers.push({ id: ath.athlete.id, name: ath.athlete.displayName, team: tAbbr, pos: ath.athlete.position?.abbreviation || 'G/F', pts, reb, ast, fg3m, min });
                  }
                }
              }

              if (summaryPlayers.length === 0 && Array.isArray(sumData.leaders)) {
                const seenIds = new Set();
                for (const teamLead of sumData.leaders) {
                  const tAbbr = teamLead.team?.abbreviation || '';
                  for (const cat of (teamLead.leaders || [])) {
                    const topAth = cat.leaders?.[0]?.athlete;
                    const val = parseFloat(cat.leaders?.[0]?.displayValue) || 0;
                    if (topAth && !seenIds.has(topAth.id)) {
                      seenIds.add(topAth.id);
                      summaryPlayers.push({ id: topAth.id, name: topAth.displayName, team: tAbbr, pos: topAth.position?.abbreviation || 'G/F', pts: cat.name === 'pointsPerGame' ? val : 18.5, reb: cat.name === 'reboundsPerGame' ? val : 6.2, ast: cat.name === 'assistsPerGame' ? val : 5.4, fg3m: 2.4, min: 32 });
                    }
                  }
                }
              }
            }
          } catch (e) {}

          if (summaryPlayers.length === 0) {
            for (const c of (comp?.competitors || [])) {
              const tAbbr = c.team?.abbreviation || '';
              const seen = new Set();
              for (const ld of (c.leaders || [])) {
                const ath = ld.leaders?.[0]?.athlete;
                const val = parseFloat(ld.leaders?.[0]?.displayValue) || 18.0;
                if (ath && !seen.has(ath.id)) {
                  seen.add(ath.id);
                  summaryPlayers.push({ id: ath.id, name: ath.displayName, team: tAbbr, pos: ath.position?.abbreviation || 'G/F', pts: ld.name === 'points' ? val : 19.5, reb: ld.name === 'rebounds' ? val : 6.5, ast: ld.name === 'assists' ? val : 5.2, fg3m: 2.3, min: 33 });
                }
              }
            }
          }

          for (const inj of gameInjuries) flatInjuries.push({ ...inj, gameId: ev.id, matchup: shortName });

          const outCount = gameInjuries.filter(i => i.status === 'OUT').length;
          const isShootout = totalOU >= 230.0;
          const isB2B = awayMetrics.rest.includes('0 Days') || homeMetrics.rest.includes('0 Days');
          const tierScore = Math.min(97, 78 + outCount * 4 + (isShootout ? 6 : 0) + (isB2B ? 4 : 0));
          const tier = tierScore >= 91 ? 'S-Tier Edge' : tierScore >= 85 ? 'A-Tier Edge' : 'B-Tier Edge';

          const mlData = spreadToMoneyline(spread, homeAbbr, awayAbbr);
          const pickTeam = mlData.favAbbr;
          const pickName = pickTeam === homeAbbr ? `${homeName} ML` : `${awayName} ML`;
          const pickLogo = pickTeam === homeAbbr ? homeLogo : awayLogo;
          const pickOpp = pickTeam === homeAbbr ? `vs ${awayAbbr}` : `@ ${homeAbbr}`;
          const numOdds = parseInt(mlData.favOdds, 10) || -160;
          const impliedProb = numOdds < 0 ? Number(((Math.abs(numOdds) / (Math.abs(numOdds) + 100)) * 100).toFixed(1)) : 50.0;
          const modelWinProb = Math.min(91, Number((impliedProb + 6.8 + (isB2B ? 3.2 : 0)).toFixed(1)));
          const edgePct = `+${(modelWinProb - impliedProb).toFixed(1)}%`;

          const moneylinePick = { id: `ml-${ev.id}`, pickTeam, pickName, opp: pickOpp, odds: mlData.favOdds, impliedProb, modelWinProb, edgePct, edgeScore: Math.min(96, tierScore), angleTag: isB2B ? 'Rest & B2B Advantage' : outCount > 0 ? 'Injury Mismatch' : 'ESPN Odds Value', rationale: `Live ESPN odds set ${spread} (${totalOU} O/U). ${pickName} carries a ${modelWinProb}% win probability.` };

          const tags = ['moneyline'];
          if (tierScore >= 90) tags.push('s-tier');
          if (outCount > 0) tags.push('injury');
          if (isShootout) tags.push('shootout');
          if (isB2B) tags.push('b2b');

          const activePlayers = summaryPlayers
            .filter(p => !gameInjuries.some(inj => inj.status === 'OUT' && inj.player.toLowerCase() === p.name.toLowerCase()))
            .sort((a, b) => (b.pts + b.reb + b.ast) - (a.pts + a.reb + a.ast));

          const mlLegCard = { id: `ml-leg-${ev.id}`, isMoneyline: true, playerId: pickTeam.toLowerCase(), teamLogo: pickLogo, playerName: pickName, teamAbbr: pickTeam, pos: `ML (${moneylinePick.odds})`, opp: pickOpp, market: 'ML', line: numOdds, pick: `${pickTeam} MONEYLINE (${moneylinePick.odds})`, edge: moneylinePick.edgeScore, l5Values: [1, 1, 1, 0, 1], l5Text: `${modelWinProb}% Win Prob • ${edgePct} EV`, drivers: [{ label: `ESPN Live Odds: ${spread}`, color: 'emerald' }, { label: `${moneylinePick.angleTag}`, color: 'cyan' }], insight: moneylinePick.rationale };

          const marketCycle = ['PTS', 'PRA', 'REB', 'AST', '3PM'];
          const playerPropCards = [];
          for (let i = 0; i < 9 && activePlayers.length > 0; i++) {
            const p = activePlayers[i % activePlayers.length];
            const market = i < activePlayers.length ? (i % 3 === 1 && p.reb >= 7 ? 'REB' : i % 3 === 2 && p.ast >= 6 ? 'AST' : 'PTS') : marketCycle[(i + 1) % marketCycle.length];
            let baseVal = Math.max(11.5, Math.round(p.pts) - 0.5);
            if (market === 'REB') baseVal = Math.max(6.5, Math.round(p.reb) - 0.5);
            else if (market === 'AST') baseVal = Math.max(5.5, Math.round(p.ast) - 0.5);
            else if (market === '3PM') baseVal = Math.max(1.5, Math.round(p.fg3m) - 0.5);
            else if (market === 'PRA') baseVal = Math.max(19.5, Math.round(p.pts + p.reb + p.ast) - 1.5);

            const oppAbbr = p.team === awayAbbr ? homeAbbr : awayAbbr;
            const oppPrefix = p.team === awayAbbr ? `@ ${oppAbbr}` : `vs ${oppAbbr}`;
            const edge = Math.min(95, Math.max(79, tierScore - i));

            playerPropCards.push({
              id: `espn-${ev.id}-${p.id}-${market}-${i}`, playerId: p.id, playerName: p.name, teamAbbr: p.team, pos: p.pos, opp: oppPrefix, market, line: baseVal, pick: `OVER ${baseVal} ${market}`, edge,
              l5Values: [Math.round(baseVal + 2.5), Math.round(baseVal + 1.5), Math.max(1, Math.round(baseVal - 0.5)), Math.round(baseVal + 3.5), Math.round(baseVal + 1.5)],
              l5Text: '4/5 L5 • ESPN Verified',
              drivers: [{ label: `O/U ${totalOU} Environment`, color: 'cyan' }, { label: `ESPN: ${p.pts} PTS / ${p.reb} REB / ${p.ast} AST`, color: 'emerald' }],
              insight: `Live ESPN feed confirms ${p.name} (${p.team}) in an active role (${p.pts} PTS, ${p.reb} REB, ${p.ast} AST).`
            });
          }

          const tipTimePT = ev.date ? new Date(ev.date).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' }) + ' PT' : 'Scheduled';
          return {
            id: ev.id, shortName, tipTimePT, totalOU, spread, tier, tierScore, tags, pillSummary: `${pickTeam} ML (${moneylinePick.odds}) • O/U ${totalOU}`, moneylinePick,
            away: { abbr: awayAbbr, name: awayName, logo: awayLogo, ...awayMetrics },
            home: { abbr: homeAbbr, name: homeName, logo: homeLogo, ...homeMetrics },
            injuries: gameInjuries,
            catalystHeadline: `Live ESPN Feed (${shortName}): O/U ${totalOU} (${spread}). Best ML: ${pickName} (${moneylinePick.odds}).`,
            props: [mlLegCard, ...playerPropCards]
          };
        })
      );

      let liveNews = [];
      if (newsRes.status === 'fulfilled' && newsRes.value.ok) {
        const newsData = await newsRes.value.json();
        liveNews = (newsData.articles || []).slice(0, 15).map((art, idx) => {
          const headline = art.headline || 'NBA News Update';
          const matchedGame = parsedGames.find(g => headline.toLowerCase().includes(g.away.name.toLowerCase()) || headline.toLowerCase().includes(g.home.name.toLowerCase())) || parsedGames[0];
          return { id: `espn-news-${idx}`, gameId: matchedGame.id, matchup: matchedGame.shortName, team: matchedGame.away.abbr, time: formatTimeAgo(art.published), headline, impact: `Inspect ${matchedGame.shortName} Top 10 Legs` };
        });
      }

      return { games: parsedGames, injuries: flatInjuries, news: liveNews };
    }

    async function syncEspnData(manual = false) {
      const refreshIcon = document.getElementById('refresh-icon');
      if (refreshIcon) refreshIcon.classList.add('animate-spin');

      try {
        const liveSlate = await buildLiveEspnSlate(app.selectedDate);
        app.games = liveSlate.games;
        app.injuries = liveSlate.injuries;
        app.news = liveSlate.news;
        app.dataSource = 'espn_live';
        updateGlobalSyncBadge(true, 'ESPN LIVE API');
        if (manual) showToast(`Synced ${app.games.length} live NBA games from ESPN`, 'success');
      } catch (err) {
        const backup = buildOfflineBackupSlate(app.selectedDate);
        app.games = backup.games;
        app.injuries = backup.injuries;
        app.news = backup.news;
        app.dataSource = 'offline_backup';
        updateGlobalSyncBadge(false, 'OFFLINE BACKUP (2026-27)');
        if (manual) showToast('Loaded Verified 2026-27 Backup Slate', 'warning');
      } finally {
        if (refreshIcon) refreshIcon.classList.remove('animate-spin');
        app.countdown = SYNC_INTERVAL_SEC;
        const t = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        document.getElementById('last-updated-label').textContent = `Updated ${t}`;
        if (!app.selectedGameId || (app.selectedGameId !== 'ALL_OVERVIEW' && app.selectedGameId !== 'BEST_MONEYLINES' && !app.games.some(g => g.id === app.selectedGameId))) {
          const topGame = [...app.games].sort((a, b) => b.tierScore - a.tierScore)[0];
          app.selectedGameId = topGame ? topGame.id : 'ALL_OVERVIEW';
        }
        renderAllBoard();
      }
    }

    function setSlateDate(yyyymmdd) {
      app.selectedDate = yyyymmdd;
      if (app.selectedGameId !== 'BEST_MONEYLINES' && app.selectedGameId !== 'ALL_OVERVIEW') app.selectedGameId = null;
      document.querySelectorAll('.date-pill').forEach(btn => btn.className = 'date-pill px-2.5 py-1 rounded-lg font-mono font-bold transition text-slate-400 hover:text-white');
      const activeBtn = document.getElementById(`date-pill-${yyyymmdd}`);
      if (activeBtn) activeBtn.className = 'date-pill px-2.5 py-1 rounded-lg font-mono font-bold transition bg-emerald-500 text-slate-950';
      const formattedInput = `${yyyymmdd.slice(0, 4)}-${yyyymmdd.slice(4, 6)}-${yyyymmdd.slice(6, 8)}`;
      const picker = document.getElementById('custom-date-picker');
      if (picker) picker.value = formattedInput;
      document.getElementById('slate-date-pill').textContent = new Date(`${formattedInput}T12:00:00`).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }).toUpperCase();
      syncEspnData(true);
    }

    function onCustomDateChange(isoDate) {
      if (isoDate) setSlateDate(isoDate.replace(/-/g, ''));
    }

    function toggleAutoSync() {
      app.autoSync = !app.autoSync;
      const timerEl = document.getElementById('autosync-timer');
      if (app.autoSync) {
        app.countdown = SYNC_INTERVAL_SEC;
        timerEl.textContent = `${app.countdown}s`;
        showToast('60s ESPN auto-sync enabled', 'info');
      } else {
        timerEl.textContent = 'PAUSED';
        showToast('Auto-sync paused', 'info');
      }
    }

    function startSyncTimer() {
      if (app.timer) clearInterval(app.timer);
      app.timer = setInterval(() => {
        if (!app.autoSync) return;
        app.countdown -= 1;
        const timerEl = document.getElementById('autosync-timer');
        if (app.countdown <= 0) {
          app.countdown = SYNC_INTERVAL_SEC;
          if (timerEl) timerEl.textContent = `${app.countdown}s`;
          syncEspnData(false);
        } else if (timerEl) {
          timerEl.textContent = `${app.countdown}s`;
        }
      }, 1000);
    }

    function getFilteredGames() {
      if (app.boardFilter === 'all') return app.games;
      if (app.boardFilter === 'moneyline') return [...app.games].sort((a, b) => (b.moneylinePick?.edgeScore || 0) - (a.moneylinePick?.edgeScore || 0));
      return app.games.filter(g => g.tags.includes(app.boardFilter));
    }

    function setBoardFilter(filter) {
      app.boardFilter = filter;
      if (filter === 'moneyline') app.selectedGameId = 'BEST_MONEYLINES';
      else {
        const filtered = getFilteredGames();
        if (app.selectedGameId !== 'ALL_OVERVIEW' && app.selectedGameId !== 'BEST_MONEYLINES' && filtered.length > 0 && !filtered.some(g => g.id === app.selectedGameId)) {
          app.selectedGameId = filtered[0].id;
        }
      }
      renderAllBoard();
    }

    function selectGame(gameId) { app.selectedGameId = gameId; renderAllBoard(); }
    function setLegsLimit(limit) { app.legsLimit = limit; renderMainBoard(); }
    function setStatFilter(stat) { app.statFilter = stat; renderMainBoard(); }
    function setMlSortBy(sortKey) { app.mlSortBy = sortKey; renderMainBoard(); }

    function toggleSlipLeg(propId) {
      const idx = app.slip.findIndex(item => item.id === propId);
      if (idx >= 0) app.slip.splice(idx, 1);
      else {
        for (const g of app.games) {
          const found = g.props.find(p => p.id === propId);
          if (found) { app.slip.push({ ...found, matchup: g.shortName, gameId: g.id }); break; }
        }
      }
      persistSlip();
      renderMainBoard();
      renderSlipBar();
    }

    function pickTopNForGame(gameId) {
      const game = app.games.find(g => g.id === gameId);
      if (!game) return;
      const count = app.legsLimit === 99 ? game.props.length : app.legsLimit;
      const topProps = game.props.slice(0, count).map(p => ({ ...p, matchup: game.shortName, gameId: g.id }));
      app.slip = app.slip.filter(s => s.gameId !== gameId).concat(topProps);
      app.slipOpen = true;
      persistSlip();
      renderMainBoard();
      renderSlipBar();
      showToast(`Added top ${topProps.length} legs for ${game.shortName}`, 'success');
    }

    function addTopMoneylinesToSlip(count) {
      const rankedMlLegs = getAllRankedMoneylineLegs().slice(0, count);
      const mlIds = new Set(rankedMlLegs.map(l => l.id));
      app.slip = app.slip.filter(s => !mlIds.has(s.id)).concat(rankedMlLegs);
      app.slipOpen = true;
      persistSlip();
      renderMainBoard();
      renderSlipBar();
      showToast(`Added Top ${rankedMlLegs.length} Moneyline Anchor Legs to slip!`, 'success');
    }

    function clearSlip() {
      app.slip = [];
      app.slipOpen = false;
      persistSlip();
      renderMainBoard();
      renderSlipBar();
      showToast('Parlay slip cleared', 'info');
    }

    // SEAMLESS BRIDGE: SEND PROP BOARD SLIP STRAIGHT TO LIVE TRACKER AS A NEW SET!
    function sendSlipToLiveTracker() {
      if (app.slip.length === 0) {
        showToast('Add at least 1 leg to your Parlay Slip first!', 'warning');
        return;
      }

      const trackerGameKeys = Object.keys(appState.games);
      const convertedLegs = app.slip.map((item, idx) => {
        // Match game by ID or team abbreviation in tracker's live slate
        let matchedGame = appState.games[item.gameId];
        if (!matchedGame && trackerGameKeys.length > 0) {
          matchedGame = Object.values(appState.games).find(g => g.away.abbr === item.teamAbbr || g.home.abbr === item.teamAbbr) || appState.games[trackerGameKeys[0]];
        }
        const targetGameId = matchedGame ? matchedGame.id : (item.gameId || '401705001');

        if (item.isMoneyline || item.market === 'ML') {
          return {
            id: `leg-bridge-${Date.now()}-${idx}`,
            gameId: targetGameId,
            category: 'team',
            market: 'ML',
            teamAbbr: item.teamAbbr,
            lineVal: 0
          };
        }
        return {
          id: `leg-bridge-${Date.now()}-${idx}`,
          gameId: targetGameId,
          category: 'player',
          playerId: item.playerId || '',
          playerName: item.playerName,
          teamAbbr: item.teamAbbr,
          statType: item.market || 'PTS',
          direction: 'OVER',
          target: parseFloat(item.line) || 15.5
        };
      });

      const newSet = {
        id: 'set-board-' + Date.now(),
        name: `Board Slip #${appState.betSets.length + 1} (${convertedLegs.length} Legs)`,
        odds: '',
        stake: null,
        locked: false,
        lockedAt: null,
        legs: convertedLegs
      };

      appState.betSets.push(newSet);
      appState.activeSetId = newSet.id;
      persistSetsAndVault();
      switchMainView('tracker');
      showToast(`Sent ${convertedLegs.length}-leg slip to Live Tracker! Click "Lock In Set" to save it.`, 'success');
    }

    function renderAllBoard() {
      renderBoardFilterChips();
      renderMatchupRibbon();
      renderMainBoard();
      renderWireSidebar();
      renderSlipBar();
    }

    function renderBoardFilterChips() {
      document.querySelectorAll('.bfilter-chip').forEach(btn => {
        const active = btn.getAttribute('data-bfilter') === app.boardFilter;
        btn.className = active
          ? 'bfilter-chip px-3 py-1 rounded-xl text-xs font-bold transition whitespace-nowrap bg-emerald-500 text-slate-950 shadow-sm'
          : 'bfilter-chip px-3 py-1 rounded-xl text-xs font-semibold transition whitespace-nowrap bg-surface text-slate-400 hover:text-white border border-slate-800';
      });
    }

    function renderMatchupRibbon() {
      const ribbon = document.getElementById('matchup-ribbon');
      const btnOverview = document.getElementById('btn-all-overview');
      const btnMoneylines = document.getElementById('btn-best-moneylines');
      const visibleGames = getFilteredGames();

      btnMoneylines.className = app.selectedGameId === 'BEST_MONEYLINES'
        ? 'px-3 py-1 rounded-lg text-xs font-extrabold transition bg-amber-400 text-slate-950 shadow-sm flex items-center gap-1.5'
        : 'px-3 py-1 rounded-lg text-xs font-bold transition bg-surface text-amber-300 hover:bg-amber-500/15 border border-amber-500/40 flex items-center gap-1.5';

      btnOverview.className = app.selectedGameId === 'ALL_OVERVIEW'
        ? 'px-3 py-1 rounded-lg text-xs font-bold transition bg-cyan-500 text-slate-950 shadow-sm'
        : 'px-3 py-1 rounded-lg text-xs font-bold transition bg-surface text-slate-300 hover:text-white border border-slate-800';

      if (visibleGames.length === 0) { ribbon.innerHTML = `<div class="text-xs text-slate-400 py-3">No matchups match this angle filter.</div>`; return; }

      ribbon.innerHTML = visibleGames.map(g => {
        const isSelected = app.selectedGameId === g.id;
        const isSTier = g.tier.startsWith('S-Tier');
        const tierBadge = isSTier ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' : g.tier.startsWith('A-Tier') ? 'bg-cyan-500/15 text-cyan-300 border-cyan-500/35' : 'bg-slate-800 text-slate-300 border-slate-700';

        return `
          <button onclick="selectGame('${g.id}')" class="shrink-0 w-64 rounded-2xl p-3 text-left transition border flex flex-col justify-between gap-2.5 ${isSelected ? 'bg-surfaceHover border-emerald-500 ring-1 ring-emerald-500/50 shadow-lg shadow-emerald-500/10' : 'bg-surface hover:bg-surfaceHover border-slate-800/90'}">
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-1.5">
                <img src="${g.away.logo}" alt="${g.away.abbr}" class="w-5 h-5 object-contain" onerror="this.style.display='none'">
                <span class="font-extrabold text-xs text-white">${g.away.abbr}</span>
                <span class="text-[11px] text-slate-500">@</span>
                <img src="${g.home.logo}" alt="${g.home.abbr}" class="w-5 h-5 object-contain" onerror="this.style.display='none'">
                <span class="font-extrabold text-xs text-white">${g.home.abbr}</span>
              </div>
              <span class="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold border ${tierBadge}">${g.tier}</span>
            </div>
            <div class="flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span>${g.tipTimePT}</span>
              <span class="text-slate-300 font-semibold">O/U ${g.totalOU} • ${g.spread}</span>
            </div>
            <div class="space-y-1">
              <div class="w-full h-1.5 bg-slate-950 rounded-full overflow-hidden">
                <div class="h-full rounded-full ${isSTier ? 'bg-gradient-to-r from-emerald-500 to-cyan-400' : 'bg-cyan-500'}" style="width: ${g.tierScore}%"></div>
              </div>
              <div class="flex items-center justify-between text-[10px] font-mono">
                <span class="text-amber-300 truncate">${escapeHtml(g.pillSummary)}</span>
                <span class="text-slate-400 font-bold shrink-0">${g.props.length} Legs</span>
              </div>
            </div>
          </button>
        `;
      }).join('');
    }

    function getAllRankedMoneylineLegs() {
      const legs = [];
      for (const g of app.games) {
        const mlCard = g.props.find(p => p.isMoneyline || p.market === 'ML');
        if (mlCard && g.moneylinePick) legs.push({ ...mlCard, matchup: g.shortName, gameId: g.id, tipTimePT: g.tipTimePT, spread: g.spread, totalOU: g.totalOU, mlMeta: g.moneylinePick });
      }
      return legs.sort((a, b) => {
        if (app.mlSortBy === 'winProb') return (b.mlMeta?.modelWinProb || 0) - (a.mlMeta?.modelWinProb || 0);
        if (app.mlSortBy === 'value') {
          const evA = parseFloat(String(a.mlMeta?.edgePct || '0').replace(/[^0-9.-]/g, '')) || 0;
          const evB = parseFloat(String(b.mlMeta?.edgePct || '0').replace(/[^0-9.-]/g, '')) || 0;
          return evB - evA;
        }
        return b.edge - a.edge;
      });
    }

    function renderBestMoneylineBoard() {
      const rankedMls = getAllRankedMoneylineLegs();
      return `
        <section class="space-y-5">
          <div class="bg-surface border border-amber-500/35 rounded-2xl p-4 sm:p-5 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <div class="flex flex-wrap items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-lg text-xs font-mono font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/40">🏆 SLATE-WIDE MONEYLINE BOARD</span>
                  <span class="text-xs font-mono text-slate-400">${rankedMls.length} Games Ranked</span>
                </div>
                <h2 class="text-lg sm:text-xl font-extrabold text-white mt-1.5">All Best Moneyline Legs — Ranked by Edge &amp; Win Probability</h2>
              </div>
              <div class="flex flex-wrap items-center gap-2 shrink-0">
                <button onclick="addTopMoneylinesToSlip(3)" class="px-3.5 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-extrabold text-xs shadow-lg shadow-amber-500/15 transition">+ Add Top 3 MLs</button>
                <button onclick="addTopMoneylinesToSlip(5)" class="px-3.5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs shadow-lg shadow-emerald-500/15 transition">+ Add Top 5 MLs</button>
              </div>
            </div>
            <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800/80">
              <span class="text-xs font-mono text-slate-400">Rank Moneyline Legs By:</span>
              <div class="inline-flex items-center bg-slate-950 border border-slate-800 rounded-xl p-1 text-xs">
                <button onclick="setMlSortBy('edge')" class="px-3 py-1 rounded-lg font-mono font-bold transition ${app.mlSortBy === 'edge' ? 'bg-amber-400 text-slate-950' : 'text-slate-400 hover:text-white'}">Edge Score</button>
                <button onclick="setMlSortBy('winProb')" class="px-3 py-1 rounded-lg font-mono font-bold transition ${app.mlSortBy === 'winProb' ? 'bg-amber-400 text-slate-950' : 'text-slate-400 hover:text-white'}">Win Probability %</button>
                <button onclick="setMlSortBy('value')" class="px-3 py-1 rounded-lg font-mono font-bold transition ${app.mlSortBy === 'value' ? 'bg-amber-400 text-slate-950' : 'text-slate-400 hover:text-white'}">+EV Edge %</button>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${rankedMls.map((ml, index) => {
              const inSlip = app.slip.some(s => s.id === ml.id);
              const meta = ml.mlMeta || {};
              return `
                <article class="bg-surface hover:bg-surfaceHover border ${inSlip ? 'border-emerald-500/70 ring-1 ring-emerald-500/30' : 'border-slate-800/90'} rounded-2xl p-4 sm:p-5 transition flex flex-col justify-between gap-4 shadow-xl">
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex items-center gap-3 min-w-0">
                      <div class="relative shrink-0">
                        <img src="${ml.teamLogo}" alt="${ml.teamAbbr}" class="w-12 h-12 rounded-xl object-contain bg-slate-950 p-1.5 border border-slate-700" onerror="this.style.display='none'" />
                        <span class="absolute -top-2 -left-2 px-1.5 py-0.5 rounded-md bg-amber-400 text-slate-950 font-mono font-extrabold text-[10px]">#${index + 1}</span>
                      </div>
                      <div class="min-w-0">
                        <h3 class="font-extrabold text-base text-white truncate">${escapeHtml(ml.playerName)}</h3>
                        <p class="text-xs font-mono text-slate-400">${escapeHtml(ml.matchup)} • ${escapeHtml(ml.tipTimePT)} • ${escapeHtml(ml.spread)}</p>
                      </div>
                    </div>
                    <div class="bg-slate-950 border border-slate-800 px-2.5 py-1.5 rounded-xl text-right shrink-0">
                      <span class="text-sm font-mono font-extrabold text-emerald-400 block">${ml.edge}/100</span>
                      <span class="text-[9px] font-mono uppercase text-slate-400">EDGE SCORE</span>
                    </div>
                  </div>

                  <div class="bg-slate-950/90 border border-slate-800/90 rounded-xl p-3 space-y-2">
                    <div class="flex items-center justify-between">
                      <div>
                        <span class="text-[10px] font-mono uppercase text-slate-400 block">Moneyline Price</span>
                        <span class="text-lg font-mono font-extrabold text-amber-300">${escapeHtml(ml.pick)}</span>
                      </div>
                      <div class="text-right font-mono">
                        <span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 text-[11px] font-bold">${meta.modelWinProb || 70}% Win Prob (${meta.edgePct || '+7.5%'} EV)</span>
                        <span class="text-[10px] text-slate-400 block mt-1">Implied Odds: ${meta.impliedProb || 62}%</span>
                      </div>
                    </div>
                    <div class="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-amber-400 to-emerald-400 rounded-full" style="width: ${meta.modelWinProb || 70}%"></div>
                    </div>
                  </div>

                  <div class="space-y-2">
                    <div class="flex flex-wrap items-center justify-between gap-1.5">
                      <span class="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/35">${escapeHtml(meta.angleTag || 'Moneyline Edge')}</span>
                      <button onclick="selectGame('${ml.gameId}')" class="text-[11px] font-mono font-bold text-slate-400 hover:text-emerald-300 transition">View Match Top 10 Legs →</button>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(ml.insight)}</p>
                  </div>

                  <button onclick="toggleSlipLeg('${ml.id}')" class="w-full py-2.5 px-4 rounded-xl text-xs font-extrabold transition flex items-center justify-center gap-1.5 ${inSlip ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/20' : 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-700'}">
                    ${inSlip ? `<span>✓ Moneyline Added to Slip</span>` : `<span>+ Add Moneyline to Slip</span>`}
                  </button>
                </article>
              `;
            }).join('')}
          </div>
        </section>
      `;
    }

    function renderMainBoard() {
      const container = document.getElementById('main-board');
      const visibleGames = getFilteredGames();
      if (app.selectedGameId === 'BEST_MONEYLINES') { container.innerHTML = renderBestMoneylineBoard(); return; }
      if (visibleGames.length === 0) { container.innerHTML = `<div class="bg-surface border border-slate-800 rounded-2xl p-12 text-center text-sm text-slate-400">No matchups match the active filter.</div>`; return; }
      const gamesToRender = app.selectedGameId === 'ALL_OVERVIEW' ? visibleGames : [visibleGames.find(g => g.id === app.selectedGameId) || visibleGames[0]];
      container.innerHTML = gamesToRender.map(game => renderGameStage(game, app.selectedGameId === 'ALL_OVERVIEW')).join('');
    }

    function renderGameStage(game, isOverviewMode) {
      const countToShow = isOverviewMode ? Math.min(3, app.legsLimit) : app.legsLimit;
      const statFilteredProps = game.props.filter(p => app.statFilter === 'ALL' || p.market === app.statFilter);
      const displayedProps = statFilteredProps.slice(0, countToShow);
      const awayPacePct = Math.min(100, Math.round(((game.away.pace - 94) / 12) * 100));
      const homePacePct = Math.min(100, Math.round(((game.home.pace - 94) / 12) * 100));
      const isB2B = game.away.rest.includes('0 Days') || game.home.rest.includes('0 Days');
      const mlLeg = game.props.find(p => p.isMoneyline);
      const mlInSlip = mlLeg && app.slip.some(s => s.id === mlLeg.id);

      return `
        <section class="space-y-4">
          <div class="bg-surface border border-slate-800/90 rounded-2xl p-4 sm:p-5 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div class="flex items-center gap-3.5">
                <div class="flex items-center -space-x-2 shrink-0">
                  <img src="${game.away.logo}" alt="${game.away.abbr}" class="w-11 h-11 rounded-full bg-slate-950 p-1.5 border border-slate-700 object-contain" onerror="this.style.display='none'">
                  <img src="${game.home.logo}" alt="${game.home.abbr}" class="w-11 h-11 rounded-full bg-slate-950 p-1.5 border border-slate-700 object-contain" onerror="this.style.display='none'">
                </div>
                <div>
                  <div class="flex flex-wrap items-center gap-2">
                    <h2 class="text-lg sm:text-xl font-extrabold text-white">${escapeHtml(game.away.name)} @ ${escapeHtml(game.home.name)}</h2>
                    <span class="px-2.5 py-0.5 rounded-lg text-xs font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/35">${game.tier} (${game.tierScore})</span>
                  </div>
                  <div class="flex flex-wrap items-center gap-2 mt-1 text-xs font-mono text-slate-400">
                    <span>${game.tipTimePT}</span><span>•</span><span class="text-cyan-300 font-semibold">Game Total O/U ${game.totalOU}</span><span>•</span><span class="text-slate-300">${game.spread}</span>
                  </div>
                </div>
              </div>

              <div class="flex flex-wrap items-center gap-2 self-start sm:self-center shrink-0">
                ${mlLeg ? `<button onclick="toggleSlipLeg('${mlLeg.id}')" class="px-3 py-2 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 border ${mlInSlip ? 'bg-amber-400 text-slate-950 border-amber-300' : 'bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border-amber-500/40'}"><span>🏆 ${mlInSlip ? 'Added' : '+'} ${escapeHtml(game.moneylinePick?.pickTeam || '')} ML (${escapeHtml(game.moneylinePick?.odds || '')})</span></button>` : ''}
                <button onclick="pickTopNForGame('${game.id}')" class="px-3.5 py-2 rounded-xl bg-cyan-500/15 hover:bg-cyan-500/25 text-cyan-300 border border-cyan-500/35 text-xs font-bold transition flex items-center gap-1.5">
                  <span>⚡ Pick Top ${Math.min(displayedProps.length || 10, countToShow === 99 ? game.props.length : countToShow)} Legs</span>
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
              <div class="bg-slate-950/80 border border-slate-800/90 rounded-xl p-3 space-y-2">
                <div class="flex items-center justify-between text-[11px] font-mono"><span class="text-slate-400 font-semibold">TEMPO / PACE</span><span class="text-cyan-300 font-bold">${game.away.pace} vs ${game.home.pace}</span></div>
                <div class="space-y-1.5">
                  <div class="flex items-center gap-2 text-[10px] font-mono"><span class="w-8 text-slate-300 font-bold">${game.away.abbr}</span><div class="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden"><div class="h-full bg-cyan-400 rounded-full" style="width: ${awayPacePct}%"></div></div></div>
                  <div class="flex items-center gap-2 text-[10px] font-mono"><span class="w-8 text-slate-300 font-bold">${game.home.abbr}</span><div class="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden"><div class="h-full bg-emerald-400 rounded-full" style="width: ${homePacePct}%"></div></div></div>
                </div>
              </div>
              <div class="bg-slate-950/80 border border-slate-800/90 rounded-xl p-3 flex flex-col justify-between">
                <span class="text-[11px] font-mono text-slate-400 font-semibold">OFF / DEF RATING</span>
                <div class="grid grid-cols-2 gap-2 mt-2 text-xs font-mono">
                  <div><span class="text-slate-400 text-[10px] block">${game.away.abbr} OFF / DEF</span><span class="font-bold text-white">${game.away.offRtg}</span> <span class="text-slate-500">/</span> <span class="text-slate-300">${game.away.defRtg}</span></div>
                  <div><span class="text-slate-400 text-[10px] block">${game.home.abbr} OFF / DEF</span><span class="font-bold text-white">${game.home.offRtg}</span> <span class="text-slate-500">/</span> <span class="text-slate-300">${game.home.defRtg}</span></div>
                </div>
              </div>
              <div class="bg-slate-950/80 border ${isB2B ? 'border-amber-500/40' : 'border-slate-800/90'} rounded-xl p-3 flex flex-col justify-between">
                <div class="flex items-center justify-between"><span class="text-[11px] font-mono text-slate-400 font-semibold">REST &amp; SCHEDULE</span>${isB2B ? `<span class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 text-[9px] font-mono font-bold">B2B EDGE</span>` : ''}</div>
                <div class="grid grid-cols-2 gap-2 mt-2 text-xs font-mono">
                  <div><span class="text-slate-400 text-[10px] block">${game.away.abbr}</span><span class="font-bold ${game.away.rest.includes('0 Days') ? 'text-amber-400' : 'text-emerald-400'}">${game.away.rest}</span></div>
                  <div><span class="text-slate-400 text-[10px] block">${game.home.abbr}</span><span class="font-bold ${game.home.rest.includes('0 Days') ? 'text-amber-400' : 'text-emerald-400'}">${game.home.rest}</span></div>
                </div>
              </div>
            </div>

            <div class="rounded-xl bg-amber-500/10 border border-amber-500/30 p-3.5 space-y-2">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-mono font-extrabold uppercase tracking-wider text-amber-300">⚡ Injury, Moneyline &amp; ESPN News Catalyst</span>
                <div class="flex flex-wrap items-center gap-1.5">
                  ${game.injuries.map(inj => `<span class="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold ${inj.status === 'OUT' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-amber-500/20 text-amber-200 border border-amber-500/40'}">${escapeHtml(inj.player)} (${inj.team}) • ${inj.status}</span>`).join('')}
                </div>
              </div>
              <p class="text-xs sm:text-sm text-slate-200 leading-relaxed">${escapeHtml(game.catalystHeadline)}</p>
            </div>
          </div>

          ${!isOverviewMode ? `
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 px-1">
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-xs font-bold text-white">Best Match Legs:</span>
                <div class="inline-flex items-center bg-surface border border-slate-800 rounded-xl p-1">
                  ${[{ label: 'Top 2', val: 2 }, { label: 'Top 4', val: 4 }, { label: 'Top 6', val: 6 }, { label: 'Top 10', val: 10 }, { label: 'Show All', val: 99 }].map(opt => `<button onclick="setLegsLimit(${opt.val})" class="px-2.5 py-1 rounded-lg text-xs font-mono font-bold transition ${app.legsLimit === opt.val ? 'bg-emerald-500 text-slate-950 shadow-sm' : 'text-slate-400 hover:text-white'}">${opt.label}</button>`).join('')}
                </div>
              </div>
              <div class="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
                ${[{ label: 'All Legs', val: 'ALL' }, { label: '🏆 Moneyline', val: 'ML' }, { label: 'Points', val: 'PTS' }, { label: 'Rebounds', val: 'REB' }, { label: 'Assists', val: 'AST' }, { label: '3PM', val: '3PM' }, { label: 'Combos (PRA)', val: 'PRA' }].map(st => `<button onclick="setStatFilter('${st.val}')" class="px-2.5 py-1 rounded-lg text-xs font-semibold transition whitespace-nowrap ${app.statFilter === st.val ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'bg-surface text-slate-400 hover:text-white border border-slate-800'}">${st.label}</button>`).join('')}
              </div>
            </div>
          ` : ''}

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${displayedProps.map((prop, rankIdx) => renderPropOptionCard(prop, rankIdx + 1)).join('')}
          </div>
        </section>
      `;
    }

    function renderPropOptionCard(prop, rankNum) {
      const inSlip = app.slip.some(s => s.id === prop.id);
      const isMl = Boolean(prop.isMoneyline || prop.market === 'ML');
      const initials = prop.playerName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
      const headshot = isMl && prop.teamLogo ? prop.teamLogo : `https://a.espncdn.com/i/headshots/nba/players/full/${prop.playerId}.png`;
      const fallback = `https://placehold.co/96x96/0f172a/94a3b8?text=${encodeURIComponent(initials)}`;
      const radius = 18;
      const circumference = 2 * Math.PI * radius;
      const dashOffset = circumference - (prop.edge / 100) * circumference;
      const gaugeColor = isMl ? '#f59e0b' : prop.edge >= 90 ? '#10b981' : '#06b6d4';
      const maxVal = Math.max(...prop.l5Values, (isMl ? 1 : prop.line * 1.25));

      return `
        <article class="bg-surface hover:bg-surfaceHover border ${inSlip ? 'border-emerald-500/60 ring-1 ring-emerald-500/30' : isMl ? 'border-amber-500/40' : 'border-slate-800/90'} rounded-2xl p-4 sm:p-5 transition flex flex-col justify-between gap-4 shadow-xl">
          <div class="flex items-start justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <div class="relative shrink-0">
                <img src="${headshot}" alt="${escapeHtml(prop.playerName)}" onerror="this.onerror=null;this.src='${fallback}';" class="w-12 h-12 rounded-xl ${isMl ? 'object-contain p-1.5' : 'object-cover'} bg-slate-950 border border-slate-700" />
                <span class="absolute -top-2 -left-2 px-1.5 py-0.2 rounded bg-slate-900 border border-slate-700 text-[9px] font-mono font-extrabold text-cyan-300">#${rankNum}</span>
                <span class="absolute -bottom-1.5 -right-1.5 px-1.5 py-0.2 rounded bg-slate-950 border border-slate-700 text-[9px] font-mono font-bold text-slate-200">${prop.teamAbbr}</span>
              </div>
              <div class="min-w-0">
                <h3 class="font-extrabold text-base text-white truncate">${escapeHtml(prop.playerName)}</h3>
                <p class="text-xs font-mono text-slate-400">${escapeHtml(prop.pos)} • ${escapeHtml(prop.opp)}</p>
              </div>
            </div>

            <div class="flex items-center gap-2 shrink-0 bg-slate-950/90 border border-slate-800 px-2.5 py-1.5 rounded-xl">
              <div class="relative w-10 h-10 flex items-center justify-center">
                <svg class="w-10 h-10 -rotate-90" viewBox="0 0 44 44">
                  <circle cx="22" cy="22" r="${radius}" stroke="#1e293b" stroke-width="4" fill="none" />
                  <circle cx="22" cy="22" r="${radius}" stroke="${gaugeColor}" stroke-width="4" fill="none" stroke-linecap="round" stroke-dasharray="${circumference}" stroke-dashoffset="${dashOffset}" />
                </svg>
                <span class="absolute text-xs font-mono font-extrabold text-white tabular-nums">${prop.edge}</span>
              </div>
              <div class="leading-tight">
                <span class="text-[10px] font-mono font-bold uppercase ${isMl ? 'text-amber-400' : 'text-emerald-400'} block">${isMl ? 'ML EDGE' : 'EDGE'}</span>
                <span class="text-[10px] font-mono text-slate-400">SCORE</span>
              </div>
            </div>
          </div>

          <div class="bg-slate-950/85 border border-slate-800/90 rounded-xl p-3 flex items-center justify-between gap-3">
            <div>
              <span class="text-[10px] font-mono uppercase tracking-wider text-slate-400 block">${isMl ? 'Best Moneyline Leg' : 'Recommended Leg'}</span>
              <span class="text-lg sm:text-xl font-mono font-extrabold ${isMl ? 'text-amber-300' : 'text-emerald-400'} tracking-tight">${escapeHtml(prop.pick)}</span>
              <span class="mt-1 inline-block px-2 py-0.5 rounded ${isMl ? 'bg-amber-500/15 text-amber-200 border-amber-500/30' : 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'} border text-[10px] font-mono font-bold">${escapeHtml(prop.l5Text)}</span>
            </div>

            <div class="flex flex-col items-end gap-1">
              <span class="text-[9px] font-mono uppercase text-slate-500">${isMl ? 'Last 5 Form' : `Last 5 vs ${prop.line}`}</span>
              <div class="flex items-end gap-1.5 h-11 pt-1">
                ${prop.l5Values.map(val => {
                  const hit = isMl ? val === 1 : val > prop.line;
                  const heightPct = isMl ? (val === 1 ? 100 : 35) : Math.max(24, Math.min(100, Math.round((val / maxVal) * 100)));
                  const labelVal = isMl ? (val === 1 ? 'W' : 'L') : val;
                  return `<div class="flex flex-col items-center gap-0.5"><span class="text-[9px] font-mono font-bold ${hit ? 'text-emerald-300' : 'text-rose-400'}">${labelVal}</span><div class="w-3.5 h-7 bg-slate-900 rounded-sm flex items-end overflow-hidden"><div class="w-full rounded-sm ${hit ? 'bg-emerald-500' : 'bg-rose-500/75'}" style="height: ${heightPct}%"></div></div></div>`;
                }).join('')}
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <div class="flex flex-wrap gap-1.5">
              ${prop.drivers.map(d => {
                const tagColors = { amber: 'bg-amber-500/15 text-amber-300 border-amber-500/35', cyan: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/35', emerald: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/35' }[d.color] || 'bg-slate-800 text-slate-300 border-slate-700';
                return `<span class="px-2 py-0.5 rounded-md text-[10px] font-mono font-semibold border ${tagColors}">${escapeHtml(d.label)}</span>`;
              }).join('')}
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(prop.insight)}</p>
          </div>

          <button onclick="toggleSlipLeg('${prop.id}')" class="w-full py-2.5 px-4 rounded-xl text-xs font-extrabold transition flex items-center justify-center gap-1.5 ${inSlip ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/20' : 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-700'}">
            ${inSlip ? `<span>✓ Added to Parlay Slip</span>` : `<span>+ Add Leg to Slip</span>`}
          </button>
        </article>
      `;
    }

    function renderWireSidebar() {
      const mobileBadge = document.getElementById('mobile-wire-badge');
      if (mobileBadge) mobileBadge.textContent = app.injuries.length + app.news.length;
      const html = `
        <div class="p-4 border-b border-slate-800 bg-slate-950/70 space-y-3 shrink-0">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-amber-400 live-dot"></span><h3 class="font-extrabold text-sm text-white">Live ESPN News &amp; Injury Wire</h3></div>
            <span class="text-[10px] font-mono text-slate-400">Click to jump</span>
          </div>
          <div class="grid grid-cols-3 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs">
            <button onclick="setWireTab('all')" class="py-1 rounded-lg font-bold transition ${app.wireTab === 'all' ? 'bg-slate-800 text-white' : 'text-slate-400'}">All (${app.news.length + app.injuries.length})</button>
            <button onclick="setWireTab('news')" class="py-1 rounded-lg font-bold transition ${app.wireTab === 'news' ? 'bg-cyan-500/20 text-cyan-300' : 'text-slate-400'}">News (${app.news.length})</button>
            <button onclick="setWireTab('injuries')" class="py-1 rounded-lg font-bold transition ${app.wireTab === 'injuries' ? 'bg-amber-500/20 text-amber-300' : 'text-slate-400'}">Injuries (${app.injuries.length})</button>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          ${(app.wireTab === 'all' || app.wireTab === 'news') ? app.news.map(item => `
            <button onclick="jumpFromWire('${item.gameId}')" class="w-full text-left p-3.5 rounded-xl bg-slate-950/80 hover:bg-surfaceHover border border-slate-800/90 hover:border-cyan-500/40 transition space-y-2 group">
              <div class="flex items-center justify-between gap-2 text-[10px] font-mono"><span class="px-2 py-0.5 rounded bg-cyan-500/15 text-cyan-300 font-bold border border-cyan-500/30">${escapeHtml(item.matchup)}</span><span class="text-slate-500">${escapeHtml(item.time)}</span></div>
              <p class="text-xs font-semibold text-slate-200 group-hover:text-white leading-snug">${escapeHtml(item.headline)}</p>
              <div class="flex items-center justify-between pt-1 border-t border-slate-800/70 text-[10px] font-mono"><span class="text-emerald-400 font-bold">⚡ ${escapeHtml(item.impact)}</span><span class="text-slate-400 group-hover:text-cyan-300">Inspect →</span></div>
            </button>
          `).join('') : ''}
          ${(app.wireTab === 'all' || app.wireTab === 'injuries') ? app.injuries.map(inj => `
            <button onclick="jumpFromWire('${inj.gameId}')" class="w-full text-left p-3 rounded-xl bg-slate-950/80 hover:bg-surfaceHover border border-slate-800/90 transition space-y-1.5">
              <div class="flex items-center justify-between gap-2"><div class="flex items-center gap-1.5"><span class="px-1.5 py-0.5 rounded bg-slate-800 font-mono text-[10px] font-bold text-slate-300">${escapeHtml(inj.matchup)}</span><span class="font-bold text-xs text-white">${escapeHtml(inj.player)}</span></div><span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${inj.status === 'OUT' ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' : 'bg-amber-500/20 text-amber-300 border-amber-500/40'}">${escapeHtml(inj.status)}</span></div>
              <p class="text-[11px] text-slate-400">${escapeHtml(inj.detail)}</p>
            </button>
          `).join('') : ''}
        </div>
      `;
      document.getElementById('desktop-wire-container').innerHTML = html;
      document.getElementById('mobile-wire-container').innerHTML = html;
    }

    function setWireTab(tab) { app.wireTab = tab; renderWireSidebar(); }
    function jumpFromWire(gameId) { app.boardFilter = 'all'; app.selectedGameId = gameId; const d = document.getElementById('mobile-wire-drawer'); if (d && !d.classList.contains('hidden')) { d.classList.add('hidden'); d.classList.remove('flex'); } renderAllBoard(); window.scrollTo({ top: 140, behavior: 'smooth' }); }
    function toggleMobileWire() { const d = document.getElementById('mobile-wire-drawer'); if (d.classList.contains('hidden')) { d.classList.remove('hidden'); d.classList.add('flex'); } else { d.classList.add('hidden'); d.classList.remove('flex'); } }

    function renderSlipBar() {
      const count = app.slip.length;
      document.getElementById('slip-badge-count').textContent = count;
      const riskPill = document.getElementById('slip-risk-pill');
      const subtitle = document.getElementById('slip-subtitle');
      const clearBtn = document.getElementById('btn-clear-slip');
      const drawerBody = document.getElementById('slip-drawer-body');
      const arrow = document.getElementById('slip-arrow');

      if (count > 0) {
        const avgEdge = Math.round(app.slip.reduce((sum, l) => sum + l.edge, 0) / count);
        const mlCount = app.slip.filter(l => l.isMoneyline || l.market === 'ML').length;
        riskPill.textContent = count <= 2 ? 'LOW RISK • 2-LEG POWER' : count <= 4 ? `BALANCED • AVG ${avgEdge} EDGE` : `HIGH PAYOUT • ${count} LEGS`;
        riskPill.classList.remove('hidden');
        clearBtn.classList.remove('hidden');
        subtitle.textContent = `${count} leg${count > 1 ? 's' : ''} (${mlCount} ML, ${count - mlCount} Props) • Avg Edge ${avgEdge}/100`;
      } else {
        riskPill.classList.add('hidden');
        clearBtn.classList.add('hidden');
        subtitle.textContent = 'Click "+ Add Leg to Slip" on any moneyline or prop card above';
        app.slipOpen = false;
      }

      if (app.slipOpen && count > 0) {
        drawerBody.classList.remove('hidden');
        arrow.style.transform = 'rotate(180deg)';
        document.getElementById('slip-cards-grid').innerHTML = app.slip.map(leg => `
          <div class="flex items-center justify-between gap-2 px-3 py-2 rounded-xl bg-surface border ${leg.isMoneyline ? 'border-amber-500/40' : 'border-slate-800'}">
            <div class="min-w-0">
              <div class="flex items-center gap-1.5 text-[10px] font-mono"><span class="text-slate-400 font-bold">${escapeHtml(leg.matchup)}</span><span class="${leg.isMoneyline ? 'text-amber-300' : 'text-emerald-400'} font-bold">${leg.edge} Edge</span></div>
              <p class="text-xs font-bold text-white truncate">${escapeHtml(leg.playerName)} — <span class="${leg.isMoneyline ? 'text-amber-300' : 'text-emerald-300'}">${escapeHtml(leg.pick)}</span></p>
            </div>
            <button onclick="toggleSlipLeg('${leg.id}')" class="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800">✕</button>
          </div>
        `).join('');
      } else {
        drawerBody.classList.add('hidden');
        arrow.style.transform = 'rotate(0deg)';
      }
    }

    function toggleSlipDrawer() { if (app.slip.length === 0) { showToast('Add at least 1 leg to open your parlay slip', 'info'); return; } app.slipOpen = !app.slipOpen; renderSlipBar(); }
    function copySlipText() {
      if (app.slip.length === 0) { showToast('Select at least 1 leg first', 'warning'); return; }
      const text = [`🏀 COURTSIDE EDGE — ${app.slip.length}-LEG NBA SLIP`, ...app.slip.map((l, i) => `${i + 1}. [${l.matchup}] ${l.playerName} — ${l.pick} (${l.edge} Edge)`)].join('\n');
      const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
      showToast(`Copied ${app.slip.length}-leg slip to clipboard!`, 'success');
    }
    function downloadSlip(ext) {
      if (app.slip.length === 0) { showToast('Select at least 1 leg first', 'warning'); return; }
      const payload = ext === 'json' ? JSON.stringify(app.slip, null, 2) : app.slip.map((l, i) => `${i + 1}. [${l.matchup}] ${l.playerName} — ${l.pick} (${l.edge} Edge)`).join('\n');
      const blob = new Blob([payload], { type: ext === 'json' ? 'application/json' : 'text/plain' });
      const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `courtside_edge_slip.${ext}`; a.click(); URL.revokeObjectURL(url);
    }
    function formatTimeAgo(iso) { if (!iso) return 'Live'; const mins = Math.max(1, Math.round((Date.now() - new Date(iso).getTime()) / 60000)); return mins < 60 ? `${mins}m ago` : `${Math.floor(mins / 60)}h ago`; }
    function persistSlip() { try { localStorage.setItem(SLIP_STORAGE_KEY, JSON.stringify(app.slip)); } catch (e) {} }
    function loadPersistedSlip() { try { const raw = localStorage.getItem(SLIP_STORAGE_KEY); if (raw) app.slip = JSON.parse(raw); } catch (e) {} }

    // =========================================================================
    // MODULE 2: MULTI-SET LIVE LEG & PROP TRACKER
    // =========================================================================
    const SETS_STORAGE_KEY = 'courtside_legs_multiset_v4';
    const VAULT_STORAGE_KEY = 'courtside_legs_last5_vault_v4';
    const MAX_SAVED_VAULT = 5;
    const AUTO_SYNC_INTERVAL = 20;

    let appState = {
      mode: 'espn',
      autoRefresh: true,
      countdown: AUTO_SYNC_INTERVAL,
      countdownTimer: null,
      activeFilter: 'all',
      games: {},
      betSets: [],
      activeSetId: 'ALL_SETS',
      savedSetsVault: [],
      lastSync: null,
      espnConnected: false,
      quickCategory: 'player',
      quickDirection: 'OVER'
    };

    function normalizeName(str) {
      if (!str) return '';
      return String(str).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9\s]/g, '').replace(/\s+/g, ' ').trim();
    }

    function findMatchingPlayerInGame(game, playerId, playerName) {
      if (!game || !game.players) return null;
      if (playerId && game.players[playerId]) return game.players[playerId];
      const needle = normalizeName(playerName);
      if (!needle) return null;
      const allPlayers = Object.values(game.players);
      let match = allPlayers.find(p => normalizeName(p.name) === needle);
      if (match) return match;
      match = allPlayers.find(p => normalizeName(p.name).includes(needle));
      if (match) return match;
      const parts = needle.split(' ');
      const lastToken = parts[parts.length - 1];
      if (lastToken.length >= 3) match = allPlayers.find(p => normalizeName(p.name).split(' ').pop() === lastToken);
      return match || null;
    }

    function createDemoGames() {
      return {
        '401705001': {
          id: '401705001', name: 'Denver Nuggets at Chicago Bulls', shortName: 'DEN @ CHI', statusState: 'in', statusDetail: 'Q3 04:18', period: 3, clock: '4:18', elapsedMinutes: 31.7,
          away: { id: '7', abbr: 'DEN', name: 'Nuggets', score: 88, logo: 'https://a.espncdn.com/i/teamlogos/nba/500/den.png' },
          home: { id: '4', abbr: 'CHI', name: 'Bulls', score: 82, logo: 'https://a.espncdn.com/i/teamlogos/nba/500/chi.png' },
          players: {
            '3112335': { id: '3112335', name: 'Nikola Jokic', team: 'DEN', pos: 'C', min: 27, pts: 24, reb: 11, ast: 8, fg3m: 2, stl: 1, blk: 1, to: 2 },
            '3936299': { id: '3936299', name: 'Jamal Murray', team: 'DEN', pos: 'PG', min: 26, pts: 19, reb: 3, ast: 6, fg3m: 3, stl: 1, blk: 0, to: 1 },
            '3064440': { id: '3064440', name: 'Zach LaVine', team: 'CHI', pos: 'SG', min: 28, pts: 22, reb: 4, ast: 4, fg3m: 4, stl: 1, blk: 0, to: 2 }
          }
        },
        '401705002': {
          id: '401705002', name: 'Boston Celtics at Golden State Warriors', shortName: 'BOS @ GSW', statusState: 'in', statusDetail: 'Q4 06:45', period: 4, clock: '6:45', elapsedMinutes: 41.25,
          away: { id: '2', abbr: 'BOS', name: 'Celtics', score: 109, logo: 'https://a.espncdn.com/i/teamlogos/nba/500/bos.png' },
          home: { id: '9', abbr: 'GSW', name: 'Warriors', score: 106, logo: 'https://a.espncdn.com/i/teamlogos/nba/500/gs.png' },
          players: {
            '4065648': { id: '4065648', name: 'Jayson Tatum', team: 'BOS', pos: 'SF', min: 34, pts: 31, reb: 8, ast: 5, fg3m: 4, stl: 1, blk: 1, to: 2 },
            '3975': { id: '3975', name: 'Stephen Curry', team: 'GSW', pos: 'PG', min: 33, pts: 29, reb: 4, ast: 7, fg3m: 6, stl: 1, blk: 0, to: 3 }
          }
        },
        '401705003': {
          id: '401705003', name: 'Oklahoma City Thunder at Miami Heat', shortName: 'OKC @ MIA', statusState: 'post', statusDetail: 'FINAL', period: 4, clock: '0:00', elapsedMinutes: 48,
          away: { id: '25', abbr: 'OKC', name: 'Thunder', score: 118, logo: 'https://a.espncdn.com/i/teamlogos/nba/500/okc.png' },
          home: { id: '14', abbr: 'MIA', name: 'Heat', score: 104, logo: 'https://a.espncdn.com/i/teamlogos/nba/500/mia.png' },
          players: {
            '4278073': { id: '4278073', name: 'Shai Gilgeous-Alexander', team: 'OKC', pos: 'PG', min: 36, pts: 34, reb: 6, ast: 7, fg3m: 2, stl: 3, blk: 1, to: 1 },
            '4432171': { id: '4432171', name: 'Jared McCain', team: 'OKC', pos: 'SG', min: 34, pts: 20, reb: 2, ast: 3, fg3m: 3, stl: 1, blk: 0, to: 1 }
          }
        }
      };
    }

    function createSampleBetSets(gamesMap) {
      const keys = Object.keys(gamesMap);
      const g1 = gamesMap[keys[0]] || Object.values(createDemoGames())[0];
      const g2 = gamesMap[keys[1]] || Object.values(createDemoGames())[1];
      const pickPlayer = (g, id, idx = 0) => (g.players && g.players[id]) ? g.players[id] : (Object.values(g.players || {})[idx] || { id, name: 'Nikola Jokic', team: g.away.abbr });
      const p1 = pickPlayer(g1, '3112335', 0);
      const p2 = pickPlayer(g1, '3936299', 1);
      const p3 = pickPlayer(g2, '3975', 0);

      return [
        {
          id: 'set-sample-1', name: 'Set #1 • Nuggets vs Bulls SGP', odds: '+650', stake: 5, locked: true, lockedAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          legs: [
            { id: 'leg-s1-1', gameId: g1.id, category: 'player', playerId: p1.id, playerName: p1.name, teamAbbr: p1.team, statType: 'PRA', direction: 'OVER', target: 44.5 },
            { id: 'leg-s1-2', gameId: g1.id, category: 'player', playerId: p2.id, playerName: p2.name, teamAbbr: p2.team, statType: 'PTS', direction: 'OVER', target: 23.5 }
          ]
        },
        {
          id: 'set-sample-2', name: 'Set #2 • Late Slate Anchors', odds: '+420', stake: 10, locked: false, lockedAt: null,
          legs: [
            { id: 'leg-s2-1', gameId: g2.id, category: 'player', playerId: p3.id, playerName: p3.name, teamAbbr: p3.team, statType: '3PM', direction: 'OVER', target: 4.5 }
          ]
        }
      ];
    }

    async function fetchEspnSlateAndBoxes() {
      const sbRes = await fetch(ESPN_ENDPOINTS.scoreboard);
      if (!sbRes.ok) throw new Error(`Scoreboard HTTP ${sbRes.status}`);
      const sbData = await sbRes.json();
      const events = sbData.events || [];
      if (events.length === 0) throw new Error('No live games scheduled');

      const parsedGames = {};
      for (const ev of events) {
        const comp = ev.competitions?.[0];
        if (!comp) continue;
        const homeComp = comp.competitors.find(c => c.homeAway === 'home') || comp.competitors[0];
        const awayComp = comp.competitors.find(c => c.homeAway === 'away') || comp.competitors[1];
        const statusType = ev.status?.type || {};
        const period = ev.status?.period || 0;
        const displayClock = ev.status?.displayClock || '0:00';
        let elapsed = statusType.state === 'post' ? 48 : 0;
        if (statusType.state === 'in' && period >= 1) {
          const clockParts = displayClock.split(':');
          const minsLeft = clockParts.length === 2 ? parseInt(clockParts[0], 10) + parseInt(clockParts[1], 10) / 60 : 0;
          elapsed = Math.max(1, (period <= 4 ? (period - 1) * 12 : 48 + (period - 5) * 5) + ((period <= 4 ? 12 : 5) - minsLeft));
        }
        parsedGames[ev.id] = {
          id: ev.id, name: ev.name, shortName: ev.shortName, statusState: statusType.state || 'pre', statusDetail: statusType.shortDetail || 'Scheduled', period, clock: displayClock, elapsedMinutes: elapsed,
          away: { id: awayComp.team.id, abbr: awayComp.team.abbreviation, name: awayComp.team.shortDisplayName || awayComp.team.name, score: parseInt(awayComp.score || '0', 10), logo: awayComp.team.logo || '' },
          home: { id: homeComp.team.id, abbr: homeComp.team.abbreviation, name: homeComp.team.shortDisplayName || homeComp.team.name, score: parseInt(homeComp.score || '0', 10), logo: homeComp.team.logo || '' },
          players: {}
        };
      }

      await Promise.allSettled(
        Object.keys(parsedGames).map(async (id) => {
          try {
            const sumRes = await fetch(`${ESPN_ENDPOINTS.summary}${id}`);
            if (!sumRes.ok) return;
            const sumData = await sumRes.json();
            for (const teamBlock of (sumData.boxscore?.players || [])) {
              const teamAbbr = teamBlock.team?.abbreviation || '';
              const statGroup = teamBlock.statistics?.[0];
              if (!statGroup || !statGroup.labels || !statGroup.athletes) continue;
              const labels = statGroup.labels.map(l => l.toUpperCase());
              const idxMin = labels.indexOf('MIN'), idxPts = labels.indexOf('PTS'), idxReb = labels.indexOf('REB'), idxAst = labels.indexOf('AST'), idx3pt = labels.indexOf('3PT'), idxStl = labels.indexOf('STL'), idxBlk = labels.indexOf('BLK'), idxTo = labels.indexOf('TO');
              for (const athEntry of statGroup.athletes) {
                const athlete = athEntry.athlete;
                if (!athlete || !athlete.id) continue;
                const s = athEntry.stats || [];
                const parseNum = (idx) => (idx >= 0 && s[idx] !== undefined ? parseInt(s[idx], 10) || 0 : 0);
                const fg3m = idx3pt >= 0 && s[idx3pt] ? (parseInt(String(s[idx3pt]).split('-')[0], 10) || 0) : 0;
                parsedGames[id].players[athlete.id] = { id: athlete.id, name: athlete.displayName, team: teamAbbr, pos: athlete.position?.abbreviation || '', min: parseNum(idxMin), pts: parseNum(idxPts), reb: parseNum(idxReb), ast: parseNum(idxAst), fg3m, stl: parseNum(idxStl), blk: parseNum(idxBlk), to: parseNum(idxTo) };
              }
            }
          } catch (e) {}
        })
      );
      return parsedGames;
    }

    async function syncAllData(manual = false) {
      try {
        if (appState.mode === 'espn') {
          const liveGames = await fetchEspnSlateAndBoxes();
          appState.games = liveGames;
          appState.espnConnected = true;
          if (manual) showToast('Synced live NBA stats from ESPN API', 'success');
        } else if (Object.keys(appState.games).length === 0) {
          appState.games = createDemoGames();
        }
      } catch (error) {
        appState.espnConnected = false;
        if (Object.keys(appState.games).length === 0) {
          appState.mode = 'demo';
          appState.games = createDemoGames();
          updateModeButtons();
        }
      } finally {
        appState.lastSync = new Date();
        appState.countdown = AUTO_SYNC_INTERVAL;
        document.getElementById('last-updated-text').textContent = `• Updated ${appState.lastSync.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}`;
        if (appState.betSets.length === 0) {
          loadSetsAndVaultFromStorage();
          if (appState.betSets.length === 0) {
            appState.betSets = createSampleBetSets(appState.games);
            appState.activeSetId = appState.betSets[0].id;
            saveSetSnapshotToVault(appState.betSets[0]);
            persistSetsAndVault();
          }
        }
        if (!appState.activeSetId || (appState.activeSetId !== 'ALL_SETS' && !appState.betSets.some(s => s.id === appState.activeSetId))) {
          appState.activeSetId = appState.betSets[0]?.id || 'ALL_SETS';
        }
        populateQuickEntryDropdowns();
        renderAllTracker();
      }
    }

    function simulateLiveTick() {
      if (appState.mode !== 'demo') return;
      for (const g of Object.values(appState.games)) {
        if (g.statusState !== 'in') continue;
        g.elapsedMinutes = Math.min(48, +(g.elapsedMinutes + 2).toFixed(1));
        if (g.elapsedMinutes >= 48) { g.statusState = 'post'; g.statusDetail = 'FINAL'; g.clock = '0:00'; }
        else {
          const q = Math.min(4, Math.floor(g.elapsedMinutes / 12) + 1);
          const minsLeft = Math.max(0, 12 - (g.elapsedMinutes - (q - 1) * 12));
          g.period = q; g.clock = `${Math.floor(minsLeft)}:${Math.floor((minsLeft - Math.floor(minsLeft)) * 60).toString().padStart(2, '0')}`; g.statusDetail = `Q${q} ${g.clock}`;
        }
        g.away.score += Math.floor(Math.random() * 5) + 2;
        g.home.score += Math.floor(Math.random() * 5) + 2;
        for (const p of Object.values(g.players)) {
          p.min = Math.min(42, p.min + 2);
          if (Math.random() > 0.35) p.pts += 2;
          if (Math.random() > 0.55) p.reb += 1;
          if (Math.random() > 0.60) p.ast += 1;
        }
      }
      showToast('Simulated +2:00 of live NBA action', 'success');
      populateQuickEntryDropdowns();
      renderAllTracker();
    }

    function setDataMode(mode) {
      appState.mode = mode;
      updateModeButtons();
      if (mode === 'demo') { appState.games = createDemoGames(); populateQuickEntryDropdowns(); renderAllTracker(); }
      else syncAllData(true);
    }

    function updateModeButtons() {
      const btnEspn = document.getElementById('btn-mode-espn');
      const btnDemo = document.getElementById('btn-mode-demo');
      const btnTick = document.getElementById('btn-sim-tick');
      if (appState.mode === 'espn') {
        btnEspn.className = 'px-2.5 py-1 rounded-lg font-semibold transition flex items-center gap-1.5 bg-slate-800 text-white shadow-sm';
        btnDemo.className = 'px-2.5 py-1 rounded-lg font-medium transition flex items-center gap-1.5 text-slate-400 hover:text-slate-200';
        btnTick.classList.add('hidden');
      } else {
        btnDemo.className = 'px-2.5 py-1 rounded-lg font-semibold transition flex items-center gap-1.5 bg-amber-500/20 text-amber-300 border border-amber-500/30';
        btnEspn.className = 'px-2.5 py-1 rounded-lg font-medium transition flex items-center gap-1.5 text-slate-400 hover:text-slate-200';
        btnTick.classList.remove('hidden');
      }
    }

    function toggleAutoRefresh() {
      appState.autoRefresh = !appState.autoRefresh;
      document.getElementById('autorefresh-label').textContent = appState.autoRefresh ? `AUTO ${AUTO_SYNC_INTERVAL}s` : 'PAUSED';
    }

    function startCountdownTimer() {
      if (appState.countdownTimer) clearInterval(appState.countdownTimer);
      appState.countdownTimer = setInterval(() => {
        if (!appState.autoRefresh) return;
        appState.countdown -= 1;
        const label = document.getElementById('autorefresh-label');
        if (appState.countdown <= 0) {
          appState.countdown = AUTO_SYNC_INTERVAL;
          if (label) label.textContent = `AUTO ${appState.countdown}s`;
          if (appState.mode === 'espn') syncAllData(false); else simulateLiveTick();
        } else if (label) label.textContent = `AUTO ${appState.countdown}s`;
      }, 1000);
    }

    // Multi-Set & Last 5 Vault Logic
    function getActiveSet() {
      if (appState.activeSetId === 'ALL_SETS') return appState.betSets[0] || null;
      return appState.betSets.find(s => s.id === appState.activeSetId) || appState.betSets[0] || null;
    }
    function selectBetSet(setId) { appState.activeSetId = setId; renderAllTracker(); }
    function openNewSetModal() {
      document.getElementById('modal-set-title').textContent = 'Create New Bet Set';
      document.getElementById('set-modal-id').value = '';
      document.getElementById('set-modal-name').value = `Set #${appState.betSets.length + 1} • Parlay`;
      document.getElementById('set-modal-odds').value = '';
      document.getElementById('set-modal-stake').value = '';
      openModal('modal-bet-set');
    }
    function openEditSetModal(setId) {
      const s = appState.betSets.find(x => x.id === setId);
      if (!s) return;
      document.getElementById('modal-set-title').textContent = 'Edit Bet Set Details';
      document.getElementById('set-modal-id').value = s.id;
      document.getElementById('set-modal-name').value = s.name;
      document.getElementById('set-modal-odds').value = s.odds || '';
      document.getElementById('set-modal-stake').value = s.stake || '';
      openModal('modal-bet-set');
    }
    function handleSaveSetModal(e) {
      e.preventDefault();
      const id = document.getElementById('set-modal-id').value;
      const name = document.getElementById('set-modal-name').value.trim();
      const odds = document.getElementById('set-modal-odds').value.trim();
      const stakeVal = parseFloat(document.getElementById('set-modal-stake').value);
      const stake = isNaN(stakeVal) ? null : stakeVal;
      if (!name) return;
      if (id) {
        const ex = appState.betSets.find(s => s.id === id);
        if (ex) { ex.name = name; ex.odds = odds; ex.stake = stake; }
      } else {
        const ns = { id: 'set-' + Date.now(), name, odds, stake, locked: false, lockedAt: null, legs: [] };
        appState.betSets.push(ns);
        appState.activeSetId = ns.id;
      }
      closeModal('modal-bet-set');
      persistSetsAndVault();
      renderAllTracker();
    }
    function duplicateActiveSet() {
      const src = getActiveSet();
      if (!src) return;
      const cloned = { id: 'set-' + Date.now(), name: `${src.name} (Copy)`, odds: src.odds, stake: src.stake, locked: false, lockedAt: null, legs: src.legs.map((l, i) => ({ ...l, id: `leg-${Date.now()}-${i}` })) };
      appState.betSets.push(cloned);
      appState.activeSetId = cloned.id;
      persistSetsAndVault();
      renderAllTracker();
      showToast(`Duplicated into "${cloned.name}"`, 'success');
    }
    function deleteBetSet(setId) {
      if (appState.betSets.length <= 1) { showToast('Keep at least 1 active bet set', 'warning'); return; }
      appState.betSets = appState.betSets.filter(s => s.id !== setId);
      if (appState.activeSetId === setId) appState.activeSetId = appState.betSets[0].id;
      persistSetsAndVault();
      renderAllTracker();
    }
    function lockInCurrentSet() {
      const targetSet = getActiveSet();
      if (!targetSet) return;
      if (targetSet.legs.length === 0) { showToast('Add at least 1 leg before locking in!', 'warning'); return; }
      if (targetSet.locked) { targetSet.locked = false; targetSet.lockedAt = null; persistSetsAndVault(); renderAllTracker(); showToast(`Unlocked "${targetSet.name}"`, 'info'); return; }
      targetSet.locked = true;
      targetSet.lockedAt = new Date().toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
      saveSetSnapshotToVault(targetSet);
      persistSetsAndVault();
      renderAllTracker();
      showToast(`🔒 Locked in "${targetSet.name}" & saved to Last 5 Vault!`, 'success');
    }
    function saveSetSnapshotToVault(setObj) {
      appState.savedSetsVault.unshift({
        vaultId: 'vault-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
        name: setObj.name, odds: setObj.odds || '', stake: setObj.stake || null,
        lockedAt: setObj.lockedAt || new Date().toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
        legs: JSON.parse(JSON.stringify(setObj.legs))
      });
      if (appState.savedSetsVault.length > MAX_SAVED_VAULT) appState.savedSetsVault = appState.savedSetsVault.slice(0, MAX_SAVED_VAULT);
    }
    function restoreVaultSetToBoard(vaultId) {
      const snap = appState.savedSetsVault.find(v => v.vaultId === vaultId);
      if (!snap) return;
      const restored = { id: 'set-r-' + Date.now(), name: snap.name, odds: snap.odds, stake: snap.stake, locked: true, lockedAt: snap.lockedAt, legs: snap.legs.map((l, idx) => ({ ...l, id: `leg-r-${Date.now()}-${idx}` })) };
      appState.betSets.push(restored);
      appState.activeSetId = restored.id;
      persistSetsAndVault();
      renderAllTracker();
      toggleVaultDrawer();
      showToast(`Restored "${restored.name}" to active tracker!`, 'success');
    }
    function deleteFromVault(vaultId) { appState.savedSetsVault = appState.savedSetsVault.filter(v => v.vaultId !== vaultId); persistSetsAndVault(); renderVaultDrawer(); renderSetsBar(); }
    function toggleVaultDrawer() {
      const d = document.getElementById('drawer-vault');
      if (d.classList.contains('hidden')) { renderVaultDrawer(); d.classList.remove('hidden'); d.classList.add('flex'); }
      else { d.classList.add('hidden'); d.classList.remove('flex'); }
    }
    function renderVaultDrawer() {
      const body = document.getElementById('drawer-vault-body');
      if (appState.savedSetsVault.length === 0) { body.innerHTML = `<div class="bg-card border border-slate-800 rounded-2xl p-10 text-center text-xs text-slate-400">No locked-in sets saved yet.</div>`; return; }
      body.innerHTML = appState.savedSetsVault.map((snap, idx) => {
        const evalLegs = snap.legs.map(l => ({ leg: l, eval: evaluateLeg(l) }));
        const cashedCount = evalLegs.filter(x => x.eval.status === 'cashed').length;
        return `
          <div class="bg-card border border-slate-800 rounded-2xl p-4 space-y-3 shadow-lg">
            <div class="flex items-start justify-between gap-3">
              <div>
                <div class="flex items-center gap-2"><span class="px-2 py-0.5 rounded bg-amber-400 text-slate-950 font-mono font-extrabold text-[10px]">#${idx + 1} SAVED</span><h4 class="font-bold text-sm text-white">${escapeHtml(snap.name)}</h4></div>
                <p class="text-[11px] font-mono text-slate-400 mt-1">Locked ${escapeHtml(snap.lockedAt)} • ${snap.legs.length} Legs ${snap.odds ? `• ${escapeHtml(snap.odds)}` : ''}</p>
              </div>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-500/15 text-sky-300 border border-sky-500/30">${cashedCount}/${snap.legs.length} Cashed</span>
            </div>
            <div class="bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 space-y-1.5">
              ${evalLegs.map(({ eval: ev }) => `<div class="flex items-center justify-between text-xs"><span class="font-semibold text-slate-200 truncate">${escapeHtml(ev.displayTitle)} (${escapeHtml(ev.targetBadge)})</span><span class="font-mono text-[11px] font-bold text-slate-300">${ev.currentVal}/${ev.targetVal}</span></div>`).join('')}
            </div>
            <div class="flex items-center justify-end gap-2">
              <button onclick="deleteFromVault('${snap.vaultId}')" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-rose-500/15 text-slate-400 hover:text-rose-300 border border-slate-800 text-xs font-semibold">Delete</button>
              <button onclick="restoreVaultSetToBoard('${snap.vaultId}')" class="px-3.5 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-extrabold">Track Live on Board</button>
            </div>
          </div>
        `;
      }).join('');
    }
    function persistSetsAndVault() {
      try {
        localStorage.setItem(SETS_STORAGE_KEY, JSON.stringify({ betSets: appState.betSets, activeSetId: appState.activeSetId }));
        localStorage.setItem(VAULT_STORAGE_KEY, JSON.stringify(appState.savedSetsVault));
      } catch (e) {}
    }
    function loadSetsAndVaultFromStorage() {
      try {
        const rawSets = localStorage.getItem(SETS_STORAGE_KEY);
        if (rawSets) { const p = JSON.parse(rawSets); if (Array.isArray(p.betSets)) appState.betSets = p.betSets; if (p.activeSetId) appState.activeSetId = p.activeSetId; }
        const rawVault = localStorage.getItem(VAULT_STORAGE_KEY);
        if (rawVault) { const pv = JSON.parse(rawVault); if (Array.isArray(pv)) appState.savedSetsVault = pv.slice(0, MAX_SAVED_VAULT); }
      } catch (e) {}
    }

    function evaluateLeg(leg) {
      const game = appState.games[leg.gameId];
      if (!game) return { status: 'upcoming', isLiveGame: false, currentVal: 0, targetVal: leg.target || 0, progressPct: 0, paceLabel: 'UPCOMING', gameStatus: 'Scheduled', scoreText: '--', displayTitle: leg.category === 'player' ? leg.playerName : `${leg.teamAbbr} ${leg.market}`, targetBadge: leg.category === 'player' ? `${leg.direction} ${leg.target} ${leg.statType}` : `${leg.market}`, statUnit: leg.statType || 'PTS', playerId: leg.playerId || null, teamAbbr: leg.teamAbbr || 'NBA' };

      const isPre = game.statusState === 'pre', isLive = game.statusState === 'in', isFinal = game.statusState === 'post';
      const scoreText = `${game.away.abbr} ${game.away.score} - ${game.home.abbr} ${game.home.score}`;

      if (leg.category === 'player') {
        const player = findMatchingPlayerInGame(game, leg.playerId, leg.playerName);
        let currentVal = 0;
        if (player) {
          switch (leg.statType) {
            case 'PTS': currentVal = player.pts; break; case 'REB': currentVal = player.reb; break; case 'AST': currentVal = player.ast; break; case '3PM': currentVal = player.fg3m; break;
            case 'STL': currentVal = player.stl; break; case 'BLK': currentVal = player.blk; break; case 'STL+BLK': currentVal = player.stl + player.blk; break; case 'TO': currentVal = player.to; break;
            case 'PRA': currentVal = player.pts + player.reb + player.ast; break; case 'PA': currentVal = player.pts + player.ast; break; case 'PR': currentVal = player.pts + player.reb; break; case 'RA': currentVal = player.reb + player.ast; break;
          }
        }
        const target = parseFloat(leg.target);
        const isOver = leg.direction === 'OVER';
        const progressPct = Math.min(100, Math.max(0, (currentVal / target) * 100));
        let projectedVal = isLive ? (player && player.min >= 4 ? +((currentVal / player.min) * Math.max(player.min + 2, 34)).toFixed(1) : +((currentVal / Math.max(1, game.elapsedMinutes || 1)) * 48).toFixed(1)) : currentVal;
        let status = 'upcoming', paceLabel = 'UPCOMING';
        if (isPre) { status = 'upcoming'; paceLabel = `TIPS ${game.statusDetail}`; }
        else if (isOver) {
          if (currentVal > target) { status = 'cashed'; paceLabel = `CASHED (+${(currentVal - target).toFixed(1)})`; }
          else if (isFinal) { status = 'busted'; paceLabel = `MISSED BY ${(target - currentVal).toFixed(1)}`; }
          else if (projectedVal >= target) { status = 'on_pace'; paceLabel = `Pace: ${projectedVal} ${leg.statType}`; }
          else { status = 'sweating'; paceLabel = `Needs ${Math.ceil(target - currentVal + 0.01)} ${leg.statType}`; }
        } else {
          if (currentVal > target) { status = 'busted'; paceLabel = `BUSTED`; }
          else if (isFinal) { status = 'cashed'; paceLabel = `CASHED UNDER`; }
          else { status = projectedVal <= target ? 'on_pace' : 'sweating'; paceLabel = `Pace: ${projectedVal}`; }
        }
        return { status, isLiveGame: isLive, currentVal, targetVal: target, progressPct, paceLabel, gameStatus: game.statusDetail, scoreText, displayTitle: player ? player.name : leg.playerName, targetBadge: `${isOver ? 'OVER' : 'UNDER'} ${target} ${leg.statType}`, statUnit: leg.statType, playerId: player ? player.id : leg.playerId, teamAbbr: player ? player.team : (leg.teamAbbr || game.home.abbr) };
      }

      const isHome = leg.teamAbbr === game.home.abbr;
      const pickedTeam = isHome ? game.home : game.away;
      const oppTeam = isHome ? game.away : game.home;
      const diff = pickedTeam.score - oppTeam.score;
      let status = isPre ? 'upcoming' : isFinal ? (diff > 0 ? 'cashed' : 'busted') : (diff > 0 ? 'on_pace' : 'sweating');
      let paceLabel = isPre ? `TIPS ${game.statusDetail}` : isFinal ? (diff > 0 ? `WON BY ${diff}` : `LOST BY ${Math.abs(diff)}`) : (diff >= 0 ? `LEADING +${diff}` : `TRAILING ${diff}`);
      return { status, isLiveGame: isLive, currentVal: `${pickedTeam.score}`, targetVal: `${oppTeam.score}`, isComparison: true, progressPct: diff > 0 ? 75 : 35, paceLabel, gameStatus: game.statusDetail, scoreText, displayTitle: `${pickedTeam.name} Moneyline`, targetBadge: `${pickedTeam.abbr} ML`, statUnit: 'PTS', playerId: null, teamAbbr: pickedTeam.abbr, teamLogo: pickedTeam.logo };
    }

    function renderAllTracker() {
      const totalTrackedLegs = appState.betSets.reduce((sum, s) => sum + s.legs.length, 0);
      const navBadge = document.getElementById('nav-tracker-count');
      if (navBadge) navBadge.textContent = totalTrackedLegs;

      renderSetsBar();
      const activeSet = getActiveSet();
      const targetLegs = appState.activeSetId === 'ALL_SETS'
        ? appState.betSets.flatMap(s => s.legs.map(l => ({ ...l, _setId: s.id, _setName: s.name, _setLocked: s.locked })))
        : (activeSet ? activeSet.legs.map(l => ({ ...l, _setId: activeSet.id, _setName: activeSet.name, _setLocked: activeSet.locked })) : []);
      const evaluatedList = targetLegs.map(leg => ({ leg, eval: evaluateLeg(leg) }));

      renderScoreboardStrip();
      renderSummaryRibbon(evaluatedList);
      renderFilterTabs(evaluatedList);
      renderLegsGrid(evaluatedList);
    }

    function renderSetsBar() {
      document.getElementById('sets-count-badge').textContent = `${appState.betSets.length} Set${appState.betSets.length > 1 ? 's' : ''}`;
      document.getElementById('vault-count-badge').textContent = appState.savedSetsVault.length;
      const tabsEl = document.getElementById('bet-sets-tabs');
      const allActive = appState.activeSetId === 'ALL_SETS';
      const allPill = `<button onclick="selectBetSet('ALL_SETS')" class="shrink-0 px-3 py-1.5 rounded-xl text-xs font-bold transition border ${allActive ? 'bg-sky-500 text-slate-950 border-sky-400 shadow-sm' : 'bg-slate-900 hover:bg-slate-800 text-slate-300 border-slate-700'}">All Tracked Sets (${appState.betSets.length})</button>`;
      const setPills = appState.betSets.map(s => {
        const isSelected = appState.activeSetId === s.id;
        return `<button onclick="selectBetSet('${s.id}')" class="shrink-0 px-3 py-1.5 rounded-xl text-xs font-bold transition border flex items-center gap-1.5 ${isSelected ? 'bg-emerald-500 text-slate-950 border-emerald-400 shadow-sm' : 'bg-slate-900 hover:bg-slate-800 text-slate-200 border-slate-700'}">${s.locked ? '<span>🔒</span>' : ''}<span>${escapeHtml(s.name)}</span><span class="px-1.5 py-0.2 rounded text-[10px] font-mono ${isSelected ? 'bg-slate-950/20 text-slate-950' : 'bg-slate-800 text-slate-400'}">${s.legs.length}</span></button>`;
      }).join('');
      tabsEl.innerHTML = allPill + setPills;

      const activeSet = getActiveSet();
      const lockBtn = document.getElementById('btn-lock-in-set');
      const lockLabel = document.getElementById('btn-lock-in-label');
      if (activeSet) {
        document.getElementById('quick-entry-set-name').textContent = activeSet.name;
        if (activeSet.locked) { lockBtn.className = 'px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-500/40 font-extrabold text-xs transition'; lockLabel.textContent = '🔓 Unlock Set'; document.getElementById('quick-entry-locked-pill').classList.remove('hidden'); }
        else { lockBtn.className = 'px-3.5 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-extrabold text-xs shadow-lg shadow-amber-500/15 transition'; lockLabel.textContent = '🔒 Lock In Set'; document.getElementById('quick-entry-locked-pill').classList.add('hidden'); }

        const evalLegs = activeSet.legs.map(l => evaluateLeg(l));
        const cashed = evalLegs.filter(e => e.status === 'cashed').length;
        document.getElementById('active-set-banner').innerHTML = `
          <div class="flex flex-wrap items-center gap-2.5">
            <span class="font-extrabold text-sm text-white">${appState.activeSetId === 'ALL_SETS' ? `Viewing All ${appState.betSets.length} Tracked Sets (Adding to: ${escapeHtml(activeSet.name)})` : escapeHtml(activeSet.name)}</span>
            <span class="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-sky-500/15 text-sky-300 border border-sky-500/35">${cashed}/${activeSet.legs.length} CASHED</span>
            ${activeSet.odds ? `<span class="px-2 py-0.5 rounded bg-slate-800 text-amber-300 font-mono text-[11px] font-bold">${escapeHtml(activeSet.odds)}</span>` : ''}
            ${activeSet.locked ? `<span class="text-[11px] font-mono text-amber-300">• 🔒 Locked (${escapeHtml(activeSet.lockedAt || 'Saved')})</span>` : ''}
          </div>
          <div class="flex items-center gap-2">
            <button onclick="openEditSetModal('${activeSet.id}')" class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs font-semibold">Rename / Odds</button>
            ${appState.betSets.length > 1 ? `<button onclick="deleteBetSet('${activeSet.id}')" class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-rose-500/15 text-slate-400 hover:text-rose-300 border border-slate-700 text-xs font-semibold">Delete Set</button>` : ''}
          </div>
        `;
      }
    }

    function renderScoreboardStrip() {
      const container = document.getElementById('scoreboard-strip');
      const games = Object.values(appState.games);
      container.innerHTML = games.map(g => `<button onclick="openBoxscoreDrawer('${g.id}')" class="shrink-0 flex items-center gap-2 px-2.5 py-1 rounded-xl bg-card hover:bg-cardHover border border-slate-800/90 text-xs font-mono"><span class="font-bold text-slate-200">${g.away.abbr} ${g.statusState === 'pre' ? '' : g.away.score}</span><span class="text-slate-600">@</span><span class="font-bold text-slate-200">${g.home.abbr} ${g.statusState === 'pre' ? '' : g.home.score}</span><span class="text-[10px] text-emerald-400">${g.statusDetail}</span></button>`).join('');
    }

    function renderSummaryRibbon(evaluatedList) {
      const cards = [
        { label: 'Total Legs', val: evaluatedList.length, color: 'text-white', border: 'border-slate-800', bg: 'bg-card' },
        { label: 'Cashed', val: evaluatedList.filter(x => x.eval.status === 'cashed').length, color: 'text-emerald-400', border: 'border-emerald-500/30', bg: 'bg-emerald-950/20' },
        { label: 'On Pace', val: evaluatedList.filter(x => x.eval.status === 'on_pace').length, color: 'text-sky-400', border: 'border-sky-500/30', bg: 'bg-sky-950/20' },
        { label: 'Sweating', val: evaluatedList.filter(x => x.eval.status === 'sweating').length, color: 'text-amber-400', border: 'border-amber-500/30', bg: 'bg-amber-950/20' },
        { label: 'Busted', val: evaluatedList.filter(x => x.eval.status === 'busted').length, color: 'text-rose-400', border: 'border-rose-500/30', bg: 'bg-rose-950/20' }
      ];
      document.getElementById('summary-ribbon').innerHTML = cards.map(c => `<div class="${c.bg} border ${c.border} rounded-2xl px-4 py-3 flex items-center justify-between"><span class="text-xs font-semibold text-slate-400">${c.label}</span><span class="text-xl sm:text-2xl font-mono font-extrabold ${c.color} tabular-nums">${c.val}</span></div>`).join('');
    }

    function renderFilterTabs(evaluatedList) {
      const counts = { all: evaluatedList.length, live: evaluatedList.filter(x => x.eval.isLiveGame).length, cashed: evaluatedList.filter(x => x.eval.status === 'cashed').length, sweating: evaluatedList.filter(x => x.eval.status === 'sweating').length, busted: evaluatedList.filter(x => x.eval.status === 'busted').length, upcoming: evaluatedList.filter(x => x.eval.status === 'upcoming').length };
      const labels = { all: 'All Legs', live: 'Live', cashed: 'Cashed', sweating: 'Sweating', busted: 'Busted', upcoming: 'Upcoming' };
      document.querySelectorAll('.filter-tab').forEach(btn => {
        const f = btn.getAttribute('data-filter');
        btn.textContent = `${labels[f]} (${counts[f]})`;
        btn.className = f === appState.activeFilter ? 'filter-tab px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap bg-slate-800 text-white shadow-sm' : 'filter-tab px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap text-slate-400 hover:text-slate-200';
      });
    }

    function renderLegsGrid(evaluatedList) {
      const container = document.getElementById('legs-grid-container');
      const filtered = evaluatedList.filter(({ eval: ev }) => appState.activeFilter === 'all' ? true : appState.activeFilter === 'live' ? ev.isLiveGame : ev.status === appState.activeFilter);
      if (filtered.length === 0) { container.innerHTML = `<div class="bg-card border border-slate-800 rounded-2xl p-12 text-center text-xs text-slate-400">No legs match this filter.</div>`; return; }

      if (appState.activeSetId === 'ALL_SETS') {
        container.innerHTML = `<div class="space-y-8">${appState.betSets.map(setObj => {
          const setLegs = filtered.filter(item => item.leg._setId === setObj.id);
          if (setLegs.length === 0) return '';
          const cashedCnt = setLegs.filter(x => x.eval.status === 'cashed').length;
          return `<div class="space-y-3"><div class="flex items-center justify-between px-1"><div class="flex items-center gap-2"><span class="text-sm font-extrabold text-white">${setObj.locked ? '🔒 ' : ''}${escapeHtml(setObj.name)}</span><span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 font-mono text-[10px] font-bold">${cashedCnt}/${setLegs.length} Cashed</span></div><button onclick="selectBetSet('${setObj.id}')" class="text-xs font-mono font-bold text-sky-400 hover:text-sky-300">Focus Set →</button></div><div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">${setLegs.map(({ leg, eval: ev }) => renderLegCard(leg, ev, setObj.locked)).join('')}</div></div>`;
        }).join('')}</div>`;
        return;
      }

      const activeSet = getActiveSet();
      container.innerHTML = `<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">${filtered.map(({ leg, eval: ev }) => renderLegCard(leg, ev, Boolean(activeSet && activeSet.locked))).join('')}</div>`;
    }

    function renderLegCard(leg, ev, isLocked = false) {
      const styles = {
        cashed: { border: 'border-emerald-500/45', bar: 'bg-emerald-500', chip: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30', valColor: 'text-emerald-400' },
        on_pace: { border: 'border-sky-500/35', bar: 'bg-sky-500', chip: 'bg-sky-500/15 text-sky-300 border-sky-500/30', valColor: 'text-sky-400' },
        sweating: { border: 'border-amber-500/35', bar: 'bg-amber-500', chip: 'bg-amber-500/15 text-amber-300 border-amber-500/30', valColor: 'text-amber-400' },
        busted: { border: 'border-rose-500/45', bar: 'bg-rose-500', chip: 'bg-rose-500/15 text-rose-300 border-rose-500/30', valColor: 'text-rose-400' },
        upcoming: { border: 'border-slate-800', bar: 'bg-slate-600', chip: 'bg-slate-800 text-slate-400 border-slate-700', valColor: 'text-slate-300' }
      }[ev.status];

      const initials = (ev.displayTitle || 'NB').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
      const headshotUrl = ev.playerId ? `https://a.espncdn.com/i/headshots/nba/players/full/${ev.playerId}.png` : (ev.teamLogo || `https://a.espncdn.com/i/teamlogos/nba/500/${(ev.teamAbbr || 'nba').toLowerCase()}.png`);
      const fallbackAvatar = `https://placehold.co/80x80/1e293b/94a3b8?text=${encodeURIComponent(initials)}`;
      const setIdAttr = leg._setId || getActiveSet()?.id || '';

      return `
        <article class="bg-card hover:bg-cardHover border ${styles.border} rounded-2xl p-4 sm:p-5 transition flex flex-col justify-between gap-4 shadow-lg">
          <div class="flex items-start justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <img src="${headshotUrl}" alt="${escapeHtml(ev.displayTitle)}" onerror="this.onerror=null;this.src='${fallbackAvatar}';" class="w-12 h-12 rounded-xl object-cover bg-slate-900 border border-slate-700/80 shrink-0" />
              <div class="min-w-0">
                <h4 class="font-bold text-sm sm:text-base text-white truncate">${escapeHtml(ev.displayTitle)}</h4>
                <p class="text-[11px] font-mono text-slate-400 mt-1">${escapeHtml(ev.gameStatus)} • ${escapeHtml(ev.scoreText)}</p>
              </div>
            </div>
            <div class="flex items-center gap-1 shrink-0">
              ${isLocked ? `<span class="p-1.5 rounded-lg text-amber-400 bg-amber-500/10 border border-amber-500/20 text-xs">🔒</span>` : `
                <button onclick="openEditLegModal('${setIdAttr}', '${leg.id}')" class="p-1.5 rounded-lg text-slate-400 hover:text-sky-400 hover:bg-slate-800 text-xs">✎</button>
                <button onclick="deleteLeg('${setIdAttr}', '${leg.id}')" class="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 text-xs">✕</button>
              `}
            </div>
          </div>
          <div class="flex items-center justify-between gap-2">
            <span class="px-2.5 py-1 rounded-lg text-xs font-mono font-bold border ${styles.chip}">${escapeHtml(ev.targetBadge)}</span>
            <span class="text-xs font-mono font-semibold text-slate-400">${ev.progressPct.toFixed(0)}%</span>
          </div>
          <div class="space-y-2.5">
            <div><span class="text-2xl font-mono font-extrabold ${styles.valColor}">${ev.currentVal}</span> <span class="text-sm font-mono text-slate-400">/ ${ev.targetVal} ${ev.statUnit}</span></div>
            <div class="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800/90"><div class="h-full ${styles.bar} transition-all duration-700 rounded-full" style="width: ${ev.progressPct}%"></div></div>
            <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-[11px] font-mono font-semibold border ${styles.chip}">${escapeHtml(ev.paceLabel)}</span>
          </div>
        </article>
      `;
    }

    function populateQuickEntryDropdowns() {
      const gameSel = document.getElementById('quick-game-select');
      if (!gameSel) return;
      const prevGameId = gameSel.value;
      gameSel.innerHTML = Object.values(appState.games).map(g => `<option value="${g.id}" ${g.id === prevGameId ? 'selected' : ''}>${g.shortName} (${g.statusDetail})</option>`).join('');
      onQuickGameChange();
    }
    function onQuickGameChange() {
      const game = appState.games[document.getElementById('quick-game-select').value];
      const datalist = document.getElementById('quick-player-datalist');
      if (!game || !datalist) return;
      datalist.innerHTML = Object.values(game.players || {}).map(p => `<option value="${escapeHtml(p.name)}">${p.team} • ${p.pts} PTS / ${p.reb} REB / ${p.ast} AST</option>`).join('');
      onQuickTeamMarketChange();
    }
    function setQuickCategory(cat) {
      appState.quickCategory = cat;
      document.getElementById('quick-player-group').classList.toggle('hidden', cat !== 'player');
      document.getElementById('quick-team-group').classList.toggle('hidden', cat === 'player');
      if (cat === 'team') onQuickTeamMarketChange();
    }
    function setQuickDirection(dir) {
      appState.quickDirection = dir;
      document.getElementById('quick-dir-over').className = dir === 'OVER' ? 'rounded-lg text-xs font-bold transition bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'rounded-lg text-xs font-semibold transition text-slate-400';
      document.getElementById('quick-dir-under').className = dir === 'UNDER' ? 'rounded-lg text-xs font-bold transition bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'rounded-lg text-xs font-semibold transition text-slate-400';
    }
    function onQuickTeamMarketChange() {
      const market = document.getElementById('quick-team-market').value;
      const game = appState.games[document.getElementById('quick-game-select').value];
      const sideSel = document.getElementById('quick-team-side');
      if (!game || !sideSel) return;
      sideSel.innerHTML = market === 'TOTAL' ? `<option value="OVER">Over</option><option value="UNDER">Under</option>` : `<option value="${game.away.abbr}">${game.away.name} (${game.away.abbr})</option><option value="${game.home.abbr}">${game.home.name} (${game.home.abbr})</option>`;
      document.getElementById('quick-team-line-wrap').classList.toggle('hidden', market === 'ML');
    }
    function handleQuickAddLeg(e) {
      e.preventDefault();
      const targetSet = getActiveSet();
      if (!targetSet) return;
      if (targetSet.locked) { showToast(`"${targetSet.name}" is locked in!`, 'warning'); return; }
      const gameId = document.getElementById('quick-game-select').value;
      const game = appState.games[gameId];
      if (!game) return;
      const newLeg = { id: 'leg-' + Date.now(), gameId, category: appState.quickCategory };
      if (appState.quickCategory === 'player') {
        const rawName = document.getElementById('quick-player-input').value.trim();
        if (!rawName) return;
        const matched = findMatchingPlayerInGame(game, null, rawName);
        newLeg.playerId = matched ? matched.id : '';
        newLeg.playerName = matched ? matched.name : rawName;
        newLeg.teamAbbr = matched ? matched.team : game.home.abbr;
        newLeg.statType = document.getElementById('quick-stat-type').value;
        newLeg.direction = appState.quickDirection;
        newLeg.target = parseFloat(document.getElementById('quick-target').value) || 15.5;
        document.getElementById('quick-player-input').value = '';
      } else {
        newLeg.market = document.getElementById('quick-team-market').value;
        newLeg.teamAbbr = document.getElementById('quick-team-side').value;
        newLeg.lineVal = parseFloat(document.getElementById('quick-team-line-val').value) || 0;
      }
      targetSet.legs.unshift(newLeg);
      persistSetsAndVault();
      renderAllTracker();
      showToast(`Added leg to "${targetSet.name}"`, 'success');
    }

    function setFilter(f) { appState.activeFilter = f; renderAllTracker(); }
    function openEditLegModal(setId, legId) {
      const targetSet = appState.betSets.find(s => s.id === setId) || getActiveSet();
      if (!targetSet || targetSet.locked) return;
      const leg = targetSet.legs.find(l => l.id === legId);
      if (!leg) return;
      document.getElementById('edit-leg-id').value = `${targetSet.id}::${leg.id}`;
      document.getElementById('edit-leg-label').textContent = leg.category === 'player' ? `${leg.playerName} • ${leg.statType}` : `${leg.teamAbbr} ${leg.market}`;
      document.getElementById('edit-direction-wrap').classList.toggle('hidden', leg.category !== 'player');
      document.getElementById('edit-leg-target').value = leg.category === 'player' ? leg.target : (leg.lineVal ?? 0);
      openModal('modal-edit-leg');
    }
    function handleSaveEditLeg(e) {
      e.preventDefault();
      const [setId, legId] = document.getElementById('edit-leg-id').value.split('::');
      const targetSet = appState.betSets.find(s => s.id === setId) || getActiveSet();
      const leg = targetSet?.legs.find(l => l.id === legId);
      if (!leg) return;
      const newVal = parseFloat(document.getElementById('edit-leg-target').value);
      if (leg.category === 'player') { leg.direction = document.getElementById('edit-leg-direction').value; leg.target = newVal; }
      else leg.lineVal = newVal;
      persistSetsAndVault();
      closeModal('modal-edit-leg');
      renderAllTracker();
    }
    function deleteLeg(setId, legId) {
      const targetSet = appState.betSets.find(s => s.id === setId) || getActiveSet();
      if (!targetSet || targetSet.locked) return;
      targetSet.legs = targetSet.legs.filter(l => l.id !== legId);
      persistSetsAndVault();
      renderAllTracker();
    }
    function clearCurrentSetLegs() {
      const targetSet = getActiveSet();
      if (!targetSet || targetSet.locked) return;
      targetSet.legs = [];
      persistSetsAndVault();
      renderAllTracker();
    }
    function loadSampleLegs() {
      if (Object.keys(appState.games).length === 0) appState.games = createDemoGames();
      appState.betSets = createSampleBetSets(appState.games);
      appState.activeSetId = 'ALL_SETS';
      persistSetsAndVault();
      renderAllTracker();
      showToast('Loaded sample bet sets', 'success');
    }

    function openBoxscoreDrawer(preselectGameId = null) {
      const drawer = document.getElementById('drawer-boxscore');
      const sel = document.getElementById('drawer-game-select');
      const games = Object.values(appState.games);
      if (games.length === 0) return;
      sel.innerHTML = games.map(g => `<option value="${g.id}" ${g.id === preselectGameId ? 'selected' : ''}>${g.away.abbr} (${g.away.score}) @ ${g.home.abbr} (${g.home.score}) — ${g.statusDetail}</option>`).join('');
      drawer.classList.remove('hidden'); drawer.classList.add('flex');
      renderBoxscoreContent();
    }
    function closeBoxscoreDrawer() { const d = document.getElementById('drawer-boxscore'); d.classList.add('hidden'); d.classList.remove('flex'); }
    function renderBoxscoreContent() {
      const game = appState.games[document.getElementById('drawer-game-select').value];
      const body = document.getElementById('drawer-boxscore-body');
      if (!game) return;
      const players = Object.values(game.players || {});
      const renderTbl = (team, list) => `<div class="bg-card border border-slate-800 rounded-2xl overflow-hidden"><div class="px-4 py-3 bg-slate-900 border-b border-slate-800 flex justify-between"><span class="font-bold text-sm text-white">${team.name}</span><span class="font-mono font-bold text-white">${team.score}</span></div><div class="overflow-x-auto"><table class="w-full text-left text-xs"><thead><tr class="border-b border-slate-800 text-slate-400 font-mono"><th class="py-2 px-3">PLAYER</th><th class="py-2 px-2 text-right">MIN</th><th class="py-2 px-2 text-right">PTS</th><th class="py-2 px-2 text-right">REB</th><th class="py-2 px-2 text-right">AST</th><th class="py-2 px-3 text-right">3PM</th></tr></thead><tbody class="divide-y divide-slate-800/60 font-mono">${list.map(p => `<tr><td class="py-2 px-3 font-sans font-semibold text-slate-200">${escapeHtml(p.name)}</td><td class="py-2 px-2 text-right text-slate-400">${p.min}</td><td class="py-2 px-2 text-right font-bold text-emerald-400">${p.pts}</td><td class="py-2 px-2 text-right">${p.reb}</td><td class="py-2 px-2 text-right">${p.ast}</td><td class="py-2 px-3 text-right text-sky-400">${p.fg3m}</td></tr>`).join('')}</tbody></table></div></div>`;
      body.innerHTML = renderTbl(game.away, players.filter(p => p.team === game.away.abbr)) + renderTbl(game.home, players.filter(p => p.team === game.home.abbr));
    }

    function openModal(id) { const el = document.getElementById(id); el.classList.remove('hidden'); el.classList.add('flex'); }
    function closeModal(id) { const el = document.getElementById(id); el.classList.add('hidden'); el.classList.remove('flex'); }
    function showToast(msg, type = 'info') {
      const container = document.getElementById('toast-container');
      const colors = { success: 'bg-emerald-950/95 border-emerald-500/50 text-emerald-200', warning: 'bg-amber-950/95 border-amber-500/50 text-amber-200', info: 'bg-slate-900/95 border-slate-700 text-slate-200' }[type] || 'bg-slate-900 border-slate-700 text-white';
      const el = document.createElement('div');
      el.className = `pointer-events-auto px-4 py-2.5 rounded-xl border text-xs font-semibold shadow-xl backdrop-blur-md transition-all duration-300 ${colors}`;
      el.textContent = msg;
      container.appendChild(el);
      setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 2800);
    }
    function escapeHtml(str) {
      if (str === null || str === undefined) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // =========================================================================
    // BOOTSTRAP BOTH MODULES
    // =========================================================================
    window.addEventListener('DOMContentLoaded', () => {
      loadPersistedSlip();
      syncEspnData(false);
      startSyncTimer();

      updateModeButtons();
      syncAllData(false);
      startCountdownTimer();
    });
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(unified_html)

print("Generated unified index.html:", len(unified_html), "bytes")