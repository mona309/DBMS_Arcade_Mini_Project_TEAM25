package com.arcade.management.repository;
import com.arcade.management.model.MultiplayerSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface MultiplayerSessionRepository extends JpaRepository<MultiplayerSession, Integer> {}