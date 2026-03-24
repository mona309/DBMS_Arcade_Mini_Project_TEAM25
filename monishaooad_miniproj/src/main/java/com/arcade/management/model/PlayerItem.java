package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDate;

@Entity @Table(name = "playeritem") @Data @NoArgsConstructor @AllArgsConstructor
public class PlayerItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer playerItemID;
    @ManyToOne @JoinColumn(name = "playerID")
    private Player player;
    @ManyToOne @JoinColumn(name = "itemID")
    private Item item;
    private LocalDate dateObtained;
    private Integer quantity;
    @Override public String toString() { return "PlayerItem{id=" + playerItemID + "}"; }
}