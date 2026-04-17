# 🎮 Demo Script — Member 366
### **Your Classes:** `Admin`, `Item`

---

## 🧭 SECTION 1: Your Role in the Project (Say This First)

> *"I am responsible for the **administrative control layer and item catalog system** of our Online Arcade Management System. My two classes — `Admin` and `Item` — form the privileged management tier. The `Admin` entity represents authorized personnel who manage the system, while `Item` is the catalog of in-game collectibles (weapons, armor, consumables) that players can acquire. More importantly, I implemented the **Factory Method design pattern** through `ItemFactory.java`, which is the only creational design pattern in our project."*

---

## 🏗️ SECTION 2: Full Project Overview (Know This for Viva)

### What is this project?
An **Online Arcade Game Management System** built with Spring Boot, Hibernate JPA, Thymeleaf, and MySQL. Players register/login, play multiplayer games, earn scores and ranks, collect items, and unlock achievements. Admins manage the system from a privileged backend.

### Architecture — MVC Pattern
```
Browser
   ↓
[Controller Layer]     ← AdminController, ItemController (YOUR code)
   ↓ delegates
[Service Layer]        ← AdminService, ItemService interfaces
   ↓ implements
[ServiceImpl Layer]    ← AdminServiceImpl, ItemServiceImpl
   ↓ calls
[Repository Layer]     ← AdminRepository, ItemRepository (Spring Data JPA)
   ↓
[MySQL Database]       ← admin table, item table
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
| `Achievement` | `achievement` | 906 |
| `MultiplayerSession` | `multiplayersession` | 906 |
| `Level` | `level` | 906 |
| `Admin` | `admin` | **366** ✅ |
| `Item` | `item` | **366** ✅ |

---

## 🗂️ SECTION 3: Your Classes — Full Code Walkthrough

### 3.1 — `Admin.java` (model)
**File:** `src/main/java/com/arcade/management/model/Admin.java`

```java
@Entity
@Table(name = "admin")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Admin implements Serializable {
    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer adminID;

    @Column(nullable = false, unique = true, length = 50)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false, length = 100)
    private String email;

    @Column(nullable = false)
    private String role = "SUPER_ADMIN";
}
```

**What to say:**
> *"`Admin` is a completely **separate JPA entity** from `Player`. Both have a username and password, but that's where the similarity ends. `Admin` has a `role` field (defaulting to 'SUPER_ADMIN'), while `Player` has gameplay data like `totalScore`, `rank`, achievements, and sessions. The `implements Serializable` with `serialVersionUID` is important because Spring Session JDBC serializes admin session objects into the database — without `Serializable`, session persistence would fail.*
>
> *Notice there is NO `@ManyToOne` to `Player` here. Admin and Player are **completely decoupled entities** — an admin is not a player with extra permissions. This is a deliberate design choice."*

---

### Why Not Just Add an `isAdmin` Flag to Player?

**This is a common viva question — be ready:**

> *"Initially it might seem simpler to add an `isAdmin = true` field to the `Player` table. But that would be a design mistake. Players have complex game data: `totalScore`, `avatar`, `rank`, `PlayerSession`, `PlayerAchievement`, `PlayerItem`. Admins need NONE of that. If we merged them, every admin row would have NULL in 6+ game-related columns — that's dirty data and poor separation of concerns. By having a separate `Admin` entity with its own table, controller, service, and repository, each class has **exactly one reason to change**: Admin changes only when admin authorization logic changes; Player changes only when gameplay logic changes. This is the Single Responsibility Principle."*

---

### 3.2 — `Item.java` (model)
**File:** `src/main/java/com/arcade/management/model/Item.java`

```java
@Entity @Table(name = "item") @Data @NoArgsConstructor @AllArgsConstructor
public class Item {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer itemID;
    @Column(length = 100)
    private String itemName;    // e.g., "Excalibur", "Health Potion"
    @Column(length = 50)
    private String itemType;    // "Weapon", "Consumable", "Armor"
    @Column(length = 50)
    private String rarity;      // "Common", "Uncommon", "Rare", "Epic"
    @OneToMany(mappedBy = "item")
    private List<PlayerItem> playerItems;  // which players own this item
}
```

**What to say:**
> *"The `Item` entity is the **global catalog** of all available in-game items. `itemName` is the display name, `itemType` categorizes it, and `rarity` indicates how rare it is. The `@OneToMany` to `PlayerItem` is the inverse side — it lets us query 'which players own this item?' without storing any FK here. The FK (`itemID`) lives in the `playeritem` table, managed by `PlayerItem.item`."*

---

### 3.3 — ⭐ `ItemFactory.java` — The Factory Method Pattern
**File:** `src/main/java/com/arcade/management/factory/ItemFactory.java`

```java
public class ItemFactory {

