# Graph Report - .  (2026-06-22)

## Corpus Check
- Corpus is ~8,934 words - fits in a single context window. You may not need a graph.

## Summary
- 89 nodes · 111 edges · 13 communities (12 shown, 1 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Game Views & Routing Loop|Game Views & Routing Loop]]
- [[_COMMUNITY_Player Logic & Character Tests|Player Logic & Character Tests]]
- [[_COMMUNITY_Game Balancing & Config Loader|Game Balancing & Config Loader]]
- [[_COMMUNITY_Item Mechanics & Magnet Pickup|Item Mechanics & Magnet Pickup]]
- [[_COMMUNITY_Arcade Migration & RPG Design|Arcade Migration & RPG Design]]
- [[_COMMUNITY_Database Design & Library Stack|Database Design & Library Stack]]
- [[_COMMUNITY_Project Overview & Game FSM|Project Overview & Game FSM]]
- [[_COMMUNITY_Dungeon Map Layout & Secrets|Dungeon Map Layout & Secrets]]
- [[_COMMUNITY_Documentation Guidelines & Style|Documentation Guidelines & Style]]
- [[_COMMUNITY_Git Workflow & Team Setup|Git Workflow & Team Setup]]

## God Nodes (most connected - your core abstractions)
1. `GameView` - 18 edges
2. `Player` - 15 edges
3. `Balancing` - 13 edges
4. `ItemManager` - 12 edges
5. `MenuView` - 8 edges
6. `Action RPG Design Document` - 5 edges
7. `DatabaseManager Class` - 3 edges
8. `Map Design Document` - 3 edges
9. `main()` - 2 edges
10. `test_default_balancing_fallback()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Map Design Document` --references--> `Dungeon Tilesheet Image`  [INFERRED]
  markdown/arcade/map_design.md → assets/images/dungeon_tilesheet.png
- `MindMatrix Overview and Designs` --semantically_similar_to--> `Dungeon Swordman Project README`  [INFERRED] [semantically similar]
  markdown/awal.md → readme.md
- `GameView` --uses--> `Balancing`  [INFERRED]
  views/game_view.py → core/balancing.py
- `GameView` --uses--> `ItemManager`  [INFERRED]
  views/game_view.py → core/item_manager.py
- `GameView` --uses--> `Player`  [INFERRED]
  views/game_view.py → core/player.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pygame Game Loop and UI System** — markdown_01_project_overview_game_loop, markdown_02_folder_structure_gamestate_manager, markdown_05_ui_design_button [INFERRED 0.85]
- **Data Storage and Validation System** — markdown_04_database_design_database_manager, markdown_04_database_design_dao_pattern, markdown_03_library_stack_pydantic [INFERRED 0.85]
- **Dungeon Game Exploration and Loop Progression** — concept_swordman, concept_queen_tesa, markdown_arcade_map_design_doc [INFERRED 0.85]

## Communities (13 total, 1 thin omitted)

### Community 0 - "Game Views & Routing Loop"
Cohesion: 0.14
Nodes (3): main(), GameView, MenuView

### Community 1 - "Player Logic & Character Tests"
Cohesion: 0.23
Nodes (6): Player, test_add_item(), test_drop_item(), test_player_initial_state(), test_select_slot(), test_update_position()

### Community 2 - "Game Balancing & Config Loader"
Cohesion: 0.23
Nodes (3): Balancing, test_default_balancing_fallback(), test_load_balancing_from_file()

### Community 3 - "Item Mechanics & Magnet Pickup"
Cohesion: 0.29
Nodes (5): ItemManager, test_magnet_pull_and_pickup(), test_pickup_inventory_full(), test_spawn_item(), test_update_cooldown()

### Community 4 - "Arcade Migration & RPG Design"
Cohesion: 0.22
Nodes (9): Inventory/Magnet Mechanics, Lighting/Aura System, Queen Tesa Boss, Swordman Character, Action RPG Design Document, MindMatrix Overview and Designs, Arcade Learning and Migration Plan, Dungeon Swordman Project README (+1 more)

### Community 5 - "Database Design & Library Stack"
Cohesion: 0.29
Nodes (8): Library Stack & Dependencies, Pydantic Validation, Pygame-CE, Database Design & DAO, Data Access Object (DAO) Pattern, DatabaseManager Class, UI Design & Screens, Button Class

### Community 6 - "Project Overview & Game FSM"
Cohesion: 0.40
Nodes (5): Project Overview Document, Game Loop Architecture, MindMatrix: Trivia & Puzzle, Folder Structure & Routing Logic, GameStateManager Class

### Community 7 - "Dungeon Map Layout & Secrets"
Cohesion: 0.50
Nodes (4): Dungeon Tilesheet Image, Developer Room Teleport, Sewage Drain Easter Egg, Map Design Document

### Community 8 - "Documentation Guidelines & Style"
Cohesion: 0.67
Nodes (3): Documentation Guide, Google Style Docstring, Sphinx Documentation

## Knowledge Gaps
- **15 isolated node(s):** `MindMatrix: Trivia & Puzzle`, `Folder Structure & Routing Logic`, `UI Design & Screens`, `Sphinx Documentation`, `Google Style Docstring` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GameView` connect `Game Views & Routing Loop` to `Player Logic & Character Tests`, `Game Balancing & Config Loader`, `Item Mechanics & Magnet Pickup`?**
  _High betweenness centrality (0.208) - this node is a cross-community bridge._
- **Why does `Player` connect `Player Logic & Character Tests` to `Game Views & Routing Loop`, `Game Balancing & Config Loader`, `Item Mechanics & Magnet Pickup`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `Balancing` connect `Game Balancing & Config Loader` to `Game Views & Routing Loop`, `Item Mechanics & Magnet Pickup`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `GameView` (e.g. with `Balancing` and `ItemManager`) actually correct?**
  _`GameView` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MindMatrix: Trivia & Puzzle`, `Folder Structure & Routing Logic`, `UI Design & Screens` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Game Views & Routing Loop` be split into smaller, more focused modules?**
  _Cohesion score 0.1437908496732026 - nodes in this community are weakly interconnected._