package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity @Table(name = "playersession") @Data @NoArgsConstructor @AllArgsConstructor
public class PlayerSession {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerSessionID;
    @ManyToOne @JoinColumn(name = "sessionID")
    private MultiplayerSession session;
    @ManyToOne @JoinColumn(name = "playerID")
    private Player player;
    private Integer score;
    private Integer position;
    @Override public String toString() { return "PlayerSession{id=" + playerSessionID + "}"; }
}