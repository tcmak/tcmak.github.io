\# System Architecture 🏗️

This project is deliberately designed with a "Single-File Architecture" to maximize compatibility with AI-assisted "Vibe Coding" and zero-configuration deployment via GitHub Pages.

\#\# 1\. Technical Stack  
\*   \*\*Frontend HTML:\*\* Provides the canvas container and basic UI overlays.  
\*   \*\*Styling (CSS):\*\* Inline or unified within a \`\<style\>\` tag. Manages the retro pixel-art aesthetic, SEN-friendly fonts, and responsive canvas scaling.  
\*   \*\*Logic (Vanilla JS):\*\* All game logic, physics, and state management are contained within a single \`\<script\>\` block. No build tools (Webpack, Vite, npm) are required.  
\*   \*\*Deployment:\*\* Static hosting on GitHub Pages.

\#\# 2\. Core Game Loop  
The engine relies on the browser's native \`requestAnimationFrame\` API for smooth 60 FPS rendering.  
\*   \`init()\`: Bootstraps the game, loads saved state from \`localStorage\`, and sets up event listeners.  
\*   \`update(dt)\`: Calculates delta-time. Updates physics (gravity, velocity), handles collision detection (AABB \- Axis-Aligned Bounding Box), and updates entity states.  
\*   \`draw(ctx)\`: Clears the canvas and redraws the background, tiles, entities (player, letters), and UI based on the updated state.

\#\# 3\. Entity Management  
Instead of a complex Entity-Component-System (ECS), the game uses simple JavaScript classes/objects:  
\*   \`Player\`: Manages position, velocity, jump state, and collision boundaries.  
\*   \`World\`: A 2D array (Grid) representing the level structure. Handles tile rendering and solid ground collision.  
\*   \`Block\`: Interactive tiles (like the Mario question blocks) that trigger events when struck from below.  
\*   \`LetterDrop\`: Physics-enabled entities that spawn from hit blocks and can be collected by the player.

\#\# 4\. State Management & Persistence  
The game maintains a dual-state system to handle the two distinct gameplay modes:  
1\.  \*\*Platformer State:\*\* Tracks the current target word, collected letters, and active physics entities.  
2\.  \*\*Sandbox State:\*\* Tracks the player's inventory of earned blocks and a separate 2D array representing the custom sandbox world.

\*\*Storage Module:\*\*  
A lightweight wrapper around \`localStorage\` ensures that the child's hard work (sandbox creations) and rewards (inventory) survive browser reloads.  
\`\`\`javascript  
const GameStorage \= {  
    save: (key, data) \=\> localStorage.setItem(\`swb\_${key}\`, JSON.stringify(data)),  
    load: (key) \=\> JSON.parse(localStorage.getItem(\`swb\_${key}\`))  
};  
\`\`\`

\#\# 5\. Input Handling  
\*   \*\*Keyboard:\*\* Listens for \`keydown\` and \`keyup\` events to control player movement and jumping.  
\*   \*\*Mouse/Touch:\*\* Listens for \`click\` or \`pointerdown\` events, translating screen coordinates to grid coordinates for placing blocks in Sandbox Mode.  


## 6. Audio Architecture 🔊
* **Web Audio Synthesis (`SoundFX`):** Procedural 8-bit sound effects (jump, block hit, correct chime, incorrect boop, victory fanfare) built using browser native Web Audio API oscillators and gain envelopes without external asset dependencies.
* **Speech Synthesis:** Uses browser `speechSynthesis` with lowercase text normalization so whole words are spoken aloud clearly.
* **Mute Control:** State `soundEnabled` gates all audio generators. Toggled via UI button and `M` key, persisted under `swb_sound_enabled`.

## 7. Sandbox Recycling Architecture ♻️
* **Individual Block Recycling:** Clicking or right-clicking placed green blocks invokes `recycleSandboxBlockAt()`, removing the tile from `world` and incrementing `inventoryBlocks` (+1 refund).
* **Bulk Recycling:** `recycleAllSandboxBlocks()` queries all active sandbox blocks, safely removes them from grid, and refunds the total count to inventory.

Full playtest feature specifications and regression guidelines are documented in [FEATURES.md](FEATURES.md).
