package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;

import org.example.entities.Flight;
import org.example.entities.Aircraft;
import org.example.entities.AircraftMaintenance;
import org.example.entities.CrewMember;

import java.util.*;
import java.util.stream.Collectors;


@ApplicationScoped
public class ReportService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    /**
     * (1) Выбрать тип самолёта, который чаще всего летает по указанному маршруту
     * Под "маршрутом" понимается (departurePoint -> destinationPoint).
     */
    @Transactional
    public String findMostFrequentAircraftType(String departure, String destination) {
        // Пример: группируем рейсы по типу самолёта
        List<Object[]> results = em.createQuery("""
                SELECT f.aircraft.aircraftType, COUNT(f)
                FROM Flight f
                WHERE f.departurePoint = :dep AND f.destinationPoint = :dest
                GROUP BY f.aircraft.aircraftType
                ORDER BY COUNT(f) DESC
                """, Object[].class)
                .setParameter("dep", departure)
                .setParameter("dest", destination)
                .getResultList();

        if (results.isEmpty()) {
            return "Нет данных по маршруту " + departure + " -> " + destination;
        }
        // Первый — самый часто летающий тип
        return (String) results.get(0)[0];
    }

    /**
     * (2) Выбрать маршруты, по которым рейсы заполнены менее, чем на <occupancy>%.
     */
    @Transactional
    public List<String> findRoutesBelowOccupancy(double occupancy) {
        // Ищем все рейсы, считаем текущую заполненность
        List<Flight> flights = em.createQuery("SELECT f FROM Flight f", Flight.class)
                .getResultList();

        Set<String> routesBelow = new HashSet<>();

        for (Flight f : flights) {
            Aircraft a = f.getAircraft();
            if (a == null) continue;

            int seats = a.getSeats();
            int sold = f.getTicketsSold();
            double currentOccupancy = (double) sold / seats * 100.0;

            if (currentOccupancy < occupancy) {
                String route = f.getDeparturePoint() + " -> " + f.getDestinationPoint();
                routesBelow.add(route);
            }
        }

        // Превратим в список
        return new ArrayList<>(routesBelow);
    }

    /**
     * (4) Определить количество самолетов, находящихся в ремонте (maintenanceStatus = "IN_REPAIR")
     */
    @Transactional
    public int countAircraftsInRepair() {
        Long count = em.createQuery("""
                SELECT COUNT(m) 
                FROM AircraftMaintenance m 
                WHERE m.maintenanceStatus = :status
                """, Long.class)
                .setParameter("status", "IN_REPAIR")
                .getSingleResult();
        return count.intValue();
    }

    /**
     * (5) Определить количество работников компании-авиаперевозчика
     * (учитываем CrewMember, которые связаны через Crew -> Flight -> Aircraft -> Carrier)
     */
    @Transactional
    public int countWorkersOfCarrier(Long carrierId) {
        List<CrewMember> crewMembers = em.createQuery("""
                SELECT cm
                FROM CrewMember cm
                JOIN cm.crew c
                JOIN c.flight f
                JOIN f.aircraft a
                JOIN a.carrier carrier
                WHERE carrier.carrierID = :cid
                """, CrewMember.class)
                .setParameter("cid", carrierId)
                .getResultList();

        return crewMembers.size();
    }

    /**
     * (6) Отчёт по бортам компании-владельца (carrierId) —
     *     общее количество бортов и количество по каждой марке (типу).
     */
    @Transactional
    public Map<String, Object> getAircraftReportByType(Long carrierId) {
        Map<String, Object> result = new HashMap<>();

        // Список всех самолётов данного carrier
        List<Aircraft> aircraftList = em.createQuery("""
                SELECT a
                FROM Aircraft a
                WHERE a.carrier.carrierID = :cid
                """, Aircraft.class)
                .setParameter("cid", carrierId)
                .getResultList();

        int total = aircraftList.size();
        result.put("totalAircraft", total);

        // Сгруппируем по типу самолёта
        Map<String, Long> byType = aircraftList.stream()
                .collect(Collectors.groupingBy(Aircraft::getAircraftType, Collectors.counting()));

        result.put("byType", byType);

        return result;
    }
}
