package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Session;
import ru.barkhatnat.cinema.dto.create.SessionCreateDto;
import ru.barkhatnat.cinema.dto.regular.SessionDto;
import ru.barkhatnat.cinema.dto.update.SessionUpdateDto;
import ru.barkhatnat.cinema.mapper.SessionMapper;
import ru.barkhatnat.cinema.repository.HallRepository;
import ru.barkhatnat.cinema.repository.MovieRepository;
import ru.barkhatnat.cinema.repository.SessionRepository;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class SessionService {

    private final SessionRepository sessionRepository;
    private final SessionMapper sessionMapper;
    private final HallRepository hallRepository;
    private final MovieRepository movieRepository;

    public void deleteById(UUID id) {
        sessionRepository.deleteById(id);
    }

    public SessionUpdateDto update(UUID id, SessionUpdateDto sessionUpdateDto) {
        Session session = sessionRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        sessionMapper.updateWithNull(sessionUpdateDto, session, hallRepository, movieRepository);
        Session updatedSession = sessionRepository.save(session);
        return sessionMapper.toSessionUpdateDto(updatedSession);
    }

    public List<SessionDto> findAll() {
        List<Session> sessions = sessionRepository.findAll();
        return sessions.stream()
                .map(sessionMapper::toSessionDto)
                .toList();
    }

    public SessionDto findById(UUID id) {
        Session session = sessionRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        return sessionMapper.toSessionDto(session);
    }

    public SessionDto create(@Valid SessionCreateDto sessionDto) {
        Session session = sessionMapper.toEntity(sessionDto, hallRepository, movieRepository);
        Session savedSession = sessionRepository.save(session);
        return sessionMapper.toSessionDto(savedSession);
    }
}
