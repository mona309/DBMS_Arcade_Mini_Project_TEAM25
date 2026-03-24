package com.arcade.management.service.impl;
import com.arcade.management.model.Game;
import com.arcade.management.repository.GameRepository;
import com.arcade.management.service.GameService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service @Transactional
public class GameServiceImpl implements GameService {
    @Autowired private GameRepository gameRepository;
    @Override public Game addGame(Game game) { return gameRepository.save(game); }
    @Override public Game getGameById(Integer id) { return gameRepository.findById(id).orElseThrow(() -> new RuntimeException("Game not found with ID: " + id)); }
    @Override public List<Game> getAllGames() { return gameRepository.findAll(); }
    @Override public Game updateGame(Integer id, Game u) { Game g = getGameById(id); g.setTitle(u.getTitle()); g.setGenre(u.getGenre()); g.setMaxPlayers(u.getMaxPlayers()); g.setReleaseDate(u.getReleaseDate()); return gameRepository.save(g); }
    @Override public void deleteGame(Integer id) { gameRepository.delete(getGameById(id)); }
    @Override public List<Game> getGamesByGenre(String genre) { return gameRepository.findByGenre(genre); }
}