# 🕹️ Online Arcade Game Management System
## Master Project Checklist & Complete Overview

> **Evaluation Date:** April 20, 2026 (Monday) | **Submission:** April 17, 2026 (Friday PDF)
> **Total Marks:** 10 | **Team:** 4 Members (366, 387, 906, 913)

---

## 📋 MASTER EVALUATION CHECKLIST

### ✅ Analysis & Design Models — 2 Marks

| Item | Required | Status | Who Covers It |
|---|---|---|---|
| Use Case Diagram (1) | ✅ Required | ☐ Check PDF | All members — understand it |
| Class Diagram (1) | ✅ Required | ☐ Check PDF | All members — know your classes |
| Activity Diagram (4) | ✅ Required | ☐ Check PDF | ACTIVITY_2.jpeg in repo |
| State Diagram (4) | ✅ Required | ☐ Check PDF | STATE_2.jpeg in repo |

> **Tip:** In the viva, all 4 members should be able to point to the class diagram and identify their own entities.

---

### ✅ MVC Architecture Pattern — 2 Marks

| Layer | Package | Classes |
|---|---|---|
| **Model** | `com.arcade.management.model` | Player, Game, Item, Admin, Level, Achievement, MultiplayerSession, PlayerSession, PlayerAchievement, PlayerItem, Rank |
| **View** | `src/main/resources/templates/` | Thymeleaf HTML files (players/register.html, items/list.html, etc.) |
| **Controller** | `com.arcade.management.controller` | PlayerController, GameController, ItemController, AdminController, SessionController, AchievementController, LoginController, HomeController |
| **Service** | `com.arcade.management.service` | PlayerService, ItemService, GameService, AdminService, AchievementService, SessionService (interfaces + impls) |
| **Repository** | `com.arcade.management.repository` | PlayerRepository, ItemRepository, GameRepository... (Spring Data JPA) |

**What to say about MVC:**
> *"Our project strictly follows the MVC Architecture Pattern. The Model layer (JPA entities) contains the data. The View layer (Thymeleaf templates) handles presentation. The Controller layer (Spring MVC controllers) sits between them — receiving HTTP requests, calling service methods, and passing data to views. Controllers NEVER interact with repositories directly. All business logic lives in the Service layer. This clean separation means we can swap Thymeleaf for React tomorrow without touching the model or business logic."*

---

### ✅ Design Principles & Patterns — 3 Marks

**Rule: At least 1 per team member = 4 minimum required**

| Member | Principle/Pattern | Category | Evidence File |
|---|---|---|---|
| **906** | High Cohesion | GRASP Principle | `AchievementServiceImpl.java`, `SessionServiceImpl.java` |
| **913** | Information Expert | GRASP Principle | `PlayerServiceImpl.java` → `checkAndUpdateRank()` |
| **387** | Controller | GRASP Principle | `PlayerController.java`, `GameController.java` |
| **366** | Single Responsibility Principle (SRP) | SOLID Principle | `Admin.java` vs `Player.java` separation |
| **ALL** | Factory Method Pattern | Creational Pattern | `ItemFactory.java` |

> **Note:** We use **4 GRASP + 4 SOLID + 1 Creational Pattern = 9 total principles** documented in README.md. Each member presents 1 GRASP during demo.

---

### ✅ Presentation / Demo / Code Explanation — 3 Marks

| Task | Responsible | Time Estimate |
|---|---|---|
| Run setup commands | Designated screen sharer | Before demo starts |
| Explain project overview + MVC | Any member (split) | 2-3 min |
| Demo: Register Player flow | 387 | 1 min |
| Demo: Add Item with Factory | 366 | 1 min |
| Demo: Create Session | 906 | 1 min |
| Demo: View Leaderboard / Rank | 913 | 1 min |
| Code walkthrough (each person) | Individual | 2 min each |

---

## 🚀 HOW TO RUN THE PROJECT (Do This First)

```bash
# Terminal 1: Start MySQL
sudo service mysql start

# Verify database exists (optional)
mysql -u root -p
# Inside MySQL:
CREATE DATABASE IF NOT EXISTS arcade_db;
EXIT;

# Terminal 2: Navigate to project and run
cd /path/to/monishaooad_miniproj
mvn clean spring-boot:run
```

Open browser: **http://localhost:8080**

