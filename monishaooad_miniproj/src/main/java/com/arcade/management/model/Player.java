package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDate;
import java.util.List;

@Entity @Table(name = "player") @Data @NoArgsConstructor @AllArgsConstructor
public class Player {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerID;
    @Column(nullable = false, unique = true, length = 50)
    private String username;
    @Column(nullable = false, unique = true, length = 100)
    private String email;
    private LocalDate registrationDate;
    @Column(nullable = false)
    private Integer totalScore = 0;
    @Column(length = 100)
    private String avatar;
    @ManyToOne @JoinColumn(name = "rankID")
    private Rank rank;
    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL)
    private List<PlayerAchievement> achievements;
    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL)
    private List<PlayerItem> items;
    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL)
    private List<PlayerSession> sessions;
    @Override public String toString() { return "Player{playerID=" + playerID + ", username='" + username + "'}"; }
}