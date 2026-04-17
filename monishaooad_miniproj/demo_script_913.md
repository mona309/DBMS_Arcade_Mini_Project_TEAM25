# 🎮 Demo Script — Member 913
### **Your Classes:** `PlayerSession`, `Rank`, `PlayerAchievement`

---

## 🧭 SECTION 1: Your Role in the Project (Say This First)

> *"I am responsible for the **player progression and reward system** of our Online Arcade Management System. My three classes — `PlayerSession`, `Rank`, and `PlayerAchievement` — form the core of **how a player grows over time**. When a player completes a game, their session score is recorded in `PlayerSession`. That score triggers a rank evaluation using `Rank` thresholds. And when they hit milestones, `PlayerAchievement` permanently records that badge on their profile."*

---

## 🏗️ SECTION 2: Full Project Overview (Know This for Viva)

### What is this project?
An **Online Arcade Game Management System** — a full-stack Java Spring Boot web application backed by MySQL. It manages players, games, levels, multiplayer sessions, items, achievements, and admin users — all connected via a relational database with Hibernate ORM.

### Architecture — MVC Pattern
```
Browser (User)
   ↓ HTTP Request
[Controller Layer]   ← Receives HTTP GET/POST, reads form data, delegates
   ↓ delegates to
[Service Layer]      ← Contains all business logic (checking ranks, unlocking achievements)
   ↓ calls
[Repository Layer]   ← Spring Data JPA; automatically generates SQL
   ↓ persists to
[MySQL Database]     ← arcade_db
```

### Database Relationships (Your Entities)
```
player ──< playersession >── multiplayersession
player ──< playerachievement >── achievement
player >── ranks
```
- `PlayerSession`: Many players can join many sessions (bridge table)
- `PlayerAchievement`: Many players can earn many achievements (bridge table)
- `Rank`: One rank is assigned to many players (e.g., Bronze → Silver → Gold)

---

## 🗂️ SECTION 3: Your Classes — Full Code Walkthrough

### 3.1 — `Rank.java` (model)
**File:** `src/main/java/com/arcade/management/model/Rank.java`

```java
@Entity @Table(name = "ranks") @Data @NoArgsConstructor @AllArgsConstructor
public class Rank {
    @Id
    private Integer rankID;          // NOT auto-generated — manually seeded (1=Bronze, 2=Silver, 3=Gold)
    @Column(length = 50)
    private String rankName;         // "Bronze", "Silver", "Gold", "Platinum"
    private Integer rankScore;       // Minimum score threshold to qualify
    @OneToMany(mappedBy = "rank")
    private List<Player> players;    // All players currently at this rank
}
```

**What to say:**
> *"The `Rank` entity has a **manually assigned ID** (notice there's no `@GeneratedValue`) — this is because ranks are pre-seeded data. Bronze=1 at score 0, Silver=2 at 500, Gold=3 at 1000, Platinum=4 at 5000. The `rankScore` field is the **minimum total score** needed. The `@OneToMany` relationship means one rank (like Bronze) can have many players assigned to it, while on the `Player` side there is a `@ManyToOne` to this `Rank`. This is a clean one-to-many navigable from the rank side."*

---

### 3.2 — `PlayerSession.java` (model)
**File:** `src/main/java/com/arcade/management/model/PlayerSession.java`

```java
@Entity @Table(name = "playersession") @Data @NoArgsConstructor @AllArgsConstructor
public class PlayerSession {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerSessionID;
    @ManyToOne @JoinColumn(name = "sessionID")
    private MultiplayerSession session;   // Which lobby/session this entry belongs to
    @ManyToOne @JoinColumn(name = "playerID")
    private Player player;                // Which player participated
    private Integer score;                // Score earned in this specific session
    private Integer position;             // Final rank/position in the match (1st, 2nd, 3rd...)
}
```

**What to say:**
> *"`PlayerSession` is a **junction/bridge table** that resolves the many-to-many relationship between `Player` and `MultiplayerSession`. A many-to-many means Player X can join Session A AND Session B, while Session A can have Player X AND Player Y. We decompose this with a linking entity that adds extra meaningful attributes: `score` (how much they scored in that session) and `position` (their finishing rank). The two `@ManyToOne` with `@JoinColumn` annotations place the foreign keys `sessionID` and `playerID` directly in the `playersession` table."*

---

### 3.3 — `PlayerAchievement.java` (model)
**File:** `src/main/java/com/arcade/management/model/PlayerAchievement.java`

```java
@Entity @Table(name = "playerachievement") @Data @NoArgsConstructor @AllArgsConstructor
public class PlayerAchievement {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerAchievementID;
    @ManyToOne @JoinColumn(name = "playerID")
    private Player player;
    @ManyToOne @JoinColumn(name = "achievementID")
    private Achievement achievement;
    private LocalDate dateEarned;         // When the player unlocked this achievement
}
```

**What to say:**
> *"`PlayerAchievement` is another bridge table — this one links `Player` to `Achievement`. The table stores WHICH player earned WHICH achievement and WHEN (`dateEarned`). This is a standard **decomposition of a many-to-many** relationship. The `Achievement` table itself is a **catalog** (e.g., 'Speed Runner' achievement exists as a concept), while `PlayerAchievement` is the **evidence record** proving Player X earned it on a specific date."*

