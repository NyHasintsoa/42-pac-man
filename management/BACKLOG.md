# 🕹️ Project Product Backlog: Pac-Man Game Engine

## 📌 Epics Overview

1. **Epic 1: Core Framework & Navigation Architecture**

2. **Epic 2: Map & Level Management System**

3. **Epic 3: Gameplay Mechanics & Entity Logic**

4. **Epic 4: State Management & In-Game UI**

5. **Epic 5: Score Tracking & High Score Persistence**

6. **Epic 6: Build System & Architecture Refactoring**

---

## 🚀 Epic 1: Core Framework & Navigation Architecture

### User Story 1.1: Project Setup & Dependency Management

> As a developer, I want to initialize the core project dependencies so that the environment is ready for rendering and logic development.

- [x] **Task 1.1.1:** Add required project dependencies and libraries.
- [x] **Task 1.1.2:** Configure Makefile for local caching and optimized builds.

### User Story 1.2: Page Management & Screen Transitions

> As a player, I want to seamlessly navigate between different screens (Main Menu, Game, High Scores, etc.).

- [x] **Task 1.2.1:** Implement base page structure and basic transition flow.
- [x] **Task 1.2.2:** Standardize page class naming by removing file suffixes.

- [x] **Task 1.2.3:** Update all UI pages to conform to Pac-Man project requirements.
- [x] **Task 1.2.4:** Remove outdated pages (e.g., legacy level menu page).

---

## 🗺️ Epic 2: Map & Level Management System

### User Story 2.1: Dynamic Level Generation & Loading

> As a player, I want levels to load cleanly with visually distinct mazes and dedicated loading screens.

- [x] **Task 2.1.1:** Implement procedural/dynamic Level Generator.
- [x] **Task 2.1.2:** Build a dedicated Loading Page during maze generation.
- [x] **Task 2.1.3:** Build a Level Manager to control progression between levels.

### User Story 2.2: Maze Rendering & Layout Adjustment

> As a player, I want a centered, visually polished maze layout that fits properly within the game frame.

- [x] **Task 2.2.1:** Add Maze Component and strip out unused asset images.
- [x] **Task 2.2.2:** Enhance maze wall rendering for an authentic arcade UI look.
- [x] **Task 2.2.3:** Refactor Game Page layout to center the maze and integrate UI scoreboards.

---

## 👻 Epic 3: Gameplay Mechanics & Entity Logic

### User Story 3.1: Pac-Man Control & Interactions

> As a player, I want smooth control over Pac-Man, allowing me to move around the maze and consume Pac-Gums.

- [x] **Task 3.1.1:** Implement Pac-Man movement controls and collision logic with walls.
- [x] **Task 3.1.2:** Implement Pac-Gum generator and rendering on the maze.

- [x] **Task 3.1.3:** Add eating mechanics for Pac-Man consuming standard Pac-Gums.
- [x] **Task 3.1.4:** Apply scaling parameters across all character sprites.

### User Story 3.2: Ghost AI & State Machine

> As a player, I want ghosts with distinct AI algorithms and edible states so that the game is challenging and interactive.

- [x] **Task 3.2.1:** Implement custom pathfinding algorithms for each ghost.

- [x] **Task 3.2.2:** Add "Edible" (Frightened) state to ghosts upon Pac-Man eating power pellets.

- [x] **Task 3.2.3:** Implement ghost respawn mechanics (return to initial spawn position when eaten).

---

## 🕹️ Epic 4: State Management & In-Game UI

### User Story 4.1: Game Loop & Countdown Sequence

> As a player, I want a brief countdown before a stage starts so I can prepare for gameplay.

- [x] **Task 4.1.1:** Add a stage pre-game countdown timer.

- [x] **Task 4.1.2:** Trigger active gameplay input immediately once countdown ends.

### User Story 4.2: In-Game Control Panels

> As a player/developer, I want to pause the game or trigger debug cheat commands during testing.

- [x] **Task 4.1.1:** Add Pause Panel with pause/resume game state controls.

- [x] **Task 4.1.2:** Add Cheat Panel for debug features (e.g., instant level clear, god mode).

---

## 🏆 Epic 5: Score Tracking & High Score Persistence

### User Story 5.1: High Score System & Name Submission

> As a high-scoring player, I want to record my name and save my score to a leaderboard.

- [x] **Task 5.1.1:** Implement Score Manager to handle active scoring logic.

- [x] **Task 5.1.2:** Build Player Name input screen following game completion.

- [x] **Task 5.1.3:** Create High Score Leaderboard page displaying top player records.

- [x] **Task 5.1.4:** Persist and load score data asynchronously to/from a local `JSON` file.

---

## 🏗️ Epic 6: Build System & Architecture Refactoring

### Technical Debt & Code Health

> As a developer, I want a clean, modular architecture with validated models to ensure maintainability and prevent memory leaks.

- [x] **Task 6.1:** Refactor configuration parser into centralized `GameConfig` and `GameContext` models.

- [x] **Task 6.2:** Reorganize project folder hierarchy (move enums and data definitions into `src/model/`).
- [x] **Task 6.3:** Eliminate hardcoded static settings in favor of dynamic `GameConfig`.

- [x] **Task 6.4:** Clean up dangling references, code leaks, and standardize variable naming across classes.

- [x] **Task 6.5:** Clean up generated/temp directories (removed legacy `gen/` directory).
