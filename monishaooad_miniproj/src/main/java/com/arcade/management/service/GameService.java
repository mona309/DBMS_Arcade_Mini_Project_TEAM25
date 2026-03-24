package com.arcade.management.service;
import com.arcade.management.model.Game;
import java.util.List;
public interface GameService {
    Game addGame(Game game);
    Game getGameById(Integer id);
    List<Game> getAllGames();
    Game updateGame(Integer id, Game game);
    void deleteGame(Integer id);
    List<Game> getGamesByGenre(String genre);
}