package com.arcade.management.controller;
import com.arcade.management.dto.PlayerDTO;
import com.arcade.management.service.PlayerService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
@Controller @RequestMapping("/players")
public class PlayerController {
    @Autowired private PlayerService playerService;
    @GetMapping
    public String listPlayers(Model model) { model.addAttribute("players", playerService.getAllPlayers()); return "players/list"; }
    @GetMapping("/register")
    public String showRegistrationForm(Model model) { model.addAttribute("playerDTO", new PlayerDTO()); return "players/register"; }
    @PostMapping("/register")
    public String registerPlayer(@Valid @ModelAttribute PlayerDTO playerDTO, BindingResult result, Model model) {
        if (result.hasErrors()) return "players/register";
        try { playerService.registerPlayer(playerDTO); return "redirect:/players?success"; }
        catch (IllegalArgumentException e) { model.addAttribute("error", e.getMessage()); return "players/register"; }
    }
    @GetMapping("/{id}")
    public String viewPlayer(@PathVariable Integer id, Model model) { model.addAttribute("player", playerService.getPlayerById(id)); return "players/view"; }
    @GetMapping("/{id}/delete")
    public String deletePlayer(@PathVariable Integer id) { playerService.deletePlayer(id); return "redirect:/players?deleted"; }
    @GetMapping("/leaderboard")
    public String showLeaderboard(Model model) { model.addAttribute("leaderboard", playerService.getLeaderboard(10)); return "players/leaderboard"; }
}