package ru.barkhatnat.cinema.mapper;

import org.mapstruct.*;
import ru.barkhatnat.cinema.domain.Seat;
import ru.barkhatnat.cinema.domain.Session;
import ru.barkhatnat.cinema.domain.Ticket;
import ru.barkhatnat.cinema.domain.User;
import ru.barkhatnat.cinema.dto.create.TicketCreateDto;
import ru.barkhatnat.cinema.dto.regular.TicketDto;
import ru.barkhatnat.cinema.dto.update.TicketUpdateDto;
import ru.barkhatnat.cinema.repository.SeatRepository;
import ru.barkhatnat.cinema.repository.SessionRepository;
import ru.barkhatnat.cinema.repository.UserRepository;

import java.util.UUID;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE, componentModel = MappingConstants.ComponentModel.SPRING, uses = {UserMapper.class, SessionMapper.class, SeatMapper.class})
public interface TicketMapper {
    TicketDto toTicketDto(Ticket ticket);

    @Mapping(target = "user", source = "userId", qualifiedByName = "mapUser")
    @Mapping(target = "session", source = "sessionId", qualifiedByName = "mapSession")
    @Mapping(target = "seat", source = "seatId", qualifiedByName = "mapSeat")
    Ticket toEntity(TicketCreateDto ticketCreateDto,  @Context UserRepository userRepository,
                    @Context SessionRepository sessionRepository, @Context SeatRepository seatRepository);

    @Named("mapUser")
    default User mapUser(UUID userId, @Context UserRepository userRepository) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found for ID: " + userId));
    }

    @Named("mapSession")
    default Session mapSession(UUID sessionId, @Context SessionRepository sessionRepository) {
        return sessionRepository.findById(sessionId)
                .orElseThrow(() -> new RuntimeException("Session not found for ID: " + sessionId));
    }

    @Named("mapSeat")
    default Seat mapSeat(UUID seatId, @Context SeatRepository seatRepository) {
        return seatRepository.findById(seatId)
                .orElseThrow(() -> new RuntimeException("Seat not found for ID: " + seatId));
    }
    Ticket toEntity(TicketDto ticketDto);

    TicketUpdateDto toTicketUpdateDto(Ticket ticket);

    @Mapping(target = "user", source = "userId", qualifiedByName = "mapUser")
    @Mapping(target = "session", source = "sessionId", qualifiedByName = "mapSession")
    @Mapping(target = "seat", source = "seatId", qualifiedByName = "mapSeat")
    Ticket updateWithNull(TicketUpdateDto ticketUpdateDto, @MappingTarget Ticket ticket, @Context UserRepository userRepository,
                          @Context SessionRepository sessionRepository, @Context SeatRepository seatRepository);
}