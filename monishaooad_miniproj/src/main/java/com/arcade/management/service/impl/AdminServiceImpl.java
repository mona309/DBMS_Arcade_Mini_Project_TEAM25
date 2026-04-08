package com.arcade.management.service.impl;

import com.arcade.management.model.Admin;
import com.arcade.management.repository.AdminRepository;
import com.arcade.management.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service 
@Transactional
public class AdminServiceImpl implements AdminService {

    @Autowired
    private AdminRepository adminRepository;

    @Override
    public Admin registerAdmin(Admin admin) {
        if (adminRepository.findByUsername(admin.getUsername()).isPresent()) {
            throw new IllegalArgumentException("Admin Username already exists");
        }
        return adminRepository.save(admin);
    }

    @Override
    public Admin authenticate(String username, String password) {
        return adminRepository.findByUsername(username)
                .filter(a -> a.getPassword().equals(password))
                .orElse(null);
    }

    @Override
    public List<Admin> getAllAdmins() {
        return adminRepository.findAll();
    }
}
