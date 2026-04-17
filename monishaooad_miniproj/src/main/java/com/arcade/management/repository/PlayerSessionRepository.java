package com.arcade.management.repository;
import com.arcade.management.model.MultiplayerSession;
import com.arcade.management.model.PlayerSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
@Repository
public interface PlayerSessionRepository extends JpaRepository<PlayerSession, Integer> {
    List<PlayerSession> findBySession(MultiplayerSession session);
}