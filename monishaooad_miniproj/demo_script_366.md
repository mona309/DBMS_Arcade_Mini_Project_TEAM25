# Presenation Guide: Member 366
**Your Entities:** Admin, Item

## What You Need to Explain

During the demo presentation, you are responsible for explaining how the `Admin` management system and the `Item` catalog are structured using Software Engineering principles.

### 1. GRASP Principle: Creator Pattern
* **Where it is:** Show the `ItemFactory.java` class.
* **What to say:** "To handle the `Item` entity, I implemented the GRASP 'Creator' pattern using a Factory Method. Because Items have complex categorizations (like Weapons needing to be 'Uncommon' or Consumables being 'Common'), the system shouldn't let controllers or generic admins create raw records. Instead, the `ItemFactory` acts as the explicit **Creator**. It safely processes generic properties and returns a perfectly formulated object before saving it to the database."

### 2. SOLID Principle: Single Responsibility Principle (SRP)
* **Where it is:** Show the `Admin.java` entity versus the `Player.java` entity.
* **What to say:** "For the `Admin` entity, we followed the SOLID Single Responsibility Principle. Initially, it might be tempting to just add a `role` flag to the `Player` table to make them an 'Admin'. However, Players have complex game metrics (scores, items, sessions) that Admins do not need. By extracting `Admin` into its own distinct Entity, Repository, and Controller, we ensure that the Admin classes have only *one single reason to change*—which is strictly administrative authorization, cleanly separated from gameplay."