    public static Item createItem(String name, String type, String rarity) {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Item name cannot be null or empty");
        }
        switch (type.toLowerCase()) {
            case "weapon":     return createWeapon(name, rarity);
            case "consumable": return createConsumable(name, rarity);
            case "armor":      return createArmor(name, rarity);
            default:           return createGenericItem(name, type, rarity);
        }
    }

    private static Item createWeapon(String name, String rarity) {
        Item weapon = new Item();
        weapon.setItemName(name);
        weapon.setItemType("Weapon");
        weapon.setRarity((rarity == null || rarity.isEmpty()) ? "Uncommon" : rarity);
        return weapon;
    }

    private static Item createConsumable(String name, String rarity) {
        Item consumable = new Item();
        consumable.setItemName(name);
        consumable.setItemType("Consumable");
        consumable.setRarity((rarity == null || rarity.isEmpty()) ? "Common" : rarity);
        return consumable;
    }

    private static Item createArmor(String name, String rarity) {
        Item armor = new Item();
        armor.setItemName(name);
        armor.setItemType("Armor");
        armor.setRarity((rarity == null || rarity.isEmpty()) ? "Rare" : rarity);
        return armor;
    }

    private static Item createGenericItem(String name, String type, String rarity) {
        Item item = new Item();
        item.setItemName(name);
        item.setItemType(type);
        item.setRarity(rarity);
        return item;
    }
}
```

**What to say (step by step):**
> *"This is our project's **Factory Method creational design pattern**. Let me walk through it line by line.*
>
> *`createItem()` is the public entry point. It validates that the name isn't blank, then uses a `switch` on the item type to route to the appropriate private factory method.*
>
> *`createWeapon()` sets the type to 'Weapon' and applies the default rarity 'Uncommon' if the user submitted an empty rarity field. Similarly, `createConsumable()` defaults to 'Common' and `createArmor()` defaults to 'Rare'.*
>
> *Notice we are not extending any abstract class here — this is a **static factory**, which is a valid variant of the Factory Method pattern. The key benefit is: the `ItemController` calls `ItemFactory.createItem(name, type, rarity)` and receives a fully configured, business-rule-compliant `Item` object. The controller has ZERO knowledge of rarity defaults. All construction intelligence is centralized here.*"

---

### 3.4 — `ItemController.java` — How Factory is Used

```java
@Controller @RequestMapping("/items")
public class ItemController {
    @Autowired private ItemService itemService;

    @PostMapping("/add")
    public String addItem(@ModelAttribute Item itemForm) {
        // ← Factory intercepts the raw form data
        Item processedItem = ItemFactory.createItem(
            itemForm.getItemName(), itemForm.getItemType(), itemForm.getRarity()
        );
        itemService.addItem(processedItem);
        return "redirect:/items?success";
    }
}
```

**What to say:**
> *"Here you can see the factory in action. The form submits raw data — maybe the user typed 'Excalibur', 'Weapon', and left Rarity blank. The controller passes that raw data to `ItemFactory.createItem()`. The factory returns a properly configured `Item` with rarity = 'Uncommon'. The controller then calls `itemService.addItem()` with this clean, validated object. The controller never touches rarity business rules — that's the factory's job."*

---

### 3.5 — `AdminController.java`

```java
@Controller @RequestMapping("/admin")
public class AdminController {
    @Autowired private AdminService adminService;

    @GetMapping
    @ResponseBody
    public String adminHome() {
        return "Admin Control Panel is active. Endpoints available for managing Item DB...";
    }

