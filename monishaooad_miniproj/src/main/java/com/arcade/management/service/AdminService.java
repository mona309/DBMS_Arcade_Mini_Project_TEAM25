package com.arcade.management.service;

import com.arcade.management.model.Admin;

import java.util.List;

public interface AdminService {
    Admin registerAdmin(Admin admin);
    Admin authenticate(String username, String password);
    List<Admin> getAllAdmins();
}
