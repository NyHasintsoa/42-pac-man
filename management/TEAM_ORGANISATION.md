# 👥 Team Organization & Contribution Structure

## 📌 Team Members & Roles

- **Primary User (`primary-user`)**: Lead Software Engineer & Systems Architect
- **Secondary User (`secondary-user`)**: Full-Stack Game Developer & UI/UX Specialist

---

## 🚀 Division of Responsibilities & Lifecycle Steps

```
         ┌─────────────────────────────────────────────────────────────┐
         │                    TEAM ORGANIZATION FLOW                   │
         └──────────────────────────────┬──────────────────────────────┘
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
┌───────────────────────────┐                             ┌───────────────────────────┐
│       PRIMARY USER        │                             │      SECONDARY USER       │
│  Architecture & Core AI   │                             │   UI, Assets & Frontend   │
└──────────┬────────────────┘                             └──────────┬────────────────┘
           │                                                         │
           ├── Core Framework Setup                                  ├── UI / Page Transitions
           ├── Level & Maze Generation                               ├── Pac-Gums & Scoreboard
           ├── Ghost AI Algorithms                                   ├── High Score UI & Input
           └── Configuration & Memory                                └── Cheat & Pause Panels

```

---

## 🛠️ Step-by-Step Task Distribution

### Phase 1: Initial Setup & Architectural Foundations

- **`primary-user`**:
- Initialized project configuration, build Makefile, and dependency management.

- Defined core state management architecture using `GameContext` and `GameConfig`.

- Reorganized project directory hierarchy (e.g., relocating enums into `model/enums`).

- **`secondary-user`**:
- Set up initial base pages and standard screen layout prototypes.

- Built page state machine and transition hooks between menus.

- Created asset loading pipelines and cleaned up unused image assets.

---

### Phase 2: World Generation & Rendering Mechanics

- **`primary-user`**:
- Developed the procedural `LevelGenerator` module and procedural maze construction logic.

- Designed data structures and generators for placing Pac-Gums within the maze grid.

- Built the intermediate asynchronous `LoadingPage` displayed during stage creation.

- **`secondary-user`**:
- Built the visual `Maze` component and styled wall graphics for the arcade interface.

- Centered the maze viewport and integrated side scoreboards.

- Rendered Pac-Gum sprites and implemented character scaling properties across resolutions.

---

### Phase 3: Gameplay Entities & AI Logic

- **`primary-user`**:
- Implemented Pac-Man grid movement, direction queueing, and wall collision resolution.

- Programmed custom pathfinding AI algorithms for each ghost.

- Added ghost behavior states, including frightened (edible) mode and respawning mechanisms.

- **`secondary-user`**:
- Connected Pac-Man collision detection with Pac-Gum consumption mechanics.

- Built stage pre-game countdown timer logic before unlocking gameplay.

- Built in-game overlay panels (Pause Panel & Cheat Panel).

---

### Phase 4: Persistence, High Scores & UI Polish

- **`primary-user`**:
- Built `ScoreManager` service with JSON serialization and disk persistence.

- Implemented data validation schemas using Pydantic models.

- Added `LevelManager` to orchestrate multi-stage progression and difficulty scaling.

- **`secondary-user`**:
- Created `PlayerNamePage` with input validation (alphanumeric and hyphen rules).

- Implemented dynamic scaled `HighScorePage` with scrolling and selection trophy indicators.

- Aligned all UI views to project specifications.

---

### Phase 5: Quality Assurance, Refactoring & Optimization

- **`primary-user`**:
- Conducted memory leak audits and refactored object references.

- Updated Makefile to leverage build caching for faster local compilation.

- **`secondary-user`**:
- Standardized UI page class naming, removing file suffix redundancies.

- Performed final visual polish across screens, responsiveness, and text spacing.
