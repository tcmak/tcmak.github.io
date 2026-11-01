# Test Plan 🧪 (TDD Approach)

To maintain our zero-dependency, single-file architecture, we do not introduce heavy testing frameworks (like Jest or Mocha). Instead, we decouple game logic from the Canvas rendering API and embed a built-in automated test runner directly in `index.html`.

By appending `?test=true` to the URL (e.g. `index.html?test=true`), or by running the script headlessly via Node.js during development, all automated unit tests execute immediately and report pass/fail status in `#unit-test-report`.

---

## 🎯 Test Coverage Matrix for Documented Features

Every requirement documented in [FEATURES.md](FEATURES.md) is covered by explicit unit tests:

| Feature Area | Documented Requirement | Automated Test in `index.html` |
| :--- | :--- | :--- |
| **Audio Engine** | AudioContext and oscillator sound synthesis initializes properly | **Test 1:** SoundFX AudioContext instantiation |
| **Vocabulary** | Full Oxford 3000 vocabulary dictionary loaded (3,155 words) | **Test 2:** Dictionary length and initial word length verification |
| **Screen & Cabinet** | Canvas initialized to standard 800x448 resolution | **Test 3:** Canvas 800x448 dimension verification |
| **Boundaries** | Hard left and right screen borders block Strider movement | **Test 4:** Boundary blocking at `x = 0` and `x = canvas.width - player.width` |
| **Letter Popping** | Hitting block spawns floating letters with parabolic velocity | **Test 5:** Letter spawn count and parabolic arc velocity (`140..220 px/s`) |
| **Letter Collection** | Matching letter fills word slot; wrong letter fades | **Test 6:** Correct letter matching in `spelledWord` array |
| **Speech Normalization** | Whole words pronounced cleanly without letter-by-letter spelling | **Test 7:** Speech synthesis text normalization test with lowercase word |
| **Clue Display** | Word clue, definition, and emoji displayed at word start | **Test 8:** Immediate hint unlocked status on new word |
| **Scoring & Rewards** | Word completion awards points (`length * 100`) and increments count | **Test 9:** Score calculation and completed words increment |
| **Game Modes** | Mode toggles cleanly between Spelling and Sandbox (`Tab`) | **Test 10:** Dual-state game mode toggling |
| **Sandbox Placement** | Placing block adds to grid and decrements inventory | **Test 11:** Sandbox block placement and inventory decrement |
| **Persistence** | `GameStorage` saves and loads state from `localStorage` | **Test 12:** GameStorage JSON serialization and retrieval |
| **Platforming Physics** | Coyote Time allows jumping 150ms after leaving ground | **Test 13:** Coyote time mid-air jump execution |
| **Jump Buffering** | Input buffering preserves jump command before landing | **Test 14:** Jump buffer timer retention |
| **Treasure Relocation** | Smashed question block disappears and reappears at new reachable spot | **Test 15:** Old position cleared, new block created at `rows - 5` or `rows - 6` |
| **Tier Progression** | Completing several words of length $N$ advances to length $N+1$ | **Test 16:** Word length tier advancement after `WORDS_PER_TIER` completions |
| **Layout Alignment** | Playable area canvas width aligns flush with top and bottom panels | **Test 17:** Container and canvas width alignment |
| **Audio Toggle** | Sound toggle button and `M` key switch mute state and persist | **Test 18:** Sound toggle state inversion and toggle back |
| **Block Removal** | Clicking or right-clicking green block removes it and refunds +1 | **Test 19:** Individual sandbox block removal and inventory refund |
| **Bulk Recycling** | "Recycle All Blocks" button clears all placed blocks and refunds total | **Test 20:** Bulk recycling tile clearing and full inventory restitution |
| **Head Clearance** | Question block heights allow Strider (34px) to freely run under | **Test 21:** Head clearance verification for rows `rows - 5` and `rows - 6` |
| **Audio Muting Gating** | When sound is muted, speech synthesis and SFX are suppressed | **Test 22:** Speech synthesis call suppression when `soundEnabled === false` |
| **Word Randomization** | Random selection draws varied words from pool (doesn't repeat ACT) | **Test 23:** Multi-sample uniqueness verification from 3-letter word pool |
| **Visual Grouping** | Vowels and consonants correctly classified for SEN visual grouping | **Test 24:** `isVowelChar` classification for all vowels and consonants |
| **Full Tier Cycle** | Tier progression traverses lengths 3 through 10 and wraps to 3 | **Test 25:** Complete 3..10 length progression traversal loop |
| **State Persistence** | Sound preference and game progress persist across reloads | **Test 26:** `swb_sound_enabled` persistence in `GameStorage` |
| **Targeted Recycling** | Recycling function validates tile type and ignores non-sandbox tiles | **Test 27:** `recycleSandboxBlockAt` boundaries and invalid tile rejection |

---

## 🏃 Running Tests

1. **Browser Test Runner:**  
   Open `index.html?test=true` in any browser. The built-in test suite executes synchronously, and `#unit-test-report` displays all passed assertions in green.
2. **Headless Execution (Node.js):**  
   Run the embedded script with Node.js to verify all 27 test sections and 53 assertions pass before publishing changes.
