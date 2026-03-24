package com.arcade.management.repository;
import com.arcade.management.model.PlayerSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface PlayerSessionRepository extends JpaRepository<PlayerSession, Integer> {}