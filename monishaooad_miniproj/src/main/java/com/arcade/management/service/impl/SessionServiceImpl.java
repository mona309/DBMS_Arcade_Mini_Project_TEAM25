package com.arcade.management.service.impl;
import com.arcade.management.model.MultiplayerSession;
import com.arcade.management.repository.MultiplayerSessionRepository;
import com.arcade.management.service.SessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service @Transactional
public class SessionServiceImpl implements SessionService {
    @Autowired private MultiplayerSessionRepository sessionRepository;
    @Override public MultiplayerSession createSession(MultiplayerSession s) { return sessionRepository.save(s); }
    @Override public MultiplayerSession getSessionById(Integer id) { return sessionRepository.findById(id).orElseThrow(() -> new RuntimeException("Session not found: " + id)); }
    @Override public List<MultiplayerSession> getAllSessions() { return sessionRepository.findAll(); }
    @Override public void deleteSession(Integer id) { sessionRepository.delete(getSessionById(id)); }
}