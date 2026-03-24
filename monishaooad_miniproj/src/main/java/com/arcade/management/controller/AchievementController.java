package com.arcade.management.controller;
import com.arcade.management.model.Achievement;
import com.arcade.management.service.AchievementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
@Controller @RequestMapping("/achievements")
public class AchievementController {
    @Autowired private AchievementService achievementService;
    @GetMapping
    public String listAchievements(Model model) { model.addAttribute("achievements", achievementService.getAllAchievements()); return "achievements/list"; }
    @GetMapping("/add")
    public String showAddForm(Model model) { model.addAttribute("achievement", new Achievement()); return "achievements/add"; }
    @PostMapping("/add")
    public String addAchievement(@ModelAttribute Achievement a) { achievementService.addAchievement(a); return "redirect:/achievements?success"; }
    @GetMapping("/{id}/delete")
    public String deleteAchievement(@PathVariable Integer id) { achievementService.deleteAchievement(id); return "redirect:/achievements?deleted"; }
}