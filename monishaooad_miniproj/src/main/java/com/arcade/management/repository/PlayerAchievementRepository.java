package com.arcade.management.repository;
import com.arcade.management.model.PlayerAchievement;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
@Repository
public interface PlayerAchievementRepository extends JpaRepository<PlayerAchievement, Integer> {
    List<PlayerAchievement> findByPlayer_PlayerID(Integer playerID);
}