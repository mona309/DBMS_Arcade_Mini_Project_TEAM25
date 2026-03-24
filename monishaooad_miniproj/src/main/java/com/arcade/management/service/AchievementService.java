package com.arcade.management.service;
import com.arcade.management.model.Achievement;
import java.util.List;
public interface AchievementService {
    Achievement addAchievement(Achievement achievement);
    Achievement getAchievementById(Integer id);
    List<Achievement> getAllAchievements();
    void deleteAchievement(Integer id);
}