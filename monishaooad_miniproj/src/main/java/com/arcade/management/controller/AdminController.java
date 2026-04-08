package com.arcade.management.controller;

import com.arcade.management.model.Admin;
import com.arcade.management.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    private AdminService adminService;

    @GetMapping
    @ResponseBody
    public String adminHome() {
        return "Admin Control Panel is active. Endpoints available for managing Item DB remotely via Factory implementations.";
    }

    @GetMapping("/list")
    public String listAdmins(Model model) {
        List<Admin> admins = adminService.getAllAdmins();
        model.addAttribute("admins", admins);
        return "admin/list"; // For future implementations if views are built for admin
    }
}
