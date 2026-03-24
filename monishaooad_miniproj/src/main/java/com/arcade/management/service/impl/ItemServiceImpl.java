package com.arcade.management.service.impl;
import com.arcade.management.model.Item;
import com.arcade.management.repository.ItemRepository;
import com.arcade.management.service.ItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service @Transactional
public class ItemServiceImpl implements ItemService {
    @Autowired private ItemRepository itemRepository;
    @Override public Item addItem(Item item) { return itemRepository.save(item); }
    @Override public Item getItemById(Integer id) { return itemRepository.findById(id).orElseThrow(() -> new RuntimeException("Item not found: " + id)); }
    @Override public List<Item> getAllItems() { return itemRepository.findAll(); }
    @Override public void deleteItem(Integer id) { itemRepository.delete(getItemById(id)); }
    @Override public List<Item> getItemsByRarity(String rarity) { return itemRepository.findByRarity(rarity); }
}