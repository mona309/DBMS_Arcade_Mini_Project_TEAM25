# 🎮 Demo Script — Member 387
### **Your Classes:** `Game`, `Player`, `PlayerItem`

---

## 🧭 SECTION 1: Your Role in the Project (Say This First)

> *"I am responsible for the **core user identity and game catalog** of our Online Arcade Management System. My three classes — `Player`, `Game`, and `PlayerItem` — are the foundation everything else is built upon. A `Player` is the central user entity who logs in, earns scores, and owns items. A `Game` is the catalog of available titles players can compete in. `PlayerItem` is the bridge that records which items a player has in their inventory. Without these three entities, the entire system has nothing to operate on."*

---

## 🏗️ SECTION 2: Full Project Overview (Know This for Viva)

### What is this project?
An **Online Arcade Game Management System** — a full-stack Java web application that allows players to register, log in, play multiplayer games, earn achievements, collect items, and climb a leaderboard. The entire system is backed by MySQL with Hibernate ORM for relational data management.

### Tech Stack
| Layer | Technology |
|---|---|
| Backend Framework | Spring Boot 3.x |
| ORM | Hibernate / Spring Data JPA |
| Frontend Templates | Thymeleaf |
| Database | MySQL (`arcade_db`) |
| Build Tool | Maven |
| Session Storage | Spring Session JDBC (sessions stored in DB) |

### MVC Architecture (point to directory structure)
```
controller/   ← HTTP routing layer (PlayerController, GameController...)
service/      ← Business logic interfaces
service/impl/ ← Business logic implementations (PlayerServiceImpl...)
model/        ← JPA Entity classes (your Java-to-DB mapping)
repository/   ← Spring Data JPA interfaces (auto SQL)
dto/          ← Data Transfer Objects (form data, no DB mapping)
factory/      ← ItemFactory (Creational Pattern)
exception/    ← GlobalExceptionHandler, PlayerNotFoundException
```

### Database Relationships (Your Entities)
```
player >─── playeritem ───< item        (player can own many items)
player ──< playersession >── multiplayersession
player >── ranks
game ──< level
game ──< multiplayersession
```

---

## 🗂️ SECTION 3: Your Classes — Full Code Walkthrough

### 3.1 — `Player.java` (model)
**File:** `src/main/java/com/arcade/management/model/Player.java`

```java
@Entity @Table(name = "player") @Data @NoArgsConstructor @AllArgsConstructor
public class Player {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerID;
    @Column(nullable = false, unique = true, length = 50)
    private String username;
    @Column(nullable = false, unique = true, length = 100)
    private String email;
    private LocalDate registrationDate;
    @Column(nullable = false)
    private Integer totalScore = 0;
    @Column(nullable = false)
    private String password;
    @Column(length = 100)
    private String avatar;
    @ManyToOne @JoinColumn(name = "rankID")
    private Rank rank;
    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL)
    private List<PlayerAchievement> achievements;
    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL)
    private List<PlayerItem> items;
    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL)
    private List<PlayerSession> sessions;
}
```

**What to say:**
> *"The `Player` class is the **central hub** of our system — every other entity relates back to it. Let me walk through each annotation. `@Entity` tells Hibernate this is a persistent database entity. `@Table(name='player')` maps it to the `player` MySQL table. `@Data` from Lombok auto-generates getters, setters, `equals()`, and `hashCode()` — saving us 80 lines of boilerplate. `@NoArgsConstructor @AllArgsConstructor` generates the two constructors Hibernate and Spring need.*
>
> *The `username` and `email` columns are marked `unique = true` — MySQL enforces no duplicate usernames or emails at the database constraint level. `registrationDate` is a `LocalDate` — just date, no time. `totalScore` defaults to 0 for new players.*
>
> *The `@ManyToOne` to `Rank` means many players can share the same rank. `@JoinColumn(name='rankID')` places the `rankID` foreign key IN the `player` table.*
>
> *The three `@OneToMany` with `cascade = CascadeType.ALL` mean: if a Player is deleted, ALL their achievements, items, and sessions are automatically deleted too — no orphan records.*"

---

### 3.2 — `Game.java` (model)
**File:** `src/main/java/com/arcade/management/model/Game.java`

```java
@Entity @Table(name = "game") @Data @NoArgsConstructor @AllArgsConstructor
public class Game {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer gameID;
    @Column(length = 100)
    private String title;
    @Column(length = 50)
    private String genre;
    private Integer maxPlayers;
    private LocalDate releaseDate;
    @OneToMany(mappedBy = "game")
    private List<Level> levels;
    @OneToMany(mappedBy = "game")
    private List<MultiplayerSession> sessions;
}
```

