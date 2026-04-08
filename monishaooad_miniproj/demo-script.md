# Arcade Management System - Demo Script

This document is designed for the final project demonstration for a 4-person team. It contains step-by-step instructions on running the demo, alongside heavily categorized sections for each team member to explain their portion of the project according to **GRASP** and **SOLID** principles, and the integrated **Creational Pattern**.

---

## 🚀 Part 1: How to Run the Demo (For the Screen Sharer)

Before the presentation starts, ensure your WSL environment is open.

1. **Start the Database**:
   ```bash
   sudo service mysql start
   # (Optional) Log into MySQL to verify database `arcade_db` exists: mysql -u root -p
   ```
2. **Build and Run the Application**:
   Navigate to the root directory `monishaooad_miniproj` (where `pom.xml` is) and run:
   ```bash
   mvn clean spring-boot:run
   ```
3. **Execute the Demo Flow**:
   - Open your browser to `http://localhost:8080`.
   - **Show Registration**: Navigate to `/players/register`, enter details. Point out that the data is sent to the backend.
   - **Show Login**: Navigate to `/login`. Use the credentials you just created. Explain that `spring-session-jdbc` stores this session in the MySQL DB safely.
   - **Show Factory Pattern**: Navigate to `Items` -> `Add Item`. Enter a generic name like "Excalibur", type "Weapon", and leave Rarity blank. When added, show how the system automatically assigned it "Uncommon" rarity because of the underlying Factory logic.

---

## 🎤 Part 2: Presentation Roles (4 Members)

Each team member is allotted a specific technical portion of the architecture. Each person will describe exactly **one GRASP Principle** and **one SOLID Principle** mapped to their code.

### 👤 Member 1: Database & Persistence Layer
**Focus Area**: `PlayerRepository.java`, `ItemRepository.java`, and Exception Handling.

- **GRASP Principle: Creator**
  - *Explanation*: The Spring Data JPA Repositories act as the strict Creators for all entity records in the database. Instead of controllers manually instantiating database connections and building result sets, the Repositories encapsulate the creation logic.
- **SOLID Principle: Single Responsibility Principle (SRP)**
  - *Explanation*: Point to the `GlobalExceptionHandler` and `PlayerNotFoundException`. These classes have one strict reason to change: handling errors. They guarantee that our core logic never mixes with HTTP error translations.

### 👤 Member 2: Domain Logic & Object Creation
**Focus Area**: `ItemFactory.java` and internal Entity models.

- **Creational Design Pattern: Factory Method**
  - *Explanation*: Demonstrate `ItemFactory.java`. Instead of the frontend controller specifying all default configurations (like setting a Weapon's baseline rarity to Uncommon), we introduced a Creational Factory. It intercepts raw input and returns fully constructed, context-accurate `Item` objects.
- **GRASP Principle: Low Coupling / High Cohesion**
  - *Explanation*: The `ItemFactory` makes the project Highly Cohesive. The rules of what makes an "Armor" vs a "Weapon" are tightly bound within the Factory, uncoupling the `ItemController` from complex creation logic.

### 👤 Member 3: Business Services & Routing
**Focus Area**: `PlayerService.java` (Interface) vs `PlayerServiceImpl.java` (Implementation).

- **GRASP Principle: Information Expert**
  - *Explanation*: In our project, `PlayerServiceImpl` is the Information Expert holding the behavioral logic. For example, the `authenticate(username, password)` and `checkAndUpdateRank()` algorithms live here because this layer holds the data queries necessary to validate them.
- **SOLID Principle: Open/Closed Principle (OCP)**
  - *Explanation*: We abstracted business logic into Interfaces (like `PlayerService`). Our application is Closed for modification (the existing controllers won't break), but Open for extension (we could easily drop in a `PlayerServiceAdvancedImpl` without modifying dependent layers).

### 👤 Member 4: The Web MVC & Safety
**Focus Area**: `LoginController.java` and `UserSessionDTO.java`.

- **GRASP Principle: Controller**
  - *Explanation*: The `LoginController` and `PlayerController` strictly handle HTTP semantics (GET, POST). They act as the classic UI-to-Business boundary. They do not calculate ranks or save to the database directly; they merely collect Data Transfer Objects (DTOs) and pass them down.
- **SOLID Principle: Dependency Inversion Principle (DIP)**
  - *Explanation*: Look at `@Autowired private PlayerService playerService;` in the Controllers. We are depending upon Interfaces/Abstractions, *not* concretions! The Spring Framework injects the underlying logic dynamically. Also, by creating a `UserSessionDTO`, we decouple the HTTP Session from being strictly tied to gigantic database Entities.
