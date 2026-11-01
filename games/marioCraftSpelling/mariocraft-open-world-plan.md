# MarioCraft Spelling Adventure — Open-World Build Plan

## Context

The game is currently a single HTML+JS file: one fixed screen, a flat ground row,
a handful of floating `?` boxes for the *current* word (shown as "X-LETTER WORDS
(n/4)"), a Spelling Mode and a separate Sandbox Mode, a Blocks counter, and a
Run Tests button. We're converting it into a persistent, non-level, Minecraft-flavoured
open world: no "beat the level," a looping side-scrolling world, terrain you
have to climb or build across, and two enemy types.

Before starting Phase 0, read the current source end to end. The phases below
*extend* today's mechanics (box → pop letter → fill blank; Sandbox block
placement; Run Tests) — they don't replace them unless a phase says so.

## How to use this document (for the AI agent)

1. Find the first unchecked phase in **Status** below. Implement only that phase.
2. Check off each task inside the phase as you finish it, not just the phase
   heading at the end — a fresh session needs to see partial progress.
3. Extend the test suite and the save format per **Cross-cutting requirements**
   before considering the phase done.
4. Confirm the phase's **Playable state** is actually true by walking through
   it, then check off the phase heading in Status and commit.
5. If you stop before a phase is finished (token/context limit, error, etc.),
   leave finished sub-tasks checked, leave the phase heading unchecked, and add
   one line to **Handoff notes** saying exactly where you stopped and what the
   next concrete step is. Do not start the next phase early to "make progress"
   — an unfinished phase in a half-working state is worse than a finished
   earlier one.

## Cross-cutting requirements (apply to every phase, not repeated below)

- Extend the automated tests behind "Run Tests" to cover whatever the phase
  added. Don't let existing coverage regress.
