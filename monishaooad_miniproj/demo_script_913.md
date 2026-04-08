# Presentation Guide: Member 913
**Your Entities:** PlayerSession, PlayerAchievement, Rank

## What You Need to Explain

During the demo presentation, you are responsible for explaining the core relational logic spanning how a Player earns game sessions and unlocks Achievements/Ranks. 

### 1. GRASP Principle: Information Expert
* **Where it is:** Show the `PlayerServiceImpl.java` algorithm block for `checkAndUpdateRank()`.
* **What to say:** "For the `PlayerSession`, `PlayerAchievement`, and `Rank` relations, we applied the GRASP 'Information Expert' pattern. When a player finishes a session and gets a new score, that score has to be evaluated against `Rank` thresholds. Instead of the UI Controller fetching the data and calculating the math, the `PlayerServiceImpl` does it because it is the Information Expert. It holds the `totalScore` data and has immediate access to the `RankRepository`, naturally making it the right tier to execute rank-up promotions."

### 2. SOLID Principle: Open/Closed Principle (OCP)
* **Where it is:** Show the `PlayerAchievementRepository.java` or service interfaces.
* **What to say:** "Handling `PlayerAchievement` bindings honors the SOLID Open/Closed Principle. If we want to add a completely new type of game mode or achievement unlocking mechanism in the future, we do not need to modify our existing controllers or core entity logic. Our service layers and Spring Data Repositories are closed for modification (meaning they already work as expected), but they are infinitely open for extension by injecting new achievement rules into the database without rewriting our Java classes."
