package com.arcade.management.controller;
import com.arcade.management.service.SessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
@Controller @RequestMapping("/sessions")
public class SessionController {
    @Autowired private SessionService sessionService;
    @GetMapping
    public String listSessions(Model model) { model.addAttribute("sessions", sessionService.getAllSessions()); return "sessions/list"; }
    @GetMapping("/{id}")
    public String viewSession(@PathVariable Integer id, Model model) { model.addAttribute("session", sessionService.getSessionById(id)); return "sessions/view"; }
    @GetMapping("/{id}/delete")
    public String deleteSession(@PathVariable Integer id) { sessionService.deleteSession(id); return "redirect:/sessions?deleted"; }
}