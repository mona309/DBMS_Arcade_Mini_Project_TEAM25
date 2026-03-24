package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

@Entity @Table(name = "multiplayersession") @Data @NoArgsConstructor @AllArgsConstructor
public class MultiplayerSession {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer sessionID;
    @ManyToOne @JoinColumn(name = "gameID")
    private Game game;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    @OneToMany(mappedBy = "session")
    private List<PlayerSession> playerSessions;
    @Override public String toString() { return "MultiplayerSession{sessionID=" + sessionID + "}"; }
}