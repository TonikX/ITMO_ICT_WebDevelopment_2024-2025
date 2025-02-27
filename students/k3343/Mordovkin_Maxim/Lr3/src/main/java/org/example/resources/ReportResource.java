package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;

import org.example.services.ReportService;

import java.util.List;
import java.util.Map;

/**
 * REST-эндпоинты для "отчетов" по заданию
 */
@Path("/reports")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ReportResource {

    @Inject
    private ReportService reportService;

    /**
     * (1) Получить тип самолета, который чаще всего летает по маршруту
     * @param departure пункт вылета
     * @param destination пункт назначения
     */
    @GET
    @Path("/most-frequent-aircraft-type")
    public String getMostFrequentAircraftType(
            @QueryParam("departure") String departure,
            @QueryParam("destination") String destination
    ) {
        return reportService.findMostFrequentAircraftType(departure, destination);
    }

    /**
     * (2) Маршруты, где рейсы заполнены менее, чем на <occupancy>%
     * @param occupancy Процент (0..100)
     */
    @GET
    @Path("/routes-below-occupancy")
    public List<String> getRoutesBelowOccupancy(@QueryParam("occupancy") double occupancy) {
        return reportService.findRoutesBelowOccupancy(occupancy);
    }

    /**
     * (4) Определить количество самолетов в ремонте
     */
    @GET
    @Path("/aircrafts-in-repair-count")
    public int getAircraftsInRepairCount() {
        return reportService.countAircraftsInRepair();
    }

    /**
     * (5) Количество работников авиаперевозчика
     */
    @GET
    @Path("/carrier-workers-count/{carrierId}")
    public int getWorkersCount(@PathParam("carrierId") Long carrierId) {
        return reportService.countWorkersOfCarrier(carrierId);
    }

    /**
     * (6) Отчёт по бортам для компании-владельца
     */
    @GET
    @Path("/aircrafts-report-by-type/{carrierId}")
    public Map<String, Object> getAircraftReportByType(@PathParam("carrierId") Long carrierId) {
        return reportService.getAircraftReportByType(carrierId);
    }
}