    @GetMapping("/list")
    public String listAdmins(Model model) {
        List<Admin> admins = adminService.getAllAdmins();
        model.addAttribute("admins", admins);
        return "admin/list";
    }
}
```

**What to say:**
> *"The `AdminController` handles `/admin` endpoints. The `@ResponseBody` on `adminHome()` means it returns raw text directly, not a Thymeleaf view — useful for a quick health check. The `/admin/list` endpoint retrieves all admins via `AdminService` and passes them to the view. Notice `AdminController` never touches `PlayerService` or any game logic — it's completely isolated to admin operations."*

---

## 🎓 SECTION 4: Your Design Principle — **Single Responsibility Principle** (SOLID — SRP)

### What is SRP?
> **Every class should have ONE reason to change.** A class that does 10 things has 10 reasons to change — it's fragile. A class that does one thing is stable.

### Where is it in YOUR code?

**Primary Example:** `Admin.java` vs `Player.java` separation

**Say:**
> *"The clearest demonstration of SRP in my code is the decision to make `Admin` a completely separate entity from `Player`. On the surface they seem similar — both have username and password. But their reasons to change are totally different:*
>
> *— `Player` changes when: gameplay scoring changes, rank progression is modified, avatar storage rules change, etc.*
> *— `Admin` changes when: admin roles are restructured, new admin permissions are added, admin audit logging is required.*
>
> *By keeping them separate, each class has ONE reason to change. If we had merged them into one `User` class with a `role` flag, then adding a new admin permission AND modifying how player scores work would both modify the same class — violating SRP.*
>
> *This extends through the layers: `AdminController` only handles admin HTTP routes. `AdminService` only manages admin business logic. `AdminRepository` only queries the `admin` table. No class bleeds into another's responsibility."*

---

**Secondary Example:** `GlobalExceptionHandler.java` + `PlayerNotFoundException.java`

**Say:**
> *"Another SRP example is our `GlobalExceptionHandler`. It has exactly ONE responsibility: catching exceptions from any controller and translating them into user-friendly error responses. This logic doesn't live in the controller or service — it's extracted into its own class. `PlayerNotFoundException` has one responsibility: representing the 'player not found' error condition. Each class is laser-focused."*

---

## 🔧 SECTION 5: Your Design Pattern — **Factory Method (Creational)**

### Why do we need a Creational Pattern?
> *"In software, naively calling `new ClassName()` everywhere leads to scattered, hard-to-maintain object creation. If rules change (e.g., now Weapons should default to 'Rare' not 'Uncommon'), you'd have to search every file that calls `new Item()`. A Creational Pattern centralizes this."*

### How does our Factory Method solve this?
> *"`ItemFactory` is a **static factory class**. All item creation logic lives in ONE place. The `switch` statement is the **decision router** — based on type, it calls the correct private factory method. Each private method:*
> *1. Creates a new `Item` object*
> *2. Sets the type correctly*  
> *3. Applies a sensible default rarity if the user left it blank*
> *4. Returns the complete, configured object*
>
> *Tomorrow if we add 'Mount' as a new item type with a 'Legendary' default rarity, we add ONE case to the switch and ONE private method. Zero changes to `ItemController`, `ItemService`, or any other class. This is the Factory Method in action."*

---

## ✅ SECTION 6: Viva Q&A — Be Ready for These

| Question | Answer |
|---|---|
| Why does `Admin` implement `Serializable`? | Spring Session JDBC serializes session-stored objects into the database. Any object in the HTTP session must implement `Serializable` or deserialization will fail. |
| What is `serialVersionUID`? | A version stamp for serialization. If the class changes, the UID ensures the JVM won't mix up old and new serialized formats, preventing `InvalidClassException`. |
| Why is `ItemFactory` using static methods? | It's a stateless utility class — no instance variables needed. Static methods are appropriate for pure, deterministic transformation functions like this factory. |
| What is the Factory Method Pattern? | A creational pattern that centralizes object construction logic. Instead of scattered `new` calls, one factory method is responsible for creating configured objects. |
| What is the difference between Factory Method and Abstract Factory? | Factory Method creates ONE type of object via a single method. Abstract Factory creates FAMILIES of related objects via multiple methods, typically through an interface. |
| What is SOLID SRP? | Single Responsibility Principle — each class should have exactly one reason to change. One class, one job. |
| Why is SRP important? | Smaller, focused classes are easier to test, debug, and extend. Changes are isolated — modifying one class doesn't risk breaking unrelated features. |
| How does `@Autowired` work? | Spring scans for beans marked `@Service`, `@Repository` etc., and injects them into fields annotated `@Autowired` — no `new` keyword needed. |
| What happens when a user adds an item with a blank rarity? | `ItemFactory.createItem()` receives an empty rarity string. The `(rarity == null || rarity.isEmpty()) ? "Uncommon" : rarity` check kicks in and assigns the appropriate default rarity for the item type. |
