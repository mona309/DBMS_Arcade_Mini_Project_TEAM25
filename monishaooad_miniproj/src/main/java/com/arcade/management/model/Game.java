package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDate;
import java.util.List;

@Entity @Table(name = "game") @Data @NoArgsConstructor @AllArgsConstructor
public class Game {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer gameID;
    @Column(length = 100)
    private String title;
    @Column(length = 50)
    private String genre;
    private Integer maxPlayers;
    private LocalDate releaseDate;
    @OneToMany(mappedBy = "game")
    private List<Level> levels;
    @OneToMany(mappedBy = "game")
    private List<MultiplayerSession> sessions;
    @Override public String toString() { return "Game{gameID=" + gameID + ", title='" + title + "'}"; }
}