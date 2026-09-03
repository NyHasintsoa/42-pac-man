# 🏛️ Architecture Decision Records (ADR)

This document records the key architectural decisions made during the development of the Pac-Man Game Engine project.

---

## **ADR 001: Centralized Game Context & Decoupled Configuration**

- **Status:** Accepted
- **Context:** The original setup relied on static configurations and direct coupling between individual pages, making it difficult to pass shared state (e.g., active scores, selected levels, game state) cleanly across screen transitions.
- **Decision:** Implement a centralized `GameContext` model and a dynamic `GameConfig` parser.
- `GameConfig` handles parsing and providing customizable settings instead of using hardcoded variables.
- `GameContext` acts as a shared state hub across all UI pages and components to standardize data access and validation.

- **Consequences:**
- **Positive:** Decouples page logic, simplifies screen transition management, and makes configuration easily expandable without modifying component code.
- **Negative:** Requires passing `GameContext` down through initializing view hierarchies.

---

## **ADR 002: Modular Page Navigation State Machine**

- **Status:** Accepted
- **Context:** Navigating between screens (Main Menu, Loading, Gameplay, High Scores, Name Submission) required a robust navigation flow that prevents circular dependencies and memory leaks during page swaps.
- **Decision:** Implement a state machine pattern to handle page switching. Standardize page naming conventions by removing redundant suffixes (e.g., changing `GamePage` file names to cleaner, unified page modules).
- **Consequences:**
- **Positive:** Clean lifecycle management (initialization, update, render, cleanup) per view, reducing dangling memory references and leak risks.
- **Negative:** Adding a new screen requires updating the route state enum and transition hooks.

---

## **ADR 003: Procedural Level Generation & Asynchronous Loading Screen**

- **Status:** Accepted
- **Context:** To ensure replayability, levels needed to be dynamically generated rather than strictly relying on hardcoded static maps. However, generating maze geometry and item layouts introduces a brief processing pause.
- **Decision:** Create an autonomous `LevelGenerator` alongside a `LevelManager` to control progression. Introduce a dedicated `LoadingPage` state to smoothly handle UI feedback during maze construction.
- **Consequences:**
- **Positive:** Enhances gameplay variety while maintaining a smooth user experience via visual loading feedback.
- **Negative:** Adds complexity to the level initialization lifecycle.

---

## **ADR 004: JSON-Based Local Score Persistence**

- **Status:** Accepted
- **Context:** High scores and player names need to persist across application restarts without introducing the overhead of a full relational database.
- **Decision:** Implement a lightweight `ScoreManager` that serializes leaderboard entries and writes them asynchronously to a local structured JSON file.
- **Consequences:**
- **Positive:** Zero external database dependencies; simple, human-readable data format.
- **Negative:** File I/O must be handled carefully to avoid blocking the main game loop thread.

---

## **ADR 005: Input Component Validation Rule Enforcement**

- **Status:** Accepted
- **Context:** Submitting high scores requires clean player names to maintain UI alignment on the leaderboard. Unfiltered input could lead to visual overflow or invalid persistence data.
- **Decision:** Restrict the `Input` UI component at the frame level using character filtering (`isalnum()` or `"-"`). All unapproved special characters and spaces are rejected immediately on keypress.
- **Consequences:**
- **Positive:** Prevents invalid string formatting at the entry point without requiring downstream regex sanitization.
- **Negative:** Users cannot use spaces or special symbols in their player tag.

---

## **ADR 006: Local Cache Build System Optimization**

- **Status:** Accepted
- **Context:** Incremental project builds during core refactoring and testing cycles were slowed down by full recompilation overhead.
- **Decision:** Refactor the project `Makefile` to leverage a local build cache directory for intermediate compilation objects.
- **Consequences:**
- **Positive:** Significantly faster build and execution times during local development.
- **Negative:** Build target rules in the `Makefile` must explicitly account for cache invalidation when headers or dependencies change.
