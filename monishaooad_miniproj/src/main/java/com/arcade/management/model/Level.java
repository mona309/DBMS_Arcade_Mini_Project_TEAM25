package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity @Table(name = "level") @Data @NoArgsConstructor @AllArgsConstructor
public class Level {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer levelID;
    @ManyToOne @JoinColumn(name = "gameID")
    private Game game;
    private Integer levelNumber;
    @Column(length = 20)
    private String difficulty;
    @Column(length = 255)
    private String description;
    @Override public String toString() { return "Level{levelID=" + levelID + "}"; }
}