\# Super Word Blocks 🧱🍄

A lightweight, zero-dependency educational web game combining Mario-style platforming with Minecraft-style sandbox building. Designed to help children with learning difficulties (such as dyslexia) practice spelling and simple sentence construction in a low-stress, highly rewarding environment.

\#\# 🎯 Vision  
To provide a "vibe-coded", easily modifiable game that runs directly in the browser via GitHub Pages. No backend, no build steps—just pure HTML, CSS, and Vanilla JS in a single file or minimal structure.

\#\# 🚀 Getting Started

Since this is a static architecture, setup is instant:

1\. \*\*Clone or Download:\*\* Pull the repository to your local machine.  
2\. \*\*Run Locally:\*\* Simply double-click \`index.html\` to open it in any modern browser (Chrome, Firefox, Safari).  
3\. \*\*Deploy:\*\* Push the \`main\` branch to GitHub and enable \*\*GitHub Pages\*\* (Settings \> Pages \> Deploy from a branch). The game will be live instantly.

## 🎮 Controls  
*   **A / D** or **Left / Right Arrows**: Move Strider character  
*   **Spacebar / W / Up Arrow**: Jump / Hit block  
*   **Tab**: Toggle between Platformer (Spelling) Mode and Sandbox (Building) Mode  
*   **M**: Toggle Sound On / Off  
*   **Left Click (Sandbox Mode)**: Place green block on empty tile / Click existing block to remove & recycle  
*   **Right Click (Sandbox Mode)**: Remove green block & recycle back into inventory  
*   **Recycle Button (Sandbox Mode)**: Clear all placed green blocks at once and refund full inventory

Detailed feature requirements are documented in [FEATURES.md](file:///home/user/mariocraft/FEATURES.md).

\#\# 🧠 SEN-Friendly Features  
\*   \*\*High Contrast & Readability:\*\* Utilizes large, sans-serif fonts (or OpenDyslexic) to prevent letter confusion (e.g., b/d, p/q).  
\*   \*\*Zero Punishment:\*\* No "game over" screens or life deductions for spelling mistakes. Incorrect letters simply bounce away.  
\*   \*\*Visual Grouping:\*\* Vowels and consonants are color-coded to help visual decomposition of words.  
\*   \*\*Pacing:\*\* Simple 2D horizontal scrolling reduces the motion sickness or spatial disorientation sometimes caused by full 3D environments.

\#\# 🛠️ Architecture Overview  
\*   \*\*Framework:\*\* 100% Vanilla JavaScript (HTML5 Canvas).  
\*   \*\*Storage:\*\* Client-side \`localStorage\` for persistent inventory (earned blocks) and sandbox world state.  
\*   \*\*Hosting:\*\* GitHub Pages (Static frontend hosting).  

## 🧪 Running Tests
You can run the full automated unit test suite (54 assertions across 27 categories) in three easy ways:

1. **In-Game Button**: Click the **🧪 Run Tests** button at the bottom of the game screen.
2. **Browser URL**: Open `index.html?test=true` in your browser.
3. **Terminal / CLI**: Run `node test.js` in the project folder.

Detailed test specs and coverage matrices can be found in [test_plan.md](test_plan.md).
