package com.arcade.management.controller;
import com.arcade.management.model.MultiplayerSession;
import com.arcade.management.model.PlayerSession;
import com.arcade.management.repository.PlayerSessionRepository;
import com.arcade.management.service.AchievementService;
import com.arcade.management.service.GameService;
import com.arcade.management.service.PlayerService;
import com.arcade.management.service.SessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;

@Controller @RequestMapping("/sessions")
public class SessionController {
    @Autowired private SessionService sessionService;
    @Autowired private GameService gameService;
    @Autowired private PlayerService playerService;
    @Autowired private PlayerSessionRepository playerSessionRepository;
    @Autowired private AchievementService achievementService;

    @GetMapping
    public String listSessions(Model model) {
        model.addAttribute("sessions", sessionService.getAllSessions());
        return "sessions/list";
    }

    @GetMapping("/add")
    public String showAddSessionForm(Model model) {
        model.addAttribute("session", new MultiplayerSession());
        model.addAttribute("games", gameService.getAllGames());
        model.addAttribute("players", playerService.getAllPlayers());
        return "sessions/add";
    }

    @PostMapping("/create")
    public String createAndPlaySession(
            @RequestParam Integer gameId,
            @RequestParam List<Integer> playerIds,
            @RequestParam Integer winnerId
    ) {
        MultiplayerSession session = new MultiplayerSession();
        session.setGame(gameService.getGameById(gameId));
        session.setStartTime(LocalDateTime.now());
        session.setEndTime(LocalDateTime.now());
        MultiplayerSession saved = sessionService.createSession(session);
        
        for (Integer playerId : playerIds) {
            PlayerSession ps = new PlayerSession();
            ps.setSession(saved);
            ps.setPlayer(playerService.getPlayerById(playerId));
            boolean isWin = playerId.equals(winnerId);
            ps.setScore(isWin ? 1500 : 0);
            ps.setPosition(0);
            ps.setIsWinner(isWin);
            playerSessionRepository.save(ps);
            
            if (isWin) {
                playerService.recordWin(playerId, 1500);
            } else {
                playerService.recordLoss(playerId);
            }
            achievementService.checkAndUnlockAchievements(playerId);
        }
        
        return "redirect:/sessions?success";
    }

    @GetMapping("/{id}")
    public String viewSession(@PathVariable Integer id, Model model) {
        model.addAttribute("session", sessionService.getSessionById(id));
        model.addAttribute("players", playerService.getAllPlayers());
        return "sessions/view";
    }

    @PostMapping("/{id}/join")
    public String joinSession(@PathVariable Integer id, @RequestParam String playerId) {
        if (playerId == null || playerId.isBlank()) {
            return "redirect:/sessions/" + id + "?error";
        }
        MultiplayerSession session = sessionService.getSessionById(id);
        PlayerSession ps = new PlayerSession();
        ps.setSession(session);
        ps.setPlayer(playerService.getPlayerById(Integer.parseInt(playerId)));
        ps.setPosition(0);
        playerSessionRepository.save(ps);
        return "redirect:/sessions/" + id + "?joined";
    }

    @GetMapping("/{id}/delete")
    public String deleteSession(@PathVariable Integer id) {
        sessionService.deleteSession(id);
        return "redirect:/sessions?deleted";
    }

    @PostMapping("/{id}/end")
    public String endSession(@PathVariable Integer id, @RequestParam String winnerId) {
        if (winnerId == null || winnerId.isBlank()) {
            return "redirect:/sessions/" + id + "?error";
        }
        MultiplayerSession session = sessionService.getSessionById(id);
        List<PlayerSession> playerSessions = playerSessionRepository.findBySession(session);
        int winner = Integer.parseInt(winnerId);
        for (PlayerSession ps : playerSessions) {
            if (ps.getPlayer().getPlayerID().equals(winner)) {
                playerService.recordWin(ps.getPlayer().getPlayerID(), ps.getScore() != null ? ps.getScore() : 100);
            } else {
                playerService.recordLoss(ps.getPlayer().getPlayerID());
            }
            achievementService.checkAndUnlockAchievements(ps.getPlayer().getPlayerID());
        }
        session.setEndTime(LocalDateTime.now());
        sessionService.createSession(session);
        return "redirect:/sessions?completed";
    }
}