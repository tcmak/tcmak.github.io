# MarioCraft Feature Specification & Playtest Requirements 📜

This document is the permanent single source of truth for all user-requested gameplay features, design constraints, and accessibility requirements in **MarioCraft Spelling Adventure**. All future iterations and AI pair-programming agents MUST preserve and respect every requirement detailed below.

---

## 1. Character & Movement
* **Character Model:** Authentic Minecraft Strider avatar featuring blocky crimson body, spiky side hair strands, animated wobbly legs during motion, and directional pupils facing the direction of movement.
* **Hard Boundary Enforcement:** Strict horizontal boundaries (`0 <= x <= canvas.width - player.width`). The character CANNOT walk off-screen or disappear; movement is firmly blocked at both borders.
* **Platforming Physics:**
  * Gravity: `1200 px/s²`
  * Jump Force: `-460 px/s` (peak jump reaches ~88px high)
  * Coyote Time: 150ms grace window after walking off ledges.
  * Jump Buffering: 150ms input buffer when pressing jump before landing.

---

## 2. Treasure Blocks (❓ Question Blocks) & Dynamic Relocation
* **Head Clearance & Run-Under:**
  * Question blocks MUST be positioned at heights with full clearance (`rows - 5` or `rows - 6`), providing 64px–96px clearance above the ground floor.
  * Because Strider is 34px tall, it can freely run underneath all blocks without getting stuck horizontally.
* **Smashed & Pop Letters:**
  * Jumping into a treasure block from below hits/smashes it.
  * Spawns floating letter entities popping outward in wide parabolic arcs (`vx = 140..220 px/s`) so the player must walk over and collect the right letter.
  * Generates golden particle explosion effects.
* **Dynamic Relocation:**
  * When smashed, the treasure block vanishes from its current grid position.
  * A replacement treasure block IMMEDIATELY appears at another random, reachable location (`rows - 5` or `rows - 6`).
  * Spawns golden sparkle appear particles at the new location.

---

## 3. Green Blocks & Sandbox Mode Recycling
* **Dual-Mode System:**
  * Toggled via `Tab` key or the **Switch to Sandbox / Spelling Mode** button.
* **Block Placement:**
  * In Sandbox Mode, clicking an empty grid tile places a green block (`inventoryBlocks--`).
* **Individual Block Removal & Recycling:**
  * In Sandbox Mode, clicking or right-clicking on an existing green block immediately removes it and refunds `+1` block back into inventory.
  * Hovering over an existing green block shows a red recycle highlight to indicate it can be clicked to remove.
* **Bulk Clearing & Full Recycling:**
  * In Sandbox Mode, a dedicated **♻️ Recycle All Blocks** button is available in the controls panel.
  * Clicking it removes all placed sandbox blocks from the world and refunds all of them back into the block inventory count.
* **Spelling Mode Smashing:**
  * In Spelling Mode, jumping into a green block from below smashes it with green particle effects and refunds `+1` block into inventory.

---

## 4. Vocabulary Progression (Oxford 3000)
* **Comprehensive Dictionary:** Contains 3,155 official Oxford 3000 words ranging from 3-letter to 10-letter words with definitions, emojis, and categories.
* **Randomized Word Selection:**
  * Words do NOT start with "ACT" every time. Starting the game or restarting picks a random word from the 3-letter pool.
  * Avoids immediate repetition by tracking played words in the current tier.
* **Progressive Word Length Tiers:**
  * Players complete **4 words** of a given length before automatically advancing to the next length tier ($3 \rightarrow 4 \rightarrow 5 \rightarrow 6 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 10$ letters).
  * Clue header dynamically indicates progress: e.g. `💡 WORD CLUE (Animals) - 3-Letter Words (1/4)`.
* **Speech Text Normalization:**
  * Words are normalized to lowercase strings so SpeechSynthesis pronounces them as real words (e.g. "act" and "add"), not spelled-out letters ("A-C-T").

---

## 5. Audio & Sound Control
* **Sound Effects (Web Audio API):**
  * Jump sound (rising square wave)
  * Block hit / smash sound (triangle wave)
  * Correct letter sound (arpeggio chime)
  * Incorrect letter boop (descending sawtooth)
  * Victory fanfare (multi-tone chord)
* **Speech Synthesis:**
  * Automatic pronunciation at the start of every new word.
  * Manual pronunciation via the **🔊 Speak Word** button.
* **Sound Toggle (Mute / Unmute):**
  * Prominent **🔊 Sound: ON / 🔇 Sound: OFF** toggle button in the top bar.
  * Keyboard shortcut: `M` key toggles sound on/off.
  * Mutes all Web Audio oscillators and SpeechSynthesis output.
  * Sound preference is persisted in `localStorage`.

---

## 6. Layout & Playable Area Alignment
* **Unified Cabinet Alignment:**
  * `#game-container` is constrained to `max-width: 800px; width: 100%; align-items: stretch;`.
  * The playable area `<canvas>` is styled to `width: 100%; aspect-ratio: 800 / 448;` with continuous 2px border matching the top header, hint panel, and bottom controls panel.
  * The top panels, playable canvas, and bottom panels are perfectly flush and aligned.
* **Mouse Coordinate Scaling:**
  * Canvas mouse event listeners scale client coordinates by `canvas.width / rect.width` and `canvas.height / rect.height` so clicking and placing blocks in Sandbox Mode remains pixel-accurate at all display resolutions.

---

## 7. Persistence & Game State
* **`localStorage` Keys:**
  * `swb_game_state`: Contains `inventoryBlocks`, `wordsCompletedCount`, `totalScore`, `currentTierLength`, `tierWordsCompleted`, `currentWord`, and `sandboxBlocks` grid coordinates.
  * `swb_sound_enabled`: Stores boolean audio state (`true` / `false`).
* **Game Reset:**
  * **🔄 Restart Game** button with confirmation prompt clears saved state and restarts with a new random 3-letter word.

---

## 8. Built-in Automated Unit Test Suite
* Executed automatically by appending `?test=true` to the URL.
* Tests physics, audio initialization, dictionary length, letter spawning, boundary blocking, treasure block relocation, word length progression, sandbox recycling, and persistence.
