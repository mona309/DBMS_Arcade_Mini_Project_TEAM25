package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Entity @Table(name = "achievement") @Data @NoArgsConstructor @AllArgsConstructor
public class Achievement {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer achievementID;
    @Column(length = 100)
    private String name;
    @Column(length = 255)
    private String description;
    private String criteriaType;
    private Integer criteriaValue;
    @OneToMany(mappedBy = "achievement")
    private List<PlayerAchievement> playerAchievements;
    @Override public String toString() { return "Achievement{achievementID=" + achievementID + ", name='" + name + "'}"; }
}