// src/main/java/org/example/entities/CrewMember.java
package org.example.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "crew_member")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class CrewMember {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long crewMemberId;

    @Column(nullable = false)
    private String fullName;

    @Column(nullable = false)
    private int age;

    private String education;

    @Column(nullable = false)
    private int workExperience;

    @Column(nullable = false)
    private String passportData;

    @Column(nullable = false)
    private String permissionType;

    @Column(nullable = false)
    private String employmentStatus;  // PENDING, WORKING, FIRED

    @Column(nullable = false)
    private String roleName;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "flight_id", nullable = false)
    @JsonBackReference("flight-crewMembers") // Уникальный идентификатор
    private Flight flight;

    @ManyToOne
    @JoinColumn(name = "app_user_id") // столбец в таблице crew_member
    @JsonIgnore
    private AppUser user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crew_id")
    @JsonBackReference("crew-crewMembers") // Уникальный идентификатор
    private Crew crew;
}

