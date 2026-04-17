package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Entity @Table(name = "playerachievement") @Data @NoArgsConstructor @AllArgsConstructor
public class PlayerAchievement {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerAchievementID;
    @ManyToOne @JoinColumn(name = "playerID")
    private Player player;
    @ManyToOne @JoinColumn(name = "achievementID")
    private Achievement achievement;
    private LocalDateTime dateEarned;
    @Override public String toString() { return "PlayerAchievement{id=" + playerAchievementID + "}"; }
    public void setUnlockedDate(java.time.LocalDate date) { this.dateEarned = date.atStartOfDay(); }
}