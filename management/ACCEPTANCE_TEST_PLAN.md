# 🧪 Acceptance Test Plan (ATP)

This document outlines the acceptance test cases, feature verification, and bug resolution history for the Pac-Man Game Engine.

---

## 📌 Features Tested

| Feature Category            | Test Case Description                                         | Expected Result                                                              | Status   |
| --------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------- |
| **Page Navigation & State** | Transition between Main Menu, Loading, Game, and High Scores  | Pages transition smoothly without crashing or dropping state.                | **PASS** |
| **Level Generation**        | Asynchronous generation of dynamic mazes via `LevelGenerator` | Maze structure generates cleanly during `LoadingPage` state.                 | **PASS** |
| **Pac-Man Controls**        | Arrow keys and WASD grid movement with wall collision         | Pac-Man moves smoothly along grid and stops at walls.                        | **PASS** |
| **Pac-Gum Mechanics**       | Render Pac-Gums and handle consumption mechanics              | Pac-Man eats Pac-Gums on contact, updating total score.                      | **PASS** |
| **Ghost AI Pathfinding**    | Unique pathfinding routines per ghost entity                  | Ghosts navigate maze using distinct tracking behaviors.                      | **PASS** |
| **Ghost Frightened Mode**   | Power pellet consumption turns ghosts edible                  | Ghosts enter edible mode and reset to spawn when consumed.                   | **PASS** |
| **Score Persistence**       | `ScoreManager` JSON file I/O operations                       | Scores save to and load from local `JSON` storage reliably.                  | **PASS** |
| **Player Input Validation** | `Input` component restriction rules                           | Rejects spacebar and special characters, allowing only alphanumeric and `-`. | **PASS** |
| **In-Game Overlays**        | Pause menu toggle and developer cheat panel controls          | Pauses game loop cleanly and enables developer overrides.                    | **PASS** |

---

## 🐛 Bugs Found & Resolved

### 1. **Dangling Memory References & State Leaks**

- **Issue:** Memory leaks occurred when repeatedly transitioning between game states and reloading mazes.
- **Fix:** Refactored object lifecycle methods across all pages, ensuring explicit unloading of textures, fonts, and model validations via `GameContext`.

---

### 2. **Unvalidated Player Input Character Overflow**

- **Issue:** Entering spaces or special characters in the high score name submission field caused UI overflow and visual clipping on the leaderboard.
- **Fix:** Updated the `Input` component's `update()` loop using character-level checks (`char_pressed.isalnum() or char_pressed == "-"`), instantly ignoring unapproved keypresses.

---

### 3. **Static Configuration Hardcoding**

- **Issue:** Hardcoded canvas parameters and maze configurations prevented dynamic scaling and custom window resolution support.
- **Fix:** Implemented `GameConfig` and dynamic layout scaling algorithms to proportionally offset and scale UI elements across all screen resolutions.

---

### 4. **Ghost Respawn Logic Out-of-Bounds**

- **Issue:** Eaten ghosts failed to correctly reset their position tracking to the central ghost house.
- **Fix:** Added explicit initial position resetting logic (`refactor(ghost): make ghost return to their initial position`).
