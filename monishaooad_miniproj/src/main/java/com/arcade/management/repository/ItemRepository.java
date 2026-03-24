package com.arcade.management.repository;
import com.arcade.management.model.Item;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
@Repository
public interface ItemRepository extends JpaRepository<Item, Integer> {
    List<Item> findByRarity(String rarity);
}