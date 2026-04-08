package com.arcade.management.factory;

import com.arcade.management.model.Item;

/**
 * Factory Method Pattern implementation for creating Items.
 * Consolidates the creational logic and configuration of different item types.
 */
public class ItemFactory {

    public static Item createItem(String name, String type, String rarity) {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Item name cannot be null or empty");
        }
        
        switch (type.toLowerCase()) {
            case "weapon":
                return createWeapon(name, rarity);
            case "consumable":
                return createConsumable(name, rarity);
            case "armor":
                return createArmor(name, rarity);
            default:
                return createGenericItem(name, type, rarity);
        }
    }

    private static Item createWeapon(String name, String rarity) {
        Item weapon = new Item();
        weapon.setItemName(name);
        weapon.setItemType("Weapon");
        // Weapons default to at least Uncommon if standard rarity is given
        weapon.setRarity((rarity == null || rarity.isEmpty()) ? "Uncommon" : rarity);
        return weapon;
    }

    private static Item createConsumable(String name, String rarity) {
        Item consumable = new Item();
        consumable.setItemName(name);
        consumable.setItemType("Consumable");
        consumable.setRarity((rarity == null || rarity.isEmpty()) ? "Common" : rarity);
        return consumable;
    }

    private static Item createArmor(String name, String rarity) {
        Item armor = new Item();
        armor.setItemName(name);
        armor.setItemType("Armor");
        armor.setRarity((rarity == null || rarity.isEmpty()) ? "Rare" : rarity);
        return armor;
    }

    private static Item createGenericItem(String name, String type, String rarity) {
        Item item = new Item();
        item.setItemName(name);
        item.setItemType(type);
        item.setRarity(rarity);
        return item;
    }
}
