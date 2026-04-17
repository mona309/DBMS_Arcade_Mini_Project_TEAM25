package com.arcade.management.service.impl;
import com.arcade.management.model.Achievement;
import com.arcade.management.model.Player;
import com.arcade.management.model.PlayerAchievement;
import com.arcade.management.repository.AchievementRepository;
import com.arcade.management.repository.PlayerAchievementRepository;
import com.arcade.management.repository.PlayerRepository;
import com.arcade.management.service.AchievementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service @Transactional
public class AchievementServiceImpl implements AchievementService {
    @Autowired private AchievementRepository achievementRepository;
    @Autowired private PlayerRepository playerRepository;
    @Autowired private PlayerAchievementRepository playerAchievementRepository;
    @Override public Achievement addAchievement(Achievement a) { return achievementRepository.save(a); }
    @Override public Achievement getAchievementById(Integer id) { return achievementRepository.findById(id).orElseThrow(() -> new RuntimeException("Achievement not found: " + id)); }
    @Override public List<Achievement> getAllAchievements() { return achievementRepository.findAll(); }
    @Override public void deleteAchievement(Integer id) { achievementRepository.delete(getAchievementById(id)); }
    @Override public void checkAndUnlockAchievements(Integer playerId) {
        Player player = playerRepository.findById(playerId).orElseThrow(() -> new RuntimeException("Player not found"));
        List<Achievement> allAchievements = achievementRepository.findAll();
        for (Achievement ach : allAchievements) {
            if (ach.getCriteriaType() == null) continue;
            boolean alreadyUnlocked = player.getAchievements().stream()
                .anyMatch(pa -> pa.getAchievement().getAchievementID().equals(ach.getAchievementID()));
            if (alreadyUnlocked) continue;
            boolean unlocked = false;
            switch (ach.getCriteriaType()) {
                case "wins": unlocked = player.getWins() >= ach.getCriteriaValue(); break;
                case "gamesPlayed": unlocked = player.getGamesPlayed() >= ach.getCriteriaValue(); break;
                case "totalScore": unlocked = player.getTotalScore() >= ach.getCriteriaValue(); break;
            }
            if (unlocked) {
                PlayerAchievement pa = new PlayerAchievement();
                pa.setPlayer(player);
                pa.setAchievement(ach);
                pa.setUnlockedDate(java.time.LocalDate.now());
                playerAchievementRepository.save(pa);
            }
        }
    }
}