### Demo Flow in Browser
1. Go to `/players/register` → register a new player
2. Go to `/login` → log in with new player
3. Go to `/items/add` → add item "Excalibur" type "Weapon" with blank rarity → show it saves as "Uncommon" (Factory!)
4. Go to `/items` → show item list
5. Go to `/sessions/add` → create a multiplayer session
6. Go to `/players/leaderboard` → show rank ordering
7. Go to `/achievements` → show achievement catalog

---

## 🏗️ COMPLETE SYSTEM ARCHITECTURE

### Technology Stack
```
Spring Boot 3.x          ← Application framework (auto-config, DI, web)
Hibernate / JPA          ← ORM: maps Java objects ↔ MySQL tables
Thymeleaf                ← Server-side HTML rendering (View layer)
MySQL (arcade_db)        ← Relational database
Maven                    ← Build and dependency management
Lombok                   ← Reduces boilerplate (@Data, @NoArgsConstructor)
Spring Session JDBC      ← HTTP sessions stored in MySQL (secure sessions)
```

### Full Entity-Relationship Overview
```
[Admin]          ← Manages system (separate from Player by design — SRP)

[Game] ──< [Level]                        ← One game, many levels
[Game] ──< [MultiplayerSession]           ← One game, many lobbies
[MultiplayerSession] ──< [PlayerSession] >── [Player]    ← Many players per lobby
[Player] >── [Rank]                       ← Many players share one rank
[Player] ──< [PlayerAchievement] >── [Achievement]  ← Earned achievements
[Player] ──< [PlayerItem] >── [Item]      ← Player inventory
```

### Package Structure
```
com.arcade.management/
├── ArcadeManagementApplication.java      ← Spring Boot entry point (@SpringBootApplication)
├── controller/
│   ├── PlayerController.java             ← /players/** (387)
│   ├── GameController.java               ← /games/**  (387)
│   ├── ItemController.java               ← /items/**  (366)
│   ├── AdminController.java              ← /admin/**  (366)
│   ├── SessionController.java            ← /sessions/** (906)
│   ├── AchievementController.java        ← /achievements/** (906)
│   ├── LoginController.java              ← /login, /logout (shared)
│   └── HomeController.java               ← / home page (shared)
├── service/
│   ├── PlayerService.java + impl/        ← Player business logic (387/913)
│   ├── ItemService.java + impl/          ← Item CRUD (366)
│   ├── AdminService.java + impl/         ← Admin CRUD (366)
│   ├── GameService.java + impl/          ← Game catalog (387)
│   ├── AchievementService.java + impl/   ← Achievement CRUD (906)
│   └── SessionService.java + impl/       ← Session lifecycle (906)
├── model/                                ← All JPA entities
├── repository/                           ← Spring Data JPA interfaces
├── factory/
│   └── ItemFactory.java                  ← Factory Method Pattern (366)
├── dto/
│   ├── PlayerDTO.java                    ← Player form data carrier
│   ├── LoginDTO.java                     ← Login credentials carrier
│   ├── GameDTO.java                      ← Game form data
│   ├── UserSessionDTO.java               ← Logged-in user session info
│   └── LeaderboardDTO.java               ← Leaderboard query results
└── exception/
    ├── PlayerNotFoundException.java      ← Custom exception (SRP)
    └── GlobalExceptionHandler.java       ← Centralized error handling (SRP)
```

---

## 👥 MEMBER-BY-MEMBER RESPONSIBILITIES

### 👤 Member 906 — Game Infrastructure
**Classes:** `Achievement`, `MultiplayerSession`, `Level`
**Services:** `AchievementService`, `SessionService` (+ impls)
**Controllers:** `AchievementController`, `SessionController`
**GRASP Principle:** **High Cohesion** — each service class is narrowly focused
**Pattern Knowledge:** Factory Method (project-wide)

**Key points to explain:**
- `Achievement` = catalog of available achievements (locked until earned)
- `MultiplayerSession` = a game lobby instance with start/end timestamps
- `Level` = difficulty progression within a game
- High Cohesion means each service class does exactly one thing

---

### 👤 Member 913 — Player Progression
**Classes:** `PlayerSession`, `Rank`, `PlayerAchievement`
**Services:** Collaborates with `PlayerServiceImpl` for rank logic
**GRASP Principle:** **Information Expert** — `PlayerServiceImpl` holds score+rank data → does the rank evaluation
**Pattern Knowledge:** Factory Method (project-wide)

