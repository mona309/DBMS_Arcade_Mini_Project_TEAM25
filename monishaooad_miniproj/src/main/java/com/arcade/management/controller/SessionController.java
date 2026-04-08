package com.arcade.management.controller;
import com.arcade.management.model.MultiplayerSession;
import com.arcade.management.service.GameService;
import com.arcade.management.service.PlayerService;
import com.arcade.management.service.SessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Optional;

@Controller @RequestMapping("/sessions")
public class SessionController {
    @Autowired private SessionService sessionService;
    @Autowired private GameService gameService;
    @Autowired private PlayerService playerService;

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

    @PostMapping("/add")
    public String createSession(
            @RequestParam Integer gameId,
            @RequestParam(required = false) String startTime,
            @RequestParam(required = false) String endTime
    ) {
        MultiplayerSession session = new MultiplayerSession();
        session.setGame(gameService.getGameById(gameId));

        DateTimeFormatter fmt = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
        LocalDateTime start = Optional.ofNullable(startTime)
                .filter(s -> !s.isBlank())
                .map(s -> LocalDateTime.parse(s, fmt))
                .orElse(LocalDateTime.now());

        LocalDateTime end = Optional.ofNullable(endTime)
                .filter(s -> !s.isBlank())
                .map(s -> LocalDateTime.parse(s, fmt))
                .orElse(start.plusMinutes(30));

        session.setStartTime(start);
        session.setEndTime(end);
        sessionService.createSession(session);
        return "redirect:/sessions?success";
    }

    @GetMapping("/{id}")
    public String viewSession(@PathVariable Integer id, Model model) {
        model.addAttribute("session", sessionService.getSessionById(id));
        return "sessions/view";
    }

    @GetMapping("/{id}/delete")
    public String deleteSession(@PathVariable Integer id) {
        sessionService.deleteSession(id);
        return "redirect:/sessions?deleted";
    }
}