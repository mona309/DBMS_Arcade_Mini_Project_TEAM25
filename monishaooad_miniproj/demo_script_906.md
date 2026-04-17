# 🎮 Demo Script — Member 906
### **Your Classes:** `Achievement`, `MultiplayerSession`, `Level`

---

## 🧭 SECTION 1: Your Role in the Project (Say This First)

> *"I am responsible for the **game configuration and session infrastructure** of our Online Arcade Management System. Specifically, my three classes — `Achievement`, `MultiplayerSession`, and `Level` — form the backbone of **what a game is structured like** and **how players engage in it together**. Without my entities, there are no defined game levels to progress through, no lobby sessions to join, and no achievements to earn."*

---

## 🏗️ SECTION 2: Full Project Overview (Know This for Viva)

### What is this project?
An **Online Arcade Game Management System** — a full-stack Java web application using:
- **Spring Boot** (backend framework)
- **Hibernate / JPA** (ORM — connects Java objects to MySQL tables)
- **Thymeleaf** (server-side HTML rendering)
- **MySQL** (relational database)
- **Maven** (build tool)

### Architecture — MVC Pattern
```
Browser (User)
   ↓ HTTP Request
[Controller Layer]   ← PlayerController, GameController, SessionController, etc.
   ↓ delegates to
[Service Layer]      ← PlayerServiceImpl, SessionServiceImpl, AchievementServiceImpl, etc.
   ↓ calls
[Repository Layer]   ← Spring Data JPA interfaces (auto-generated SQL)
   ↓ persists to
[MySQL Database]     ← arcade_db (tables: player, game, level, achievement, multiplayersession...)
```

### Complete Entity Map
| Entity | Table | Owned By |
|---|---|---|
| `Player` | `player` | 387 |
| `Game` | `game` | 387 |
| `PlayerItem` | `playeritem` | 387 |
| `PlayerSession` | `playersession` | 913 |
| `Rank` | `ranks` | 913 |
| `PlayerAchievement` | `playerachievement` | 913 |
| `Achievement` | `achievement` | **906** ✅ |
| `MultiplayerSession` | `multiplayersession` | **906** ✅ |
| `Level` | `level` | **906** ✅ |
| `Admin` | `admin` | 366 |
| `Item` | `item` | 366 |

---

## 🗂️ SECTION 3: Your Classes — Full Code Walkthrough

### 3.1 — `Achievement.java` (model)
**File:** `src/main/java/com/arcade/management/model/Achievement.java`

```java
@Entity @Table(name = "achievement") @Data @NoArgsConstructor @AllArgsConstructor
public class Achievement {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer achievementID;
    @Column(length = 100)
    private String name;
    @Column(length = 255)
    private String description;
    @OneToMany(mappedBy = "achievement")
    private List<PlayerAchievement> playerAchievements;
}
```

**What to say:**
> *"The `Achievement` class is a **JPA Entity** — the `@Entity` annotation tells Hibernate to map it to the `achievement` MySQL table. Each achievement has an `achievementID` (auto-generated primary key), a `name` (like 'First Win' or 'Speed Runner'), and a `description`. The `@OneToMany` relationship links this to `PlayerAchievement` — meaning one achievement can be unlocked by MANY players. The `mappedBy = "achievement"` tells Hibernate that the foreign key lives on the `PlayerAchievement` side, NOT here."*

---

### 3.2 — `MultiplayerSession.java` (model)
**File:** `src/main/java/com/arcade/management/model/MultiplayerSession.java`

```java
@Entity @Table(name = "multiplayersession") @Data @NoArgsConstructor @AllArgsConstructor
public class MultiplayerSession {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer sessionID;
    @ManyToOne @JoinColumn(name = "gameID")
    private Game game;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    @OneToMany(mappedBy = "session")
    private List<PlayerSession> playerSessions;
}
```

**What to say:**
> *"A `MultiplayerSession` represents a **live game lobby**. Many sessions can exist for one `Game` (`@ManyToOne` with `@JoinColumn(name = "gameID")`). It tracks `startTime` and `endTime` using Java's `LocalDateTime`. The `@OneToMany` to `PlayerSession` means multiple players (with their individual scores and positions) are linked to this single session lobby. This is the **junction point** between a game event and individual player performance."*

---

### 3.3 — `Level.java` (model)
**File:** `src/main/java/com/arcade/management/model/Level.java`

```java
@Entity @Table(name = "level") @Data @NoArgsConstructor @AllArgsConstructor
public class Level {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer levelID;
    @ManyToOne @JoinColumn(name = "gameID")
    private Game game;
    private Integer levelNumber;
    @Column(length = 20)
    private String difficulty;    // "Easy", "Medium", "Hard"
    @Column(length = 255)
    private String description;
}
```

**What to say:**
> *"A `Level` belongs to a `Game` (via `@ManyToOne`). Each level records its number (1, 2, 3...), its difficulty, and a text description. This lets us define the **progression ladder** within a game. For example, Game 'SpaceWars' could have Level 1 as Easy and Level 5 as Hard. The `@JoinColumn(name = "gameID")` means the `level` table has a `gameID` foreign key column pointing to the `game` table."*

---

### 3.4 — `AchievementController.java`
**File:** `src/main/java/com/arcade/management/controller/AchievementController.java`

