package com.arcade.management.repository;
import com.arcade.management.model.Item;
import com.arcade.management.model.Player;
import com.arcade.management.model.PlayerItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
@Repository
public interface PlayerItemRepository extends JpaRepository<PlayerItem, Integer> {
    List<PlayerItem> findByPlayer_PlayerID(Integer playerID);
    List<PlayerItem> findByPlayerAndItem(Player player, Item item);
}