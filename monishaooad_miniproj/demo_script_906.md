# Presentation Guide: Member 906
**Your Entities:** Achievement, MultiplayerSession, Level

## What You Need to Explain

During the demo presentation, you are responsible for explaining the overarching game configuration metadata, such as the `Level` definitions, available core `Achievement`s to unlock, and the `MultiplayerSession` routing.

### 1. GRASP Principle: High Cohesion
* **Where it is:** Show the distinct separated packages (`controller`, `service`, `model`, `repository`) specifically pointing to `AchievementService` and `SessionService`.
* **What to say:** "For `Achievement`, `Level`, and `MultiplayerSession`, we ensured High Cohesion. Each class is tightly focused on its own bounded context. The `SessionService` exclusively worries about multiplayer match states and duration, while the `AchievementService` only worries about static achievement parameters. There are no 'God classes' doing everything. Everything related to match-making stays highly cohesive within the `Session` boundary."

### 2. SOLID Principle: Liskov Substitution Principle (LSP)
* **Where it is:** Show any Repository, such as `AchievementRepository` extending `JpaRepository`.
* **What to say:** "By leveraging the Spring framework for our `Level` and `MultiplayerSession` database tasks, we perfectly follow the Liskov Substitution Principle. We declare interfaces that extend `JpaRepository`. We never write the SQL implementations ourselves, but wherever our code expects an abstract repository, Spring injects a dynamic proxy at runtime. Because it perfectly respects the expected parent interface behaviors without crashing, the subclasses seamlessly substitute the abstractions."
