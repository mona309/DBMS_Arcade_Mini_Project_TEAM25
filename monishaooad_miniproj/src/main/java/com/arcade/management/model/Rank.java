package com.arcade.management.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Entity @Table(name = "ranks") @Data @NoArgsConstructor @AllArgsConstructor
public class Rank {
    @Id
    private Integer rankID;
    @Column(length = 50)
    private String rankName;
    private Integer rankScore;
    @OneToMany(mappedBy = "rank")
    private List<Player> players;
    @Override public String toString() { return "Rank{rankID=" + rankID + ", rankName='" + rankName + "'}"; }
}