package com.arcade.management.controller;
import com.arcade.management.model.Game;
import com.arcade.management.service.GameService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDate;
@Controller @RequestMapping("/games")
public class GameController {
    @Autowired private GameService gameService;
    @GetMapping
    public String listGames(Model model) { model.addAttribute("games", gameService.getAllGames()); return "games/list"; }
    @GetMapping("/add")
    public String showAddForm(Model model) { model.addAttribute("game", new Game()); return "games/add"; }
    @PostMapping("/add")
    public String addGame(@ModelAttribute Game game) { if (game.getReleaseDate() == null) game.setReleaseDate(LocalDate.now()); gameService.addGame(game); return "redirect:/games?success"; }
    @GetMapping("/{id}")
    public String viewGame(@PathVariable Integer id, Model model) { model.addAttribute("game", gameService.getGameById(id)); return "games/view"; }
    @GetMapping("/{id}/delete")
    public String deleteGame(@PathVariable Integer id) { gameService.deleteGame(id); return "redirect:/games?deleted"; }
}