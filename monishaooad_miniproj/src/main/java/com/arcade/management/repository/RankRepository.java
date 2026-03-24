package com.arcade.management.repository;
import com.arcade.management.model.Rank;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface RankRepository extends JpaRepository<Rank, Integer> {}