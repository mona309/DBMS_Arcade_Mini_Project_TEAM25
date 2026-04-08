# Presentation Guide: Member 387
**Your Entities:** Game, Player, PlayerItems

## What You Need to Explain

During the demo presentation, you are the face of the application's core user identity layer. You explain how `Player`s interact with the `Game` interface and their persistent `PlayerItems` inventory.

### 1. GRASP Principle: Controller
* **Where it is:** Show `PlayerController.java` and `GameController.java` methods (like the `/login` or `/register` POST routes).
* **What to say:** "To manage `Player` inputs and `Game` browsing, we heavily utilize the GRASP 'Controller' pattern. When a user clicks 'Register' or wants to view their `PlayerItems`, the framework catches the web request. However, `PlayerController` does NOT talk to the database. It solely acts as the UI mediator—its only job is to intercept the data from the HTML form (like the DTOs), handle the security mapping, and pass it deeper into the system. This centralizes external I/O handling cleanly."

### 2. SOLID Principle: Dependency Inversion Principle (DIP)
* **Where it is:** Show the `@Autowired` fields inside `PlayerController` or the injected Services.
* **What to say:** "Our user layer perfectly models the SOLID Dependency Inversion Principle. The `GameController` and `PlayerController` do not depend on concrete implementations like `PlayerServiceImpl` or `GameServiceImpl`. They depend entirely on abstract generic Interfaces (`PlayerService`). This means the high-level routing rules are inverted to rely on abstraction, totally decoupled from the low-level SQL and Hibernate logic."
