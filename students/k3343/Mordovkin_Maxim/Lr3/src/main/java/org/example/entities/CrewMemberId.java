//// src/main/java/org/example/entities/CrewMemberId.java
//package org.example.entities;
//
//import jakarta.persistence.Embeddable;
//import jakarta.persistence.JoinColumn;
//import jakarta.persistence.ManyToOne;
//import jakarta.persistence.OneToOne;
//import lombok.Getter;
//
//import java.io.Serializable;
//import java.util.Objects;
//
//@Getter
//@Embeddable
//public class CrewMemberId implements Serializable {
//
//    // Геттеры и Сеттеры
//    @OneToOne
//    @JoinColumn(name = "app_user_id", nullable = false)
//    private AppUser user;
//
//    @ManyToOne
//    @JoinColumn(name = "flight_id", nullable = false)
//    private Flight flight;
//
//    // Конструкторы
//    public CrewMemberId() {}
//
//    public CrewMemberId(AppUser user, Flight flight) {
//        this.user = user;
//        this.flight = flight;
//    }
//
//    public void setUser(AppUser user) {
//        this.user = user;
//    }
//
//    public void setFlight(Flight flight) {
//        this.flight = flight;
//    }
//
//    // equals и hashCode
//    @Override
//    public boolean equals(Object o) {
//        if (this == o) return true;
//        if (o == null || getClass() != o.getClass()) return false;
//
//        CrewMemberId that = (CrewMemberId) o;
//
//        if (!Objects.equals(user, that.user)) return false;
//        return Objects.equals(flight, that.flight);
//    }
//
//    @Override
//    public int hashCode() {
//        int result = user != null ? user.hashCode() : 0;
//        result = 31 * result + (flight != null ? flight.hashCode() : 0);
//        return result;
//    }
//}
