package com.arcade.management.controller;
import com.arcade.management.model.Item;
import com.arcade.management.factory.ItemFactory;
import com.arcade.management.model.Item;
import com.arcade.management.service.ItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
@Controller @RequestMapping("/items")
public class ItemController {
    @Autowired private ItemService itemService;
    @GetMapping
    public String listItems(Model model) { model.addAttribute("items", itemService.getAllItems()); return "items/list"; }
    @GetMapping("/add")
    public String showAddForm(Model model) { model.addAttribute("item", new Item()); return "items/add"; }
    @PostMapping("/add")
    public String addItem(@ModelAttribute Item itemForm) { 
        Item processedItem = ItemFactory.createItem(itemForm.getItemName(), itemForm.getItemType(), itemForm.getRarity());
        itemService.addItem(processedItem); 
        return "redirect:/items?success"; 
    }
    @GetMapping("/{id}/delete")
    public String deleteItem(@PathVariable Integer id) { itemService.deleteItem(id); return "redirect:/items?deleted"; }
}