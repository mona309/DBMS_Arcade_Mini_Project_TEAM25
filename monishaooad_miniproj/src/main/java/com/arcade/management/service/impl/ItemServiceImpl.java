package com.arcade.management.service.impl;
import com.arcade.management.model.Item;
import com.arcade.management.model.Player;
import com.arcade.management.model.PlayerItem;
import com.arcade.management.repository.ItemRepository;
import com.arcade.management.repository.PlayerItemRepository;
import com.arcade.management.repository.PlayerRepository;
import com.arcade.management.service.ItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service @Transactional
public class ItemServiceImpl implements ItemService {
    @Autowired private ItemRepository itemRepository;
    @Autowired private PlayerRepository playerRepository;
    @Autowired private PlayerItemRepository playerItemRepository;
    @Override public Item addItem(Item item) { return itemRepository.save(item); }
    @Override public Item getItemById(Integer id) { return itemRepository.findById(id).orElseThrow(() -> new RuntimeException("Item not found: " + id)); }
    @Override public List<Item> getAllItems() { return itemRepository.findAll(); }
    @Override public void deleteItem(Integer id) { itemRepository.delete(getItemById(id)); }
    @Override public List<Item> getItemsByRarity(String rarity) { return itemRepository.findByRarity(rarity); }
    @Override public void useItem(Integer playerId, Integer itemId) {
        Player player = playerRepository.findById(playerId).orElseThrow(() -> new RuntimeException("Player not found"));
        Item item = getItemById(itemId);
        if (item.getBonusScore() != null) {
            player.setTotalScore(player.getTotalScore() + item.getBonusScore());
            playerRepository.save(player);
        }
        if (item.getBonusWins() != null && item.getBonusWins() > 0) {
            player.setWins(player.getWins() + item.getBonusWins());
            playerRepository.save(player);
        }
        if (item.getConsumable() != null && item.getConsumable()) {
            List<PlayerItem> pis = playerItemRepository.findByPlayerAndItem(player, item);
            if (!pis.isEmpty()) {
                playerItemRepository.delete(pis.get(0));
            }
        }
    }
}