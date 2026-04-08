package com.arcade.management.service.impl;

import com.arcade.management.dto.PlayerDTO;
import com.arcade.management.exception.PlayerNotFoundException;
import com.arcade.management.model.Player;
import com.arcade.management.model.Rank;
import com.arcade.management.repository.PlayerRepository;
import com.arcade.management.repository.RankRepository;
import com.arcade.management.service.PlayerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDate;
import java.util.List;

@Service @Transactional
public class PlayerServiceImpl implements PlayerService {
    @Autowired private PlayerRepository playerRepository;
    @Autowired private RankRepository rankRepository;

    @Override
    public Player registerPlayer(PlayerDTO playerDTO) {
        if (playerRepository.findByUsername(playerDTO.getUsername()).isPresent())
            throw new IllegalArgumentException("Username already exists");
        if (playerRepository.findByEmail(playerDTO.getEmail()).isPresent())
            throw new IllegalArgumentException("Email already exists");
        Player player = new Player();
        player.setUsername(playerDTO.getUsername());
        player.setEmail(playerDTO.getEmail());
        player.setPassword(playerDTO.getPassword());
        player.setRegistrationDate(LocalDate.now());
        player.setTotalScore(0);
        player.setAvatar(playerDTO.getAvatar());
        Rank bronzeRank = rankRepository.findById(1).orElseThrow(() -> new RuntimeException("Default rank not found"));
        player.setRank(bronzeRank);
        return playerRepository.save(player);
    }
    @Override public Player getPlayerById(Integer id) {
        return playerRepository.findById(id).orElseThrow(() -> new PlayerNotFoundException("Player not found with ID: " + id));
    }
    @Override
    public Player authenticate(String username, String password) {
        return playerRepository.findByUsername(username)
                .filter(p -> p.getPassword().equals(password))
                .orElse(null);
    }
    @Override public List<Player> getAllPlayers() { return playerRepository.findAll(); }
    @Override public Player updatePlayer(Integer id, PlayerDTO playerDTO) {
        Player player = getPlayerById(id);
        player.setUsername(playerDTO.getUsername());
        player.setEmail(playerDTO.getEmail());
        player.setAvatar(playerDTO.getAvatar());
        return playerRepository.save(player);
    }
    @Override public void deletePlayer(Integer id) { playerRepository.delete(getPlayerById(id)); }
    @Override public List<Player> getLeaderboard(int limit) { return playerRepository.findTop10ByOrderByTotalScoreDesc(); }
    @Override public void updatePlayerScore(Integer playerId, Integer additionalScore) {
        Player player = getPlayerById(playerId);
        player.setTotalScore(player.getTotalScore() + additionalScore);
        playerRepository.save(player);
        checkAndUpdateRank(playerId);
    }
    private void checkAndUpdateRank(Integer playerId) {
        Player player = getPlayerById(playerId);
        List<Rank> ranks = rankRepository.findAll(Sort.by(Sort.Direction.DESC, "rankScore"));
        for (Rank rank : ranks) {
            if (player.getTotalScore() >= rank.getRankScore()) {
                player.setRank(rank);
                playerRepository.save(player);
                break;
            }
        }
    }
}