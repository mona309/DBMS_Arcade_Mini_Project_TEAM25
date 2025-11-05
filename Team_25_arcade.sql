-- Enhanced Arcade Database Schema
-- Team 25: Monisha Sharma (PES2UG23CS906), Nandana Mathew (PES2UG23CS913)

-- =====================================================
-- 1. TABLE STRUCTURES (with fixes)
-- =====================================================

-- Ranks table (must be created first as it's referenced by player)
CREATE TABLE IF NOT EXISTS `ranks` (
  `RankID` int NOT NULL,
  `RankName` varchar(50) NOT NULL,
  `RankScore` int NOT NULL,
  PRIMARY KEY (`RankID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Achievement table
CREATE TABLE IF NOT EXISTS `achievement` (
  `AchievementID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`AchievementID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Game table
CREATE TABLE IF NOT EXISTS `game` (
  `GameID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(100) NOT NULL,
  `Genre` varchar(50) DEFAULT NULL,
  `MaxPlayers` int DEFAULT NULL,
  `ReleaseDate` date DEFAULT NULL,
  PRIMARY KEY (`GameID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Item table
CREATE TABLE IF NOT EXISTS `item` (
  `ItemID` int NOT NULL AUTO_INCREMENT,
  `ItemName` varchar(100) NOT NULL,
  `ItemType` varchar(50) DEFAULT NULL,
  `Rarity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Player table (with proper foreign key)
CREATE TABLE IF NOT EXISTS `player` (
  `PlayerID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `RegistrationDate` date NOT NULL,
  `TotalScore` int DEFAULT '0',
  `Avatar` varchar(100) DEFAULT NULL,
  `RankID` int DEFAULT 1,
  PRIMARY KEY (`PlayerID`),
  UNIQUE KEY `Username` (`Username`),
  UNIQUE KEY `Email` (`Email`),
  KEY `RankID` (`RankID`),
  CONSTRAINT `player_ibfk_1` FOREIGN KEY (`RankID`) REFERENCES `ranks` (`RankID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Level table
CREATE TABLE IF NOT EXISTS `level` (
  `LevelID` int NOT NULL AUTO_INCREMENT,
  `GameID` int NOT NULL,
  `LevelNumber` int NOT NULL,
  `Difficulty` varchar(20) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`LevelID`),
  KEY `GameID` (`GameID`),
  CONSTRAINT `level_ibfk_1` FOREIGN KEY (`GameID`) REFERENCES `game` (`GameID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Multiplayer session table
CREATE TABLE IF NOT EXISTS `multiplayersession` (
  `SessionID` int NOT NULL AUTO_INCREMENT,
  `GameID` int NOT NULL,
  `StartTime` datetime NOT NULL,
  `EndTime` datetime DEFAULT NULL,
  PRIMARY KEY (`SessionID`),
  KEY `GameID` (`GameID`),
  CONSTRAINT `multiplayersession_ibfk_1` FOREIGN KEY (`GameID`) REFERENCES `game` (`GameID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Player achievement junction table (FIXED: Added AUTO_INCREMENT)
CREATE TABLE IF NOT EXISTS `playerachievement` (
  `PlayerAchievementID` int NOT NULL AUTO_INCREMENT,
  `PlayerID` int NOT NULL,
  `AchievementID` int NOT NULL,
  `DateEarned` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PlayerAchievementID`),
  UNIQUE KEY `unique_player_achievement` (`PlayerID`, `AchievementID`),
  KEY `PlayerID` (`PlayerID`),
  KEY `AchievementID` (`AchievementID`),
  CONSTRAINT `playerachievement_ibfk_1` FOREIGN KEY (`PlayerID`) REFERENCES `player` (`PlayerID`) ON DELETE CASCADE,
  CONSTRAINT `playerachievement_ibfk_2` FOREIGN KEY (`AchievementID`) REFERENCES `achievement` (`AchievementID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Player item junction table
CREATE TABLE IF NOT EXISTS `playeritem` (
  `PlayerItemID` int NOT NULL AUTO_INCREMENT,
  `PlayerID` int DEFAULT NULL,
  `ItemID` int DEFAULT NULL,
  `DateObtained` date DEFAULT NULL,
  `Quantity` int DEFAULT '1',
  PRIMARY KEY (`PlayerItemID`),
  KEY `PlayerID` (`PlayerID`),
  KEY `ItemID` (`ItemID`),
  CONSTRAINT `playeritem_ibfk_1` FOREIGN KEY (`PlayerID`) REFERENCES `player` (`PlayerID`) ON DELETE CASCADE,
  CONSTRAINT `playeritem_ibfk_2` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Player session table
CREATE TABLE IF NOT EXISTS `playersession` (
  `PlayerSessionID` int NOT NULL AUTO_INCREMENT,
  `SessionID` int NOT NULL,
  `PlayerID` int NOT NULL,
  `Score` int DEFAULT 0,
  `Position` int DEFAULT NULL,
  PRIMARY KEY (`PlayerSessionID`),
  KEY `SessionID` (`SessionID`),
  KEY `PlayerID` (`PlayerID`),
  CONSTRAINT `playersession_ibfk_1` FOREIGN KEY (`SessionID`) REFERENCES `multiplayersession` (`SessionID`) ON DELETE CASCADE,
  CONSTRAINT `playersession_ibfk_2` FOREIGN KEY (`PlayerID`) REFERENCES `player` (`PlayerID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- =====================================================
-- 2. STORED PROCEDURES
-- =====================================================

DELIMITER $$

-- Procedure 1: Register a new player
DROP PROCEDURE IF EXISTS sp_register_player$$
CREATE PROCEDURE sp_register_player(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_avatar VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error registering player';
    END;
    
    START TRANSACTION;
    INSERT INTO player (Username, Email, RegistrationDate, TotalScore, Avatar, RankID)
    VALUES (p_username, p_email, CURDATE(), 0, p_avatar, 1);
    COMMIT;
END$$

-- Procedure 2: Award item to player
DROP PROCEDURE IF EXISTS sp_award_item$$
CREATE PROCEDURE sp_award_item(
    IN p_player_id INT,
    IN p_item_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE existing_quantity INT DEFAULT 0;
    
    -- Check if player already has this item
    SELECT Quantity INTO existing_quantity 
    FROM playeritem 
    WHERE PlayerID = p_player_id AND ItemID = p_item_id
    LIMIT 1;
    
    IF existing_quantity > 0 THEN
        -- Update existing quantity
        UPDATE playeritem 
        SET Quantity = Quantity + p_quantity,
            DateObtained = CURDATE()
        WHERE PlayerID = p_player_id AND ItemID = p_item_id;
    ELSE
        -- Insert new item
        INSERT INTO playeritem (PlayerID, ItemID, DateObtained, Quantity)
        VALUES (p_player_id, p_item_id, CURDATE(), p_quantity);
    END IF;
END$$

-- Procedure 3: Complete multiplayer session
DROP PROCEDURE IF EXISTS sp_complete_session$$
CREATE PROCEDURE sp_complete_session(
    IN p_session_id INT
)
BEGIN
    UPDATE multiplayersession 
    SET EndTime = NOW() 
    WHERE SessionID = p_session_id AND EndTime IS NULL;
    
    -- Update player rankings based on scores
    UPDATE playersession ps
    SET Position = (
        SELECT COUNT(*) + 1
        FROM playersession ps2
        WHERE ps2.SessionID = ps.SessionID 
        AND ps2.Score > ps.Score
    )
    WHERE ps.SessionID = p_session_id;
END$$

-- Procedure 4: Get player leaderboard
DROP PROCEDURE IF EXISTS sp_get_leaderboard$$
CREATE PROCEDURE sp_get_leaderboard(
    IN p_limit INT
)
BEGIN
    SELECT 
        p.PlayerID,
        p.Username,
        p.TotalScore,
        r.RankName,
        COUNT(DISTINCT pa.AchievementID) as AchievementCount
    FROM player p
    LEFT JOIN ranks r ON p.RankID = r.RankID
    LEFT JOIN playerachievement pa ON p.PlayerID = pa.PlayerID
    GROUP BY p.PlayerID, p.Username, p.TotalScore, r.RankName
    ORDER BY p.TotalScore DESC
    LIMIT p_limit;
END$$

-- =====================================================
-- 3. STORED FUNCTIONS
-- =====================================================

-- Function 1: Get player rank name
DROP FUNCTION IF EXISTS fn_get_player_rank$$
CREATE FUNCTION fn_get_player_rank(p_player_id INT)
RETURNS VARCHAR(50)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE rank_name VARCHAR(50);
    
    SELECT r.RankName INTO rank_name
    FROM player p
    JOIN ranks r ON p.RankID = r.RankID
    WHERE p.PlayerID = p_player_id;
    
    RETURN IFNULL(rank_name, 'Unranked');
END$$

-- Function 2: Calculate achievement completion percentage
DROP FUNCTION IF EXISTS fn_achievement_completion$$
CREATE FUNCTION fn_achievement_completion(p_player_id INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE earned INT;
    DECLARE total INT;
    DECLARE percentage DECIMAL(5,2);
    
    SELECT COUNT(*) INTO earned
    FROM playerachievement
    WHERE PlayerID = p_player_id;
    
    SELECT COUNT(*) INTO total
    FROM achievement;
    
    IF total > 0 THEN
        SET percentage = (earned / total) * 100;
    ELSE
        SET percentage = 0;
    END IF;
    
    RETURN percentage;
END$$

-- Function 3: Get player's total items value
DROP FUNCTION IF EXISTS fn_player_inventory_count$$
CREATE FUNCTION fn_player_inventory_count(p_player_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE item_count INT;
    
    SELECT IFNULL(SUM(Quantity), 0) INTO item_count
    FROM playeritem
    WHERE PlayerID = p_player_id;
    
    RETURN item_count;
END$$

-- Function 4: Check if player has achievement
DROP FUNCTION IF EXISTS fn_has_achievement$$
CREATE FUNCTION fn_has_achievement(p_player_id INT, p_achievement_id INT)
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE has_it BOOLEAN;
    
    SELECT EXISTS(
        SELECT 1 FROM playerachievement 
        WHERE PlayerID = p_player_id AND AchievementID = p_achievement_id
    ) INTO has_it;
    
    RETURN has_it;
END$$

-- =====================================================
-- 4. TRIGGERS
-- =====================================================

-- Trigger 1: Update player stats after session score update
DROP TRIGGER IF EXISTS trg_update_player_stats$$
CREATE TRIGGER trg_update_player_stats 
AFTER UPDATE ON playersession 
FOR EACH ROW
BEGIN
    IF OLD.Score <> NEW.Score THEN
        -- Update total score
        UPDATE player
        SET TotalScore = TotalScore + (NEW.Score - OLD.Score)
        WHERE PlayerID = NEW.PlayerID;
        
        -- Award Sharp Shooter achievement for high score
        IF NEW.Score > 700 AND NOT fn_has_achievement(NEW.PlayerID, 2) THEN
            INSERT INTO playerachievement (PlayerID, AchievementID, DateEarned)
            VALUES (NEW.PlayerID, 2, NOW());
        END IF;
    END IF;
END$$

-- Trigger 2: Auto-update player rank based on total score
DROP TRIGGER IF EXISTS trg_auto_rank_update$$
CREATE TRIGGER trg_auto_rank_update 
AFTER UPDATE ON player 
FOR EACH ROW
BEGIN
    DECLARE new_rank_id INT;
    
    IF OLD.TotalScore <> NEW.TotalScore THEN
        -- Determine new rank
        SELECT RankID INTO new_rank_id
        FROM ranks
        WHERE NEW.TotalScore >= RankScore
        ORDER BY RankScore DESC
        LIMIT 1;
        
        -- Update rank if changed
        IF new_rank_id IS NOT NULL AND new_rank_id <> NEW.RankID THEN
            UPDATE player
            SET RankID = new_rank_id
            WHERE PlayerID = NEW.PlayerID;
        END IF;
    END IF;
END$$

-- Trigger 3: Award First Blood achievement on first session
DROP TRIGGER IF EXISTS trg_first_session$$
CREATE TRIGGER trg_first_session 
AFTER INSERT ON playersession 
FOR EACH ROW
BEGIN
    DECLARE session_count INT;
    
    SELECT COUNT(*) INTO session_count
    FROM playersession
    WHERE PlayerID = NEW.PlayerID;
    
    -- Award First Blood on first session with score > 0
    IF session_count = 1 AND NEW.Score > 0 THEN
        INSERT IGNORE INTO playerachievement (PlayerID, AchievementID, DateEarned)
        VALUES (NEW.PlayerID, 1, NOW());
    END IF;
END$$

-- Trigger 4: Validate item quantity on insert/update
DROP TRIGGER IF EXISTS trg_validate_item_quantity$$
CREATE TRIGGER trg_validate_item_quantity 
BEFORE INSERT ON playeritem 
FOR EACH ROW
BEGIN
    IF NEW.Quantity < 1 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Item quantity must be at least 1';
    END IF;
    
    IF NEW.Quantity > 999 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Item quantity cannot exceed 999';
    END IF;
END$$

DELIMITER ;

-- =====================================================
-- 5. SAMPLE DATA
-- =====================================================

INSERT IGNORE INTO ranks VALUES 
(1,'Bronze',0),
(2,'Silver',1000),
(3,'Gold',5000),
(4,'Platinum',10000);

INSERT IGNORE INTO achievement VALUES 
(1,'First Blood','Scored first kill in a match'),
(2,'Sharp Shooter','Achieved 80% hit accuracy'),
(3,'Level Master','Completed all levels of a game');

INSERT IGNORE INTO game VALUES 
(1,'Space Invaders','Arcade',2,'2020-05-10'),
(2,'PacMan Adventures','Arcade',4,'2021-08-15'),
(3,'Battle Arena','Action',10,'2022-11-20');

INSERT IGNORE INTO item VALUES 
(1,'Excalibur Sword','Weapon','Mythic'),
(2,'Healing Potion','Consumable','Common'),
(3,'Phoenix Shield','Armor','Epic'),
(4,'Invisibility Cloak','Accessory','Rare'),
(5,'Magic Ring','Accessory','Uncommon');
