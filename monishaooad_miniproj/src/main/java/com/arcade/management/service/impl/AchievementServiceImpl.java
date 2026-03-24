package com.arcade.management.service.impl;
import com.arcade.management.model.Achievement;
import com.arcade.management.repository.AchievementRepository;
import com.arcade.management.service.AchievementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service @Transactional
public class AchievementServiceImpl implements AchievementService {
    @Autowired private AchievementRepository achievementRepository;
    @Override public Achievement addAchievement(Achievement a) { return achievementRepository.save(a); }
    @Override public Achievement getAchievementById(Integer id) { return achievementRepository.findById(id).orElseThrow(() -> new RuntimeException("Achievement not found: " + id)); }
    @Override public List<Achievement> getAllAchievements() { return achievementRepository.findAll(); }
    @Override public void deleteAchievement(Integer id) { achievementRepository.delete(getAchievementById(id)); }
}