- Extend the localStorage save/load format for any new persistent state the
  phase introduces. Add a `saveVersion` field and load older saves gracefully
  (default any field that's missing) rather than breaking existing saves.
- The game must be fully playable end to end after every phase — no
  half-wired mechanic left in a broken state.
- Commit (or otherwise checkpoint) at the end of each phase, before starting
  the next one.

## Design decisions locked in (flag before changing, don't silently re-decide)

- The world is one continuous loop, not discrete levels.
- Loop point: walking past `x = WORLD_WIDTH` wraps to `x = 0`. Walking left
  from `x = 0` is blocked by a wall — you can't shortcut backward around the
  loop to skip ahead.
- `WORLD_WIDTH = 8000` tiles, `~100` tiles per word on average (80 words).
  Adjust if the pacing feels wrong once playable.
- All 80 words are placed once along the loop, keeping the existing
  word-length groupings as contiguous neighbourhoods (so difficulty still
  ramps with distance). Any cluster is completable whenever you reach it — no
  gating by order. A global "Words solved: X/80" counter replaces "(n/4)".
- Sandbox Mode stays as an unlimited/no-cost creative toggle for debugging.
  The main mode gets its own block placement tied to the real Blocks counter.
- Enemies disrupt (knockback, letter loss) but never end the run — no
  lives/game-over system.
- World edits and word progress persist via localStorage. Enemy positions do
  not need to persist — they respawn fresh on load.

## Status

- [x] Phase 0 — World foundation: coordinates, camera, scrolling
- [ ] Phase 1 — Seamless world looping
- [ ] Phase 2 — Distribute all 80 words; free-order completion
- [ ] Phase 3 — Terrain variety + fall handling
- [ ] Phase 4 — Blocks as a building tool
- [ ] Phase 5 — Decoy letters
- [ ] Phase 6 — Base enemy framework
- [ ] Phase 7 — Enemy: Muncher (eats floor letters)
- [ ] Phase 8 — Enemy: Thief (steals collected letters)
- [ ] Phase 9 (optional) — Polish pass

## Handoff notes

- 2026-09-26: Phase 0 completed and verified with all 34 automated unit test suites passing (72 assertions). Coordinates, camera, sparse store Map, viewport culling, and saveVersion 1 implemented. Ready for Phase 1.

---

## Phase 0 — World foundation: coordinates, camera, scrolling

**Depends on:** nothing.
**Goal:** replace the fixed single-screen layout with a scrollable
coordinate-based world, no gameplay regressions.

Tasks:
- [x] Introduce a tile coordinate system (`TILE_SIZE`, integer tile x/y) and a
      sparse store (`Map<"x,y", TileData>`) for anything that isn't plain
      ground — don't allocate storage for empty tiles.
- [x] Add `camera.x` that follows the player (lead/deadzone is fine); render
      only tiles within the viewport plus a 1-tile buffer each side.
- [x] Move player physics (position, velocity, gravity, jump) into world
      coordinates instead of screen coordinates.
- [x] Re-anchor the existing per-word box logic to world coordinates: place
      the current word's boxes near the player's start position. Behaviour
      should look identical to today, just camera-scrollable.
- [x] Define `WORLD_WIDTH = 8000` as a constant (unused elsewhere yet).
- [x] Temporarily place one dummy box cluster far to the right, confirm you
      can walk to it and the camera follows — then remove the dummy.

**Playable state:** identical to today's game, except the camera can scroll.
**Do not build yet:** looping, terrain variety, multiple live words.

---

## Phase 1 — Seamless world looping

**Depends on:** Phase 0.
**Goal:** the world wraps at its east edge without a visible seam, and can't
be shortcut by walking backward from the start.

Tasks:
- [ ] On update, when `player.x >= WORLD_WIDTH`, subtract `WORLD_WIDTH` from
      both `player.x` and `camera.x` — preserve velocity and all other state.
- [ ] Add a hard collider at `x = 0` blocking leftward movement past it.
- [ ] Fix seam rendering: when the viewport spans past `WORLD_WIDTH`, also
      draw tiles from `x - WORLD_WIDTH` so the wrap has no visible pop or
      flicker.
- [ ] Manually confirm: run right continuously for the full width and land
      back at the start seamlessly.

**Playable state:** can run in one direction indefinitely and loop back
seamlessly; can't sneak backward past `x = 0`.
**Do not build yet:** the real 80-word layout (still Phase 0's dummy/placeholder).

---

## Phase 2 — Distribute all 80 words; free-order completion

**Depends on:** Phase 1.
**Goal:** all 80 words exist somewhere in the loop, completable in any order.

Tasks:
- [ ] Lay out all 80 words' box clusters across the 8000 tiles, keeping
      existing word-length groups as contiguous neighbourhoods.
- [ ] Replace the "(n/4)" within-group index with a global "Words solved:
      X/80" indicator.
- [ ] Change box-hit resolution so a box always resolves against the word
      it's tagged with, not one single global "current word" — any cluster
      is completable whenever reached.
- [ ] Update the clue panel to show the clue for whichever cluster the player
      is nearest to (or last interacted with).
- [ ] Extend the save format to persist `solvedWords` (set/array of word IDs).

**Playable state:** can walk to several different word clusters in any order
and complete them; solved count persists across reloads.
**Do not build yet:** terrain obstacles, enemies.

---

## Phase 3 — Terrain variety + fall handling

**Depends on:** Phase 2.
**Goal:** varied terrain exists and falling doesn't soft-lock the player.

Tasks:
- [ ] Add terrain types: pit (no ground, fall through), raised step
      (multi-height ground), floating platform (isolated, nothing below),
      pipe (solid decorative obstacle).
- [ ] Track the last x position where the player was on solid ground; if the
      player falls below a death plane, respawn them there.
- [ ] Add terrain variety to some (not all) word neighbourhoods — keep early
      clusters easy, ramp difficulty with distance.
- [ ] Reposition a subset of existing boxes onto platforms/steps reachable
      only with careful jumping (not yet requiring built blocks).

**Playable state:** varied terrain across the world; falling into a pit
respawns you sensibly; some boxes now require real jump timing.
**Do not build yet:** boxes that are *unreachable* without building — that's
Phase 4. For now, everything should be reachable by jumping alone.

---

## Phase 4 — Blocks as a building tool

**Depends on:** Phase 3.
**Goal:** the Blocks counter becomes a real resource used to reach places.

Tasks:
- [ ] Enable placing/removing a block in the main game mode (not just
      Sandbox), consuming/refunding the existing Blocks counter.
- [ ] Keep Sandbox Mode unchanged as a free creative/debug toggle.
- [ ] Add a few boxes/clusters unreachable by jumping alone — require
      stacking blocks into a staircase, or bridging a gap.
- [ ] Extend the save format to persist placed/removed blocks (reuse the
      Phase 0 sparse tile store).

**Playable state:** some boxes are unreachable until you spend Blocks to
build a staircase or bridge to them; the counter updates and persists correctly.
**Do not build yet:** decoys, enemies.

---

## Phase 5 — Decoy letters

**Depends on:** Phase 4 (so a wrong guess costs a resource that now matters).
**Goal:** hitting a box is no longer risk-free.

Tasks:
- [ ] When a box is hit, decide whether it yields a correct letter for the
      target word's next blank, or a decoy that belongs elsewhere / isn't
      needed.
- [ ] On decoy pickup: deduct from the Blocks counter, show a distinct
      visual/audio cue, fill no blank.
- [ ] Make sure decoys respawn under the same "smashed blocks reappear
      elsewhere" rule the correct-letter boxes already follow.

**Playable state:** wrong hits cost blocks, so players have a reason to think
about which box likely holds the letter they need (clue text / Speak Word)
instead of hitting everything.
**Do not build yet:** enemies.

---

## Phase 6 — Base enemy framework

**Depends on:** Phase 5.
**Goal:** a generic, harmless enemy exists and can be stomped.

Tasks:
- [ ] Generic enemy entity: position, simple back-and-forth patrol, a spawn
      point, placeholder rendering.
- [ ] Collision: landing on top kills it; touching it from the side gives a
      default reaction — brief knockback + ~1s invulnerability, nothing else.
- [ ] Killed enemies respawn after a fixed delay at their spawn point (no
      persistence needed).
- [ ] Scatter a handful of spawn points across the world, independent of
      word clusters.

**Playable state:** at least one enemy type wanders the world; stomping kills
it; side contact knocks you back but otherwise doesn't hurt you.
**Do not build yet:** letter-eating or letter-stealing behaviour.

---

## Phase 7 — Enemy: Muncher (eats floor letters)

**Depends on:** Phase 6.
**Goal:** letters left too long on the ground are at risk.

Tasks:
- [ ] Confirm/implement: a popped letter rests as a loose, collectable
      ground object for a short window before (or instead of) being
      auto-collected. Add this grace period if it doesn't already exist.
- [ ] New enemy subtype (Muncher): if it overlaps a loose floor letter, it
      eats it (removes it from the ground, holds it internally).
- [ ] On stomp-kill, a Muncher drops any letters it's holding back onto the
      ground at its death position, immediately collectable again.

**Playable state:** leaving a popped letter too long risks a Muncher eating
it first; killing a Muncher recovers what it ate.
**Do not build yet:** stealing from already-filled blanks.

---

## Phase 8 — Enemy: Thief (steals collected letters)

**Depends on:** Phase 7 (reuses the "drop letter on death" mechanism).
**Goal:** letters you've already collected aren't fully safe either.

Tasks:
- [ ] New enemy subtype (Thief): on side contact with the player (not
      stomp), if the player has at least one filled blank nearby, revoke one
      filled letter (blank goes back to empty) and have the Thief visibly
      carry it.
- [ ] On stomp-kill, a Thief drops its stolen letter to the ground at its
      death position as a normal loose letter — collectable as usual (and
      itself vulnerable to a passing Muncher).

**Playable state:** Thief contact costs you a letter you already had; chasing
it down and stomping it gets it back. This completes the feature set from
the brief.
**Do not build yet:** nothing mandatory remains — see Phase 9 for optional polish.

---

## Phase 9 (optional) — Polish pass

Not required. If there's appetite left: biome-styled backdrops per world
segment, a day/night cycle, distinct sound cues for decoys and each enemy
type, a small visual flourish at the loop seam.
