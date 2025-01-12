package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Ticket;
import ru.barkhatnat.cinema.domain.enums.RoleName;
import ru.barkhatnat.cinema.domain.enums.TicketStatus;
import ru.barkhatnat.cinema.dto.create.TicketCreateDto;
import ru.barkhatnat.cinema.dto.regular.TicketDto;
import ru.barkhatnat.cinema.dto.update.TicketUpdateDto;
import ru.barkhatnat.cinema.exception.ForbiddenException;
import ru.barkhatnat.cinema.mapper.TicketMapper;
import ru.barkhatnat.cinema.repository.SeatRepository;
import ru.barkhatnat.cinema.repository.SessionRepository;
import ru.barkhatnat.cinema.repository.TicketRepository;
import ru.barkhatnat.cinema.repository.UserRepository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class TicketService {

    private final TicketRepository ticketRepository;
    private final TicketMapper ticketMapper;
    private final UserRepository userRepository;
    private final SessionRepository sessionRepository;
    private final SeatRepository seatRepository;
    private final OccupiedSeatsService occupiedSeatsService;


    public void deleteById(UUID id) {
        Ticket ticket = ticketRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        UUID sessionId = ticket.getSession().getId();
        UUID seatId = ticket.getSeat().getId();
        occupiedSeatsService.markSeatAsFree(sessionId, seatId);
        ticket.setStatus(TicketStatus.AVAILABLE);
        ticketRepository.save(ticket);
    }

    public TicketUpdateDto update(UUID id, TicketUpdateDto ticketUpdateDto) {
        Ticket existingTicket = ticketRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        UUID oldSessionId = existingTicket.getSession().getId();
        UUID oldSeatId = existingTicket.getSeat().getId();
        if (!ticketUpdateDto.sessionId().equals(oldSessionId) || !ticketUpdateDto.seatId().equals(oldSeatId)) {
            occupiedSeatsService.markSeatAsFree(oldSessionId, oldSeatId);
            if (occupiedSeatsService.isSeatOccupied(ticketUpdateDto.sessionId(), ticketUpdateDto.seatId())) {
                throw new ResponseStatusException(HttpStatus.CONFLICT, "New seat is already occupied");
            }
            occupiedSeatsService.markSeatAsOccupied(ticketUpdateDto.sessionId(), ticketUpdateDto.seatId());
        }
        ticketMapper.updateWithNull(ticketUpdateDto, existingTicket, userRepository, sessionRepository, seatRepository);
        Ticket updatedTicket = ticketRepository.save(existingTicket);
        return ticketMapper.toTicketUpdateDto(updatedTicket);
    }

    public List<TicketDto> findAll() {
        List<Ticket> tickets = ticketRepository.findAll();
        return tickets.stream()
                .map(ticketMapper::toTicketDto)
                .toList();
    }

    public List<TicketDto> findAll(UUID userId) {
        List<Ticket> tickets = ticketRepository.findByUserId(userId);
        return tickets.stream()
                .map(ticketMapper::toTicketDto)
                .toList();
    }

    public TicketDto findById(UUID ticketId, UUID userId) {
        checkTicketOwnership(ticketId, userId);
        Ticket ticket = ticketRepository.findById(ticketId).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(ticketId)));
        return ticketMapper.toTicketDto(ticket);
    }

    public TicketDto book(@Valid TicketCreateDto ticketCreateDto) {
        UUID sessionId = ticketCreateDto.sessionId();
        UUID seatId = ticketCreateDto.seatId();
        if (occupiedSeatsService.isSeatOccupied(sessionId, seatId)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Seat is already occupied");
        }
        occupiedSeatsService.markSeatAsOccupied(sessionId, seatId);
        Ticket ticket = ticketMapper.toEntity(ticketCreateDto, userRepository, sessionRepository, seatRepository);
        ticket.setPurchasedAt(LocalDateTime.now());
        ticket.setTicketCode(generateTicketCode());
        ticket.setStatus(TicketStatus.SOLD);
        Ticket savedTicket = ticketRepository.save(ticket);
        return ticketMapper.toTicketDto(savedTicket);
    }

    private void checkTicketOwnership(UUID ticketId, UUID userId) {
        RoleName userRoleName = userRepository.findById(userId).get().getRole().getName();
        Optional<Ticket> ticket = ticketRepository.findById(ticketId);
        if (ticket.isEmpty()
                || ticket.get().getUser() == null
                || (!ticket.get().getUser().getId().equals(userId)
                && userRoleName.equals(RoleName.ROLE_USER))) {
            throw new ForbiddenException("Access denied");
        }
    }

    private String generateTicketCode() {
        return UUID.randomUUID().toString().substring(0, 10).toUpperCase();
    }
}
