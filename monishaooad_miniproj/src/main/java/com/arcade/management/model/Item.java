package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Entity @Table(name = "item") @Data @NoArgsConstructor @AllArgsConstructor
public class Item {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer itemID;
    @Column(length = 100)
    private String itemName;
    @Column(length = 50)
    private String itemType;
    @Column(length = 50)
    private String rarity;
    @OneToMany(mappedBy = "item")
    private List<PlayerItem> playerItems;
    @Override public String toString() { return "Item{itemID=" + itemID + ", itemName='" + itemName + "'}"; }
}