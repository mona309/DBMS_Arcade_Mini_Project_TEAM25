package com.arcade.management.controller;

import com.arcade.management.dto.LoginDTO;
import com.arcade.management.dto.UserSessionDTO;
import com.arcade.management.model.Player;
import com.arcade.management.service.PlayerService;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class LoginController {

    @Autowired
    private PlayerService playerService;

    @GetMapping("/login")
    public String showLoginForm(Model model) {
        model.addAttribute("loginDTO", new LoginDTO());
        return "players/login";
    }

    @PostMapping("/login")
    public String login(@Valid @ModelAttribute LoginDTO loginDTO, BindingResult result, HttpSession session, Model model) {
        if (result.hasErrors()) {
            return "players/login";
        }
        
        Player player = playerService.authenticate(loginDTO.getUsername(), loginDTO.getPassword());
        if (player != null) {
            UserSessionDTO sessionUser = new UserSessionDTO(player.getPlayerID(), player.getUsername());
            session.setAttribute("loggedInUser", sessionUser);
            return "redirect:/";
        } else {
            model.addAttribute("error", "Invalid username or password");
            return "players/login";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/login?logout";
    }
}
