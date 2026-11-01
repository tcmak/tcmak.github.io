# Development Plan 🗓️

This project embraces a "Vibe Coding" approach. Instead of traditional, heavy software engineering sprints, development is broken down into promptable milestones. Each phase represents a chunk of functionality that can be easily fed into an AI code generator (like Claude or ChatGPT) to iteratively build the `index.html` file.

## Phase 1: Foundation & Physics (The Mario aspect)  
**Goal:** Establish the basic game engine and character controller using HTML5 Canvas.  
*   [x] **Canvas Setup:** Initialize a standard HTML5 `<canvas>` element with a fixed aspect ratio and responsive scaling.  
*   [x] **Game Loop:** Implement a robust `requestAnimationFrame` loop to handle updates and rendering.  
*   [x] **Player Physics:** Add gravity, horizontal movement, and jumping mechanics.  
*   [x] **Basic Collision:** Create static "ground" tiles and ensure the player can stand on them without falling through.  
*   [x] **Block Interaction:** Implement floating blocks that the player can hit from below. Add a simple bounce animation when a block is hit.

## Phase 2: Educational Loop (The Spelling aspect)  
**Goal:** Introduce the learning mechanics and visual rewards.  
*   [x] **Target Word UI:** Display a target word (e.g., "C A T") at the top of the screen with empty slots for missing letters.  
*   [x] **Letter Drops:** Modify hit blocks to spawn moving entities (letters) that fall to the ground.  
*   [x] **Collection Logic:**   
    *   If the player touches the *correct* letter, it fills the slot in the Target Word UI.  
    *   If the player touches an *incorrect* letter, it plays a soft "boop" sound and fades away (Zero punishment).  
*   [x] **Reward Trigger:** Upon completing a word, trigger a visual celebration and add a "Luminous Building Block" to the player's inventory.

## Phase 3: Creative Reward (The Minecraft aspect)  
**Goal:** Implement the sandbox building mode and persistence.  
*   [x] **Mode Toggle:** Add a UI button (or keyboard shortcut like `Tab`) to switch between "Spelling Mode" and "Sandbox Mode".  
*   [x] **Inventory UI:** Display the number of earned building blocks available for use.  
*   [x] **Grid Placement:** In Sandbox Mode, allow the player to use their mouse to click and place blocks on a fixed grid.  
*   [x] **State Persistence:** Implement `localStorage` to save both the current inventory count and the layout of the blocks placed in the Sandbox.

## Phase 4: SEN Optimization & Polish  
**Goal:** Refine the experience for children with learning difficulties.  
*   [x] **Typography & Colors:** Ensure all text uses high-contrast, sans-serif fonts. Color-code vowels and consonants on the dropped letters.  
*   [x] **Sound Design:** Add non-intrusive, positive reinforcement sound effects (e.g., retro 8-bit sounds for jumping, collecting, and completing words).  
*   [x] **Pacing:** Fine-tune the player's movement speed and the falling speed of letters to reduce cognitive load and prevent frustration.  
*   [x] **Playtesting:** Test with the target audience (your child) and iterate based on their feedback.

## Phase 5: Gameplay Enhancements & Oxford 3000 Integration 🚀  
**Goal:** Implement playtest feedback to maximize engagement, accessibility, and vocabulary depth.  
*   [x] **Minecraft Strider Character Model:** Replaced character with an authentic, animated Minecraft Strider (blocky crimson body, spiky hair strands, directional eyes, wobbly legs).  
*   [x] **Immediate Word Clue & Picture Display:** Display the picture emoji and category clue in the hint panel immediately when a new word starts.  
*   [x] **Smashable Green Blocks:** Striking green sandbox blocks from underneath smashes them with particle effects and refunds +1 building block.  
*   [x] **Wider Parabolic Letter Pop Arcs:** Letters pop outward in wider parabolic arcs (`vx = 140..220 px/s`) across the floor, requiring Strider to walk over and choose the correct letter.  
*   [x] **Restart Game Button:** Added a `🔄 Restart Game` button to clear `localStorage` and reset progress back to the first word (`CAT`).  
*   [x] **Hard Screen Boundary Blocking:** Replaced infinite wrapping with strict border limits (`0 <= x <= canvas.width - player.width`) so Strider can never disappear off screen.  
*   [x] **Extra Large & Clear Target Word UI:** Enlarged target word boxes to 54x54px with 34pt font and a prominent dark navy/gold border panel for maximum visual clarity.  
*   [x] **Adjusted Block Heights & Clearance:** Positioned floating question blocks at `rows - 4` and `rows - 5` (64px - 96px clearance above ground) so the character can freely run underneath without horizontal blockage.  
*   [x] **Expanded Oxford 3000 Dictionary Progression:** Integrated all 3,156 official words from the Oxford 3000 wordlist (3-letter to 10-letter words: ACT, CAT, DOG, STAR, FROG, BANANA, ELEPHANT, UNIVERSITY, VOCABULARY), strictly sorted by length so players progress continuously through all tiers without looping early.  
*   [x] **Score Keeping:** Track and display total score and total words claimed (`🏆 Words: X  ⭐ Score: Y`) with persistent `localStorage`.

## Phase 6: Playtest Polish & Layout Alignment 🎯
**Goal:** Address player feedback regarding treasure block relocation, vocabulary randomization/progression, and visual layout alignment.
*   [x] **Dynamic Treasure Block Respawning:** Smashed treasure/question blocks explode into golden particle bursts, vanish, and dynamically reappear at a new random, reachable location (`rows - 5` or `rows - 6`) with full running clearance underneath.
*   [x] **Word Randomization & Length Progression:** Randomized words within each word length pool (no longer always starting with "ACT"). After completing several words of that length (4 words per tier), the game dynamically advances to the next length tier (3 -> 4 -> 5 -> ... -> 10 letters).
*   [x] **Playable Area Width Alignment:** Aligned the playable area canvas edge-to-edge with the top headers, hint panels, and bottom control panels (`max-width: 800px; width: 100%`) creating a flush arcade frame cabinet design with scaled sandbox mouse placement.

## Phase 7: Audio Control & Sandbox Recycling 🔊♻️
**Goal:** Implement audio toggle controls and complete sandbox block recycling tools.
*   [x] **Feature Specification & Regression Prevention:** Documented all playtest requirements in `FEATURES.md` to preserve all game mechanics across future iterations.
*   [x] **Sound Toggle (Mute/Unmute):** Added a prominent `🔊 Sound: ON / 🔇 Sound: OFF` button and `M` keyboard shortcut to mute/unmute both Web Audio SFX and SpeechSynthesis. Persisted in `localStorage`.
*   [x] **Sandbox Block Removal & Recycling:** In Sandbox Mode, clicking or right-clicking placed green blocks removes them and refunds `+1` block to inventory, with hover preview highlight.
*   [x] **Bulk Sandbox Recycle Button:** Added a `♻️ Recycle All Blocks` button in Sandbox Mode to clear all placed blocks at once and refund them into the inventory count.