**Key points to explain:**
- `PlayerSession` = bridge table: one player's record inside one lobby (score + position)
- `Rank` = pre-seeded thresholds (Bronze=0, Silver=500, Gold=1000, Platinum=5000)
- `PlayerAchievement` = bridge table: evidence a player earned a specific achievement
- `checkAndUpdateRank()` in `PlayerServiceImpl` is the Information Expert demonstration

---

### 👤 Member 387 — Core User & Game Catalog
**Classes:** `Player`, `Game`, `PlayerItem`
**Services:** `PlayerService`, `GameService` (+ impls)
**Controllers:** `PlayerController`, `GameController`
**GRASP Principle:** **Controller** — `PlayerController` is the UI-to-logic boundary
**Pattern Knowledge:** Factory Method (project-wide)

**Key points to explain:**
- `Player` = central entity with cascading relationships to achievements, items, sessions
- `PlayerDTO` shields the entity from raw HTTP form data
- `Game` = catalog with linked levels and session lobbies
- `PlayerItem` = bridge table with `acquiredDate`
- Leaderboard: `findTop10ByOrderByTotalScoreDesc()` — Spring-generated SQL

---

### 👤 Member 366 — Admin & Item Catalog + Factory
**Classes:** `Admin`, `Item`
**Services:** `AdminService`, `ItemService` (+ impls)
**Controllers:** `AdminController`, `ItemController`
**SOLID Principle:** **Single Responsibility Principle** — Admin and Player are separate for SRP reasons
**Creational Pattern:** **Factory Method** — `ItemFactory.java` (ONLY person to demo this live)

**Key points to explain:**
- `Admin` is separate from `Player` by design (SRP)
- `Admin implements Serializable` for Spring Session JDBC compatibility
- `ItemFactory.createItem()` applies default rarities per item type
- Weapons → Uncommon, Consumables → Common, Armor → Rare
- Live Demo: Add item "Excalibur" type "Weapon" no rarity → show "Uncommon" appears

---

## 📚 DESIGN PRINCIPLES FULL EXPLANATION

### GRASP Principles Used

#### 1. High Cohesion (906)
> Each class has a narrow, well-defined purpose. `AchievementServiceImpl` only manages achievements. `SessionServiceImpl` only manages session lifecycle. No "God Classes" that do everything.

#### 2. Information Expert (913)
> Assign a responsibility to the class that has the information to fulfill it. `PlayerServiceImpl` holds `totalScore` data AND has `RankRepository` access → it naturally does rank evaluation. Not the Controller, not the database.

#### 3. Controller (387)
> Dedicate a class to handle external system input. `PlayerController` receives HTTP requests, reads form data (via DTO), and delegates all logic to `PlayerService`. Zero business logic in the controller.

#### 4. Creator (All — via Factory + Repositories)
> A class should create objects when it "contains" or "records" them. Spring Data JPA repositories act as Creators for DB records. `ItemFactory` acts as Creator for properly configured Item objects.

---

### SOLID Principles Used

#### 1. Single Responsibility Principle — SRP (366)
> A class should have one reason to change. `Admin` → admin auth concerns only. `Player` → gameplay concerns only. `GlobalExceptionHandler` → error mapping only. `LoginDTO` → credential transfer only.

