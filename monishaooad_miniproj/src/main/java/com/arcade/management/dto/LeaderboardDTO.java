package com.arcade.management.dto;
import lombok.Data;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
@Data @AllArgsConstructor @NoArgsConstructor
public class LeaderboardDTO {
    private Integer rank;
    private String username;
    private Integer totalScore;
    private String rankName;
}