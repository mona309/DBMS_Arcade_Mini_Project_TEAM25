-- Extra Players
INSERT IGNORE INTO player (Username, Email, RegistrationDate, TotalScore, Avatar, RankID)
VALUES
('Alice','alice@example.com','2023-01-10',500,'avatar1.png',1),
('Bob','bob@example.com','2023-03-15',1500,'avatar2.png',2),
('Charlie','charlie@example.com','2023-06-22',5200,'avatar3.png',3),
('Diana','diana@example.com','2023-09-05',11000,'avatar4.png',4),
('Eve','eve@example.com','2024-01-20',750,'avatar5.png',1);

-- Extra Levels
INSERT IGNORE INTO level (GameID, LevelNumber, Difficulty, Description)
VALUES
(1,1,'Easy','First stage of Space Invaders'),
(1,2,'Medium','More aliens appear'),
(2,1,'Easy','Classic PacMan map'),
(3,1,'Hard','Battle Arena in2tro'),
(3,2,'Expert','Boss level');

-- Extra Multiplayer Sessions
INSERT IGNORE INTO multiplayersession (GameID, StartTime, EndTime)
VALUES
(3,'2024-04-01 10:00:00','2024-04-01 10:30:00'),
(3,'2024-04-02 12:00:00','2024-04-02 12:45:00'),
(2,'2024-05-05 15:00:00',NULL);

-- Player Sessions
INSERT IGNORE INTO playersession (SessionID, PlayerID, Score, Position)
VALUES
(1,1,300,3),
(1,2,800,2),
(1,3,1200,1),
(2,4,9000,1),
(3,5,450,2);

-- Player Achievements
INSERT IGNORE INTO playerachievement (PlayerID, AchievementID)
VALUES
(3,2),
(4,1),
(2,1),
(4,3);

-- Player Items
INSERT IGNORE INTO playeritem (PlayerID, ItemID, DateObtained, Quantity)
VALUES
(1,2,'2024-02-15',5),
(2,3,'2024-03-12',1),
(3,1,'2024-05-22',1),
(4,4,'2024-06-01',2),
(5,5,'2024-07-18',3);