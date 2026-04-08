package com.arcade.management.service;
import com.arcade.management.dto.PlayerDTO;
import com.arcade.management.model.Player;
import java.util.List;
public interface PlayerService {
    Player registerPlayer(PlayerDTO playerDTO);
    Player authenticate(String username, String password);
    Player getPlayerById(Integer id);
    List<Player> getAllPlayers();
    Player updatePlayer(Integer id, PlayerDTO playerDTO);
    void deletePlayer(Integer id);
    List<Player> getLeaderboard(int limit);
    void updatePlayerScore(Integer playerId, Integer additionalScore);
}