---

### 3.4 — `PlayerServiceImpl.java` — The Core Business Logic
**File:** `src/main/java/com/arcade/management/service/impl/PlayerServiceImpl.java`

**Focus on: `updatePlayerScore()` and `checkAndUpdateRank()`**

```java
@Override
public void updatePlayerScore(Integer playerId, Integer additionalScore) {
    Player player = getPlayerById(playerId);
    player.setTotalScore(player.getTotalScore() + additionalScore);
    playerRepository.save(player);
    checkAndUpdateRank(playerId);           // ← triggers automatic rank upgrade
}

private void checkAndUpdateRank(Integer playerId) {
    Player player = getPlayerById(playerId);
    List<Rank> ranks = rankRepository.findAll(Sort.by(Sort.Direction.DESC, "rankScore"));
    for (Rank rank : ranks) {
        if (player.getTotalScore() >= rank.getRankScore()) {
            player.setRank(rank);
            playerRepository.save(player);
            break;
        }
    }
}
```

**What to say:**
> *"This is the most important business logic in my section. When a player's score is updated, `updatePlayerScore()` first adds the new score then immediately calls `checkAndUpdateRank()`. That private method fetches all ranks from the DB **sorted in descending order by score threshold** (Platinum first, then Gold, then Silver, then Bronze). It loops and finds the FIRST rank where the player's total score is at or above the threshold — that's the highest rank they qualify for. This is clean, self-contained scoring logic."*

---

### 3.5 — Repository Layer
**File:** `src/main/java/com/arcade/management/repository/RankRepository.java`

```java
public interface RankRepository extends JpaRepository<Rank, Integer> { }
```

**What to say:**
> *"The `RankRepository` is a Spring Data JPA interface. By extending `JpaRepository<Rank, Integer>`, we immediately get: `findAll()`, `findById()`, `save()`, `delete()` — **without writing a single line of SQL**. Spring generates a proxy implementation at runtime. We also use `rankRepository.findAll(Sort.by(Sort.Direction.DESC, "rankScore"))` — Spring Data auto-translates this into `ORDER BY rankScore DESC` in SQL."*

---

## 🎓 SECTION 4: Your Design Principle — **Information Expert** (GRASP)

### What is Information Expert?
> Information Expert says: **assign a responsibility to the class that has the most information needed to fulfill that responsibility.** Don't put the logic in a random place — put it where the data lives.

### Where is it in YOUR code?

**Point to:** `PlayerServiceImpl.java` — specifically `checkAndUpdateRank()`

**Say:**
> *"When a player finishes a game and gains score, WHO should decide whether they get promoted to Gold rank? The UI Controller? No — that's just for routing. The database? No — it just stores data. The `PlayerServiceImpl` should, because it holds the player's `totalScore` AND it has direct access to `RankRepository` for fetching thresholds. It is the **Information Expert** — it has ALL the information needed: the player's score AND the rank criteria. So the rank evaluation logic naturally belongs here. If we had put this logic in the Controller, it would violate Information Expert because the Controller doesn't 'own' the data."*

---

## 🔧 SECTION 5: Your Design Pattern — **Factory Method** (Project-Wide — Know for Viva)

**Where to point:** `ItemFactory.java` — explain that this is the project's shared creational pattern

**Say:**
> *"Our team applied the **Factory Method** design pattern. The `ItemFactory.createItem(name, type, rarity)` method centralizes item construction. Depending on the type string — 'Weapon', 'Consumable', or 'Armor' — it calls a corresponding private method with pre-set default rarities. This ensures that the `ItemController` never has to know the business rules of item rarity defaults. All creation knowledge is encapsulated in the factory — a perfect example of the **Creator** GRASP principle too."*

---

## ✅ SECTION 6: Viva Q&A — Be Ready for These

| Question | Answer |
|---|---|
| What is `@ManyToOne`? | Multiple `PlayerSession` records map to one `MultiplayerSession`. FK `sessionID` lives in the `playersession` table. |
| Why is `PlayerAchievement` its own entity and not a simple list? | Because we need to store **extra data** (like `dateEarned`) alongside the relationship, which a simple join table can't do. |
| What does `Sort.by(Sort.Direction.DESC, "rankScore")` do? | Generates `ORDER BY rankScore DESC` SQL, so we evaluate the highest rank threshold first. |
| Why does `Rank` not use `@GeneratedValue`? | Ranks are fixed seed data. Manual IDs (1,2,3,4) make them predictable and easy to reference (rank 1 = Bronze always). |
| What is GRASP Information Expert? | Assign a task to the class that already has the data it needs. Don't fetch data somewhere else to do work. |
| What if a player's score drops? | Currently scores only increase. A future extension could re-evaluate downward, but the current `checkAndUpdateRank()` handles upward promotions. |
| What is `@Transactional`? | Ensures the entire service method executes as one atomic unit. Save score + update rank = one transaction. If the rank update fails, score save also rolls back. |
| What is the difference between `PlayerSession` and `MultiplayerSession`? | `MultiplayerSession` = the game lobby (one entity). `PlayerSession` = one player's participation record inside that lobby (many records per lobby). |