**What to say:**
> *"The `Game` class is the **game catalog**. It stores a game's title, genre (Action/RPG/Puzzle), max player capacity, and release date. The two `@OneToMany` relationships mean: one game can have many `Level`s (the progression stages within that game) AND many `MultiplayerSession` lobbies (players can create multiple sessions to play the same game). The `mappedBy` on both sides means the FK is maintained by `Level.game` and `MultiplayerSession.game` respectively — Game itself doesn't hold any FK."*

---

### 3.3 — `PlayerItem.java` (model)
**File:** `src/main/java/com/arcade/management/model/PlayerItem.java`

```java
@Entity @Table(name = "playeritem") @Data @NoArgsConstructor @AllArgsConstructor
public class PlayerItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerItemID;
    @ManyToOne @JoinColumn(name = "playerID")
    private Player player;
    @ManyToOne @JoinColumn(name = "itemID")
    private Item item;
    private LocalDate acquiredDate;
}
```

**What to say:**
> *"`PlayerItem` is a **bridge/junction table** between `Player` and `Item`. A player can own many items, and the same item type can be owned by many players — that's a many-to-many relationship. By creating `PlayerItem` as a separate entity (rather than a plain join table), we can attach extra data like `acquiredDate` — recording exactly when the player acquired this item. Both `@ManyToOne` relationships store FKs (`playerID` and `itemID`) in the `playeritem` table."*

---

### 3.4 — `PlayerController.java` — Full HTTP Flow
**File:** `src/main/java/com/arcade/management/controller/PlayerController.java`

```java
@Controller @RequestMapping("/players")
public class PlayerController {
    @Autowired private PlayerService playerService;

    @GetMapping("/register")
    public String showRegistrationForm(Model model) {
        model.addAttribute("playerDTO", new PlayerDTO());
        return "players/register";      // renders register.html
    }

    @PostMapping("/register")
    public String registerPlayer(@Valid @ModelAttribute PlayerDTO playerDTO,
                                  BindingResult result, Model model) {
        if (result.hasErrors()) return "players/register";
        try {
            playerService.registerPlayer(playerDTO);
            return "redirect:/players?success";
        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
            return "players/register";
        }
    }

    @GetMapping("/leaderboard")
    public String showLeaderboard(Model model) {
        model.addAttribute("leaderboard", playerService.getLeaderboard(10));
        return "players/leaderboard";
    }
}
```

**What to say:**
> *"This is the **MVC Controller** for Player. When a user visits `/players/register` (GET), we push an empty `PlayerDTO` into the Thymeleaf model so the HTML form can bind to it. When they submit (POST), `@Valid` triggers Bean Validation on the DTO fields. `BindingResult` captures any validation errors — if there are errors, we return the form again without saving. If validation passes, we call `playerService.registerPlayer()`. Notice the controller has **zero business logic** — it only routes. All duplicate username checking happens in `PlayerServiceImpl`."*

---

### 3.5 — `PlayerServiceImpl.java` — Registration Flow

```java
@Override
public Player registerPlayer(PlayerDTO playerDTO) {
    if (playerRepository.findByUsername(playerDTO.getUsername()).isPresent())
        throw new IllegalArgumentException("Username already exists");
    if (playerRepository.findByEmail(playerDTO.getEmail()).isPresent())
        throw new IllegalArgumentException("Email already exists");
    Player player = new Player();
    player.setUsername(playerDTO.getUsername());
    player.setEmail(playerDTO.getEmail());
    player.setPassword(playerDTO.getPassword());
    player.setRegistrationDate(LocalDate.now());
    player.setTotalScore(0);
    player.setAvatar(playerDTO.getAvatar());
    Rank bronzeRank = rankRepository.findById(1).orElseThrow(...);
    player.setRank(bronzeRank);
    return playerRepository.save(player);
}
```

**What to say:**
> *"In `registerPlayer()`, we first check both username AND email uniqueness by querying the DB. If either exists, we throw an `IllegalArgumentException` that the controller catches and displays. New players always start with `totalScore=0` and are assigned Bronze rank (ID=1 in the rank table). Finally `playerRepository.save(player)` triggers a SQL INSERT via Hibernate. The `PlayerDTO` (Data Transfer Object) is what carries form data — it keeps the raw `Player` entity clean from HTTP concerns."*