**What to say:**
> *"The `AchievementController` handles HTTP routes under `/achievements`. When a browser hits GET `/achievements`, the controller calls `achievementService.getAllAchievements()` and puts the list into the Thymeleaf model. It **never does any business logic itself** — it purely routes the request to the service. This is the classic **MVC Controller** role."*

---

### 3.5 — `AchievementServiceImpl.java`
**File:** `src/main/java/com/arcade/management/service/impl/AchievementServiceImpl.java`

```java
@Service @Transactional
public class AchievementServiceImpl implements AchievementService {
    @Autowired private AchievementRepository achievementRepository;
    @Override public Achievement addAchievement(Achievement a) { return achievementRepository.save(a); }
    @Override public Achievement getAchievementById(Integer id) { 
        return achievementRepository.findById(id).orElseThrow(() -> new RuntimeException("Achievement not found: " + id));
    }
    @Override public List<Achievement> getAllAchievements() { return achievementRepository.findAll(); }
    @Override public void deleteAchievement(Integer id) { achievementRepository.delete(getAchievementById(id)); }
}
```

**What to say:**
> *"`AchievementServiceImpl` **implements** the `AchievementService` interface. `@Service` marks it as a Spring bean. `@Transactional` ensures every database operation is wrapped in a transaction — if anything fails, the whole operation rolls back. It delegates all actual DB work to `AchievementRepository` which is a Spring Data JPA interface."*

---

### 3.6 — `SessionController.java` — Full Flow
**File:** `src/main/java/com/arcade/management/controller/SessionController.java`

**What to say:**
> *"The `SessionController` manages the `/sessions` endpoint. When a POST comes in to create a session, it reads `gameId`, `startTime`, and `endTime` from the form. It uses `Optional` to safely handle blank time inputs — if blank, it defaults to `now()` and `now() + 30 minutes`. The built `MultiplayerSession` object is then passed to `sessionService.createSession()`. This shows clean **null-safe defensive coding**."*

---

## 🎨 SECTION 4: Your Design Principle — **High Cohesion** (GRASP)

### What is High Cohesion?
> High Cohesion means: **each class should have a narrow, well-defined purpose**. A class with high cohesion does ONE thing and does it well. The opposite is a "God Class" that does everything.

### Where is it in YOUR code?

**Point to the service layer packages:**
```
service/
├── AchievementService.java         ← Only handles achievements
├── impl/AchievementServiceImpl.java
├── SessionService.java             ← Only handles session lifecycle
├── impl/SessionServiceImpl.java
├── GameService.java                ← Only handles game catalog
├── impl/GameServiceImpl.java
```

**Say:**
> *"Notice how each service class has exactly ONE responsibility. `AchievementServiceImpl` only does CRUD on achievements — it has `addAchievement`, `getAchievementById`, `getAllAchievements`, `deleteAchievement`. That's it. It doesn't touch ranks or player scores. `SessionServiceImpl` only manages the lifecycle of `MultiplayerSession` objects — it doesn't care about achievements. This is High Cohesion. Because of this separation, if tomorrow the achievement unlocking rules change, I only modify `AchievementServiceImpl`. Nothing else breaks."*

---

## 🔧 SECTION 5: Your Design Pattern — **Factory Method** (Creational Pattern — shared project pattern)

> *(Note: The Factory is demonstrated by 366 on `Item`, but **you must know and be able to explain the overall Factory pattern** as it's a project-wide pattern.)*

**Where to point:** `src/main/java/com/arcade/management/factory/ItemFactory.java`

**Say:**
> *"Our team implemented the **Factory Method** creational design pattern. Rather than letting controllers directly instantiate Item objects with `new Item()`, we centralized creation in `ItemFactory.createItem(name, type, rarity)`. The factory has private static methods for each type: `createWeapon()` applies 'Uncommon' as default rarity, `createConsumable()` defaults to 'Common', `createArmor()` defaults to 'Rare'. This ensures **business rules for object creation are never scattered across the UI layer** — they're locked inside one trusted factory."*

---

## ✅ SECTION 6: Viva Q&A — Be Ready for These

| Question | Answer |
|---|---|
| What is `@ManyToOne`? | Many `Level`s belong to one `Game`. The foreign key `gameID` lives in the `level` table. |
| What is `@OneToMany(mappedBy=...)`? | The inverse side. No FK column here; the FK is managed by the other entity. |
| Why use `LocalDateTime`? | It stores both date and time (timestamp) in one field — perfect for session start/end. |
| What does `@Transactional` do? | Wraps all DB operations in a transaction. If any step fails, everything rolls back — ensures data consistency. |
| What is GRASP High Cohesion? | A design guideline where each class is focused on a single bounded responsibility. Prevents "God Classes." |
| Difference between GRASP and SOLID? | GRASP is about assigning responsibilities between objects. SOLID is about writing classes that are robust and maintainable over time. |
| What does `@GeneratedValue(strategy = IDENTITY)` do? | Delegates ID generation to the database's auto-increment — MySQL assigns the ID automatically on insert. |
| Why is `Achievement` separate from `PlayerAchievement`? | `Achievement` is the **catalog** (e.g., "First Win" exists as a concept). `PlayerAchievement` is the **bridge** tracking WHICH player earned WHICH achievement. Classic many-to-many decomposition. |
