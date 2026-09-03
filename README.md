*This project has been created as part of the 42 curriculum by primary-user, secondary-user.*

# Pacman

## 📖 Description

This project is an extensible 2D **Pac-Man Game Engine** implemented in Python.  
The goal of the project is to build a complete arcade game featuring procedural maze generation, ghost pathfinding AI, adaptive difficulty progression, local high score persistence, and dynamic configuration management through a centralized state machine.

---

## 🛠️ Instructions

### Prerequisites

* Python 3.10 or higher
* [uv](https://github.com/astral-sh/uv) fast Python package installer and runner

### Installation & Execution

```bash
# Clone the repository
git clone <repository-url>
cd pacman-game

# Sync dependencies using uv
uv sync

# Run the game using uv
uv run python pac-man.py config.json

```

### Build & Automation Commands

The project includes a `Makefile` configured for execution and cache optimization:

* `make`: Compiles and launches the game engine via `uv`.
* `make clean`: Flushes intermediate local build caches, pycache directories, and temp files.

---

## ⚙️ Configuration

The engine dynamically loads runtime settings from a `config.json` (JSON with Comments) configuration file via the `GameConfig` parser, removing hardcoded logic and allowing per-level custom tuning.

### Structure & Default Values

```json
// -----------------------------------------------
// PACMAN SETTINGS
// -----------------------------------------------
{
  "highscore_filename": "highscores.json",
  "cheating": true,
  "lives": 1,
  "level_max_time": 90,
  "seed": 42,
  "pacgum": 42,

  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,

  // -----------------------------------------------
  // LEVELS
  // -----------------------------------------------
  "levels": [
    {
      "width": 20,
      "height": 18,
      "seed": 20,
      "pacgum": 2,
      "level_max_time": 90,

      "points_per_pacgum": 10,
      "points_per_super_pacgum": 50,
      "points_per_ghost": 200
    }
  ]
}
```

* **`highscore_filename`** (`string`): The local JSON filename used by `ScoreManager` to store high scores (default: `"highscores.json"`).
* **`cheating`** (`boolean`): Enables or disables developer debug controls and the `CheatPanel` overlay (default: `false`).
* **`lives`** (`integer`): Starting life counter for Pac-Man at the start of a run.
* **`level_max_time`** (`integer`): Global countdown limit in seconds per level stage.
* **`seed`** (`integer`): Pseudo-random seed used by `LevelGenerator` for reproducible procedural maze generation.
* **`pacgum`** (`integer`): Total number of Pac-Gums placed across the maze layout.
* **`points_per_pacgum`** (`integer`): Base score awarded for consuming a standard Pac-Gum.
* **`points_per_super_pacgum`** (`integer`): Score awarded for eating a power pellet, triggering frightened ghost mode.
* **`points_per_ghost`** (`integer`): Base score awarded for consuming an edible ghost.

### Level-Specific Overrides (`levels`)

The `levels` array allows overriding global settings on a per-stage basis. Any parameter defined inside a level block takes precedence over the top-level configuration when that level is loaded by `LevelManager`:

```jsonc
"levels": [
  {
    "width": 20,                  // Grid cell width of the stage maze
    "height": 18,                 // Grid cell height of the stage maze
    "seed": 20,                   // Stage-specific generation seed
    "pacgum": 2,                  // Stage-specific Pac-Gum count
    "level_max_time": 90,         // Stage countdown limit in seconds
    "points_per_pacgum": 10,      // Stage score per Pac-Gum
    "points_per_super_pacgum": 50,// Stage score per Super Pac-Gum
    "points_per_ghost": 200       // Stage score per consumed Ghost
  }
]
```

## 🏆 Highscore System

The high score engine is managed by the `ScoreManager` service, which handles score tracking and serializes records into a structured local JSON file.

### Implementation Rationale

* **Zero Database Overhead:** Using a simple structured JSON file enables persistent storage without external database drivers.
* **Input Validation:** The player name submission screen enforces character filtering (`char_pressed.isalnum() or char_pressed == '-'`), preventing long inputs or special symbols from breaking UI alignment on the leaderboard table.

---

## 🌀 Maze Generation

Maze geometry is generated procedurally using the assigned `A-Maze-ing` package via the `LevelGenerator` module.

* **Procedural Assembly:** The generator dynamically constructs maze walls, path layouts, and Pac-Gum locations.
* **Asynchronous UX:** To prevent main thread freezing during maze construction, the game transitions into a dedicated `LoadingPage` state while the maze generates in the background.

---

## 🔬 Implementation Summary

* **State Management:** Uses a shared `GameContext` model to store active state across screen transitions.
* **Layout & Rendering:** The `Maze` viewport is centered dynamically on screen with adjacent scoreboards and scaling parameters applied to character sprites.
* **Optimization:** Includes memory leak remediations, explicit lifecycle teardowns, and local build caching.

---

## 🏗️ General Software Architecture

The architecture relies on a decoupled Model-View-Controller (MVC) approach driven by a page navigation state machine.

### Core Modules

* **`GameContext` / `GameConfig`:** Central state container and dynamic configuration parser.
* **`LevelManager` & `LevelGenerator`:** Manages stage progression, difficulty tuning, dynamic wall layouts, and item placement.
* **`ScoreManager`:** Handles local score tracking and asynchronous JSON storage.

### Pac-Man Ghosts!

Ghosts operate under individual state machines and distinct pathfinding routines:

* **Tracking Behaviors:** Blinky, Pinky, Inky, and Clyde utilize tailored target-chasing algorithms.
* **States:** Ghost logic handles state transitions between **Chase**, **Scatter**, **Frightened** (edible state triggered by power pellets), and **Eaten** (returning to spawn).

---

## 📊 Project Management

The project followed an Agile workflow structured around backlog epics, Architecture Decision Records (ADR), and Kanban tracking.

* Project management artifacts, architecture decisions, and backlog details are located in the dedicated project management folder: `/management`.

---

## 📚 Resources

### References

* **[Python 3 Documentation](https://docs.python.org/3/tutorial/):** The official hands-on tutorial and reference manual covering Python syntax, data structures, built-in libraries, and object-oriented programming concepts.

* **[astral-sh/uv Documentation](https://docs.astral.sh/uv/):** Official guides and command references for `uv`, an extremely fast Python package and project manager designed to replace `pip`, `pip-tools`, and `virtualenv`.

* **[Pac-Man Ghost AI Mechanics](https://pacman.fandom.com/wiki/Maze_Ghost_AI_Behaviors):** A detailed technical breakdown of the classic arcade Pac-Man ghost behavior, explaining targeting tile math, state loops (Chase, Scatter, Frightened), and individual personality algorithms for Blinky, Pinky, Inky, and Clyde.

* **[Raylib Documentation](https://www.raylib.com/):** The central hub for Raylib, a simple and easy-to-use C library for 2D/3D hardware-accelerated game programming, complete with API cheatsheets, code examples, and binding references.

* **[Pydantic Documentation](https://pydantic.dev/docs/validation/latest/get-started/):** Getting started guides and usage references for Pydantic, a high-performance Python data validation and settings management library powered by type annotations.

* **[Classic Gaming Pac-Man Vector Art](https://classicgaming.cc/classics/pac-man/vector-art):** An online asset repository providing high-quality vector graphics, character sprites, and original arcade visual assets used for Pac-Man, the ghosts, and maze elements.

* **[Classic Gaming Pac-Man Resource Hub](https://classicgaming.cc/classics/pac-man):** A general reference page covering classic Pac-Man arcade history, game rules, maze layouts, fruit bonus values, and sound asset archives.

### AI Usage

* **Architecture Design:** Assisted in designing the state machine navigation framework and drafting initial product backlog epics.
* **Algorithm Validation:** Used to review coordinate math and pathfinding implementations for ghost target algorithms.
* **Documentation:** Used to consolidate Git commit histories into release notes, timelines, and technical summaries.