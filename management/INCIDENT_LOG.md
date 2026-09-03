# 🚧 Summary of Blocking Points & Conflict Resolution

This document summarizes the primary technical bottlenecks, architectural conflicts, and resolutions encountered during the development of the Pac-Man Game Engine.

---

## 🛑 Technical Blocking Points

### 1. **Page State Management & Transition Leaks**

- **Blocker:** Frequent switching between main menu, loading, game, and high score screens created dangling references and memory leaks, leading to frame rate degradation.
- **Resolution:** Refactored page lifecycle management and implemented `GameContext` to cleanly handle state transitions, asset unloading, and validation across views.

### 2. **Static vs. Dynamic Configuration Dependencies**

- **Blocker:** Hardcoded screen dimensions and static values prevented the UI from scaling dynamically, blocking maze centering and scoreboard alignment.
- **Resolution:** Built a dynamic `GameConfig` parser to decouple settings from component logic and integrated a scaling system across all character entities and UI elements.

### 3. **Input Handling & String Formatting Edge Cases**

- **Blocker:** Unfiltered keyboard input on the high score submission screen allowed invalid special characters and spaces, causing leaderboard rendering overflows.
- **Resolution:** Restricted keypress character filtering directly at the input component level using `isalnum()` and explicit hyphen (`"-"`) checks.

---

## ⚔️ Architectural & Design Conflicts

| Area of Conflict                           | Design Dilemma                                                                               | Final Resolution                                                                                                         |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Maze Generation Sync vs. Async**         | Blocking the main thread during maze generation vs. introducing complex async loading logic. | Introduced a dedicated `LoadingPage` state to keep the rendering loop responsive during level generation.                |
| **Ghost Pathfinding AI Complexity**        | Simple random movements vs. complex individual pathfinding behavior per ghost.               | Designed modular pathfinding routines per ghost entity, including specialized edible (frightened) and respawn behaviors. |
| **Persistence Storage Mechanism**          | External database overhead vs. local file storage simplicity.                                | Selected lightweight local JSON storage managed by a dedicated `ScoreManager` service.                                   |
| **Directory Architecture Standardization** | Loose file structure vs. strict model/view categorization.                                   | Standardized file naming by stripping redundant module suffixes and organizing models under `model/enums`.               |
