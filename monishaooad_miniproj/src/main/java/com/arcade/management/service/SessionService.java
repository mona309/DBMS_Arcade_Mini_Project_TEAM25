package com.arcade.management.service;
import com.arcade.management.model.MultiplayerSession;
import java.util.List;
public interface SessionService {
    MultiplayerSession createSession(MultiplayerSession session);
    MultiplayerSession getSessionById(Integer id);
    List<MultiplayerSession> getAllSessions();
    void deleteSession(Integer id);
}