---

## 🎓 SECTION 4: Your Design Principle — **Controller** (GRASP)

### What is GRASP Controller?
> The **Controller** principle says: when external input arrives (like an HTTP request), it should be handled by a dedicated class that acts as the **UI-to-business-logic boundary**. This class does NOT perform business logic itself — it just intercepts, validates form data, and delegates.

### Where is it in YOUR code?

**Point to:** `PlayerController.java` and `GameController.java`

**Say:**
> *"Look at `PlayerController`. Its ONLY job is to:*
> *1. Catch HTTP requests at `/players/...`*
> *2. Read data from the request (via `@ModelAttribute PlayerDTO`)*
> *3. Delegate ALL logic to `PlayerService`*
> *4. Return a view name to Thymeleaf*
>
> *It does NOT check if a username is duplicate. It does NOT assign the rank. It does NOT build the SQL INSERT. Those are all in `PlayerServiceImpl`. The Controller is the **traffic cop** — it directs traffic but doesn't drive the cars. This perfectly implements the GRASP Controller principle: external I/O handling is centralized in one entry point per domain, completely separated from business logic."*

---

### 🔧 SECTION 5: Your Design Pattern — **Factory Method** (Creational — also yours to demo!)

**File:** `src/main/java/com/arcade/management/factory/ItemFactory.java`

```java
public class ItemFactory {
    public static Item createItem(String name, String type, String rarity) {
        switch (type.toLowerCase()) {
            case "weapon":     return createWeapon(name, rarity);
            case "consumable": return createConsumable(name, rarity);
            case "armor":      return createArmor(name, rarity);
            default:           return createGenericItem(name, type, rarity);
        }
    }
    private static Item createWeapon(String name, String rarity) {
        Item w = new Item();
        w.setItemName(name); w.setItemType("Weapon");
        w.setRarity((rarity == null || rarity.isEmpty()) ? "Uncommon" : rarity);
        return w;
    }
    // Similar for Consumable (default: Common), Armor (default: Rare)
}
```

**Used in `ItemController`:**
```java
@PostMapping("/add")
public String addItem(@ModelAttribute Item itemForm) {
    Item processedItem = ItemFactory.createItem(
        itemForm.getItemName(), itemForm.getItemType(), itemForm.getRarity()
    );
    itemService.addItem(processedItem);
    return "redirect:/items?success";
}
```

**What to say:**
> *"Our team implemented the **Factory Method** creational design pattern in `ItemFactory`. When a user submits the 'Add Item' form, the `ItemController` does NOT call `new Item()` directly. Instead it calls `ItemFactory.createItem()`. The factory decides the construction details based on item type — Weapons get 'Uncommon' as their default rarity if the user left it blank. This **centralizes all object creation rules** in one class. Tomorrow if we add 30 new item types, we only modify `ItemFactory` — zero changes to the controller. This follows the Open/Closed Principle too."*

---

## ✅ SECTION 6: Viva Q&A — Be Ready for These

| Question | Answer |
|---|---|
| What is `@Entity`? | Marks a class as a JPA entity — Hibernate will map it to a DB table. |
| What is `@Column(nullable=false, unique=true)`? | Adds DB constraints: cannot be NULL, must be unique. Hibernate generates `NOT NULL UNIQUE` in the DDL. |
| What is a DTO? Why use it? | Data Transfer Object — carries raw form data without DB annotations. Keeps the entity clean. Also prevents over-posting attacks (attacker can't set `totalScore` from a form). |
| What is `CascadeType.ALL`? | Parent-child propagation. Delete a Player → cascade deletes all their PlayerAchievements, PlayerItems, and PlayerSessions automatically. |
| Why does `PlayerItem` exist instead of just a join table? | Because we store `acquiredDate` — extra attribute on the relationship. Simple join tables can't hold extra columns. |
| What is GRASP Controller? | A principle that says one class should act as the UI-to-logic boundary, handling external events. It centralizes input handling without containing business logic. |
| What does `@Valid` do? | Triggers JSR-303 Bean Validation on the DTO. `@NotNull`, `@Size`, etc. annotations on DTO fields are validated automatically. |
| How does the leaderboard work? | `playerRepository.findTop10ByOrderByTotalScoreDesc()` — Spring Data auto-generates `SELECT * FROM player ORDER BY totalScore DESC LIMIT 10`. |
| What does `redirect:/players?success` do? | HTTP 302 redirect. Prevents form re-submission on browser refresh (POST-Redirect-GET pattern). |