#### 2. Open/Closed Principle — OCP (913)
> Open for extension, closed for modification. The `PlayerService` interface is closed (controllers depend on it and won't break). New implementation variants can be added without modifying existing code.

#### 3. Liskov Substitution Principle — LSP (906)
> Subclasses must be substitutable for their base types. All `*Repository` interfaces extend `JpaRepository`. Spring injects a proxy at runtime that perfectly replaces the interface — controllers and services never know the difference.

#### 4. Dependency Inversion Principle — DIP (387)
> Depend on abstractions, not concretions. `@Autowired private PlayerService playerService` — Controllers hold INTERFACE references. Spring injects `PlayerServiceImpl` at runtime. Changing the implementation requires zero controller changes.

---

### Creational Design Pattern — Factory Method (366 — LIVE DEMO)

**Problem:** Raw `new Item()` calls scattered everywhere mean business rules (like rarity defaults) are duplicated across controllers.

**Solution:** `ItemFactory.createItem(name, type, rarity)`:
- Routes to type-specific private factory methods
- Applies default rarities if user input is blank
- Returns fully configured `Item` ready for persistence

**Benefit:** If rarity rules change, only `ItemFactory.java` needs updating.

---

## ❓ COMMON VIVA QUESTIONS (ALL MEMBERS MUST KNOW)

| Question | Answer |
|---|---|
| What does `@SpringBootApplication` do? | Combines `@Configuration`, `@EnableAutoConfiguration`, `@ComponentScan` — bootstraps the entire Spring context. |
| What is ORM / Hibernate? | Object-Relational Mapping. Hibernate maps Java classes to DB tables. `@Entity` = table, field = column, `@Id` = primary key. |
| What is Spring Data JPA? | An abstraction over JPA. Extending `JpaRepository<T, ID>` auto-generates `findAll()`, `findById()`, `save()`, `delete()` — no SQL needed. |
| What is Thymeleaf? | A server-side Java template engine. HTML files in `templates/` folder have `th:` attributes that Spring fills with model data before sending to browser. |
| What is a DTO? | Data Transfer Object. Carries data between layers (e.g., form → controller). Keeps entities clean. Prevents mass assignment vulnerabilities. |
| What is `@Transactional`? | Wraps the method in a DB transaction. All DB changes succeed or all roll back together. Prevents partial updates. |
| What is the difference between `@OneToMany` and `@ManyToOne`? | `@OneToMany` = "I have many of these." `@ManyToOne` = "Many of me belong to one of those." `@JoinColumn` always goes on the `@ManyToOne` side (FK in that table). |
| What is `CascadeType.ALL`? | Propagates all JPA operations (persist, merge, remove, refresh, detach) to child entities. Delete parent → delete all children. |
| What is `mappedBy`? | Tells JPA "the other side manages this relationship's FK column." The side with `mappedBy` is the **inverse** side — no FK column here. |
| What is `@GeneratedValue(strategy = GenerationType.IDENTITY)`? | Delegates ID generation to the DB engine's auto-increment. MySQL assigns the next available integer on INSERT. |
| What is the Factory Method pattern? | A creational pattern where object construction is delegated to a factory class/method. Controllers request objects; factory decides how to build them. |
| What is MVC? | Model-View-Controller. Model = data; View = presentation; Controller = coordination layer between them. Each layer has one concern. |
| Why store sessions in MySQL via Spring Session JDBC? | HTTP sessions are stateful. Storing in MySQL means sessions survive server restarts. Without it, all logins are lost on redeploy. |

---

## 🗂️ FILES CREATED — QUICK REFERENCE

| File | Member | Purpose |
|---|---|---|
| `demo_script_906.md` | **906** | Achievement, MultiplayerSession, Level + High Cohesion |
| `demo_script_913.md` | **913** | PlayerSession, Rank, PlayerAchievement + Information Expert |
| `demo_script_387.md` | **387** | Player, Game, PlayerItem + Controller principle |
| `demo_script_366.md` | **366** | Admin, Item + SRP + Factory Method Demo |
| `project_overview_checklist.md` | **ALL** | Master checklist, full architecture, viva prep |
| `README.md` | **ALL** | Project setup instructions + principle documentation |

---

## ⏰ DEMO DAY TIMELINE (Suggested 10-12 min total)

```
0:00 - 1:00   → Screen sharer runs app (mvn spring-boot:run)
1:00 - 2:30   → 387 introduces project: "What is it? MVC overview."
2:30 - 4:00   → 387 demos Registration + explains Player/Game/Controller GRASP
4:00 - 5:30   → 366 demos Add Item + explains Factory Method + SRP
5:30 - 7:00   → 906 demos Add Session + explains Achievement/Level/High Cohesion
7:00 - 8:30   → 913 demos Leaderboard + explains Rank/PlayerSession/Info Expert
8:30 - 9:30   → Any member shows class diagram + maps to code
9:30 - 10:00  → Any remaining Q&A or live code pointed out
```

---

> **⚠️ Important:** Each member should read ONLY their own `demo_script_XXX.md` deeply, but skim all others. Viva questions can be asked to any team member about the overall project!
