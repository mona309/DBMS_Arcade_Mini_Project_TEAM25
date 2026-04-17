package com.arcade.management.service;
import com.arcade.management.model.Item;
import java.util.List;
public interface ItemService {
    Item addItem(Item item);
    Item getItemById(Integer id);
    List<Item> getAllItems();
    void deleteItem(Integer id);
    List<Item> getItemsByRarity(String rarity);
    void useItem(Integer playerId, Integer itemId);
}