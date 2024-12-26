package ru.barkhatnat.homework_board.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.antlr.v4.runtime.misc.NotNull;
import org.hibernate.annotations.UuidGenerator;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
public class Homework {
    @Id
    @UuidGenerator
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "classroom_id", nullable = false)
    private Classroom classroom;

    @NotNull
    private LocalDate dueDate;

    private int executionPeriod;

    @NotNull
    private int number;

    private String description;

    private String penaltyInfo;

    @Column(nullable = false)
    private boolean isActive;

    @NotNull
    private int maxGrade;

    @OneToMany(mappedBy = "homework", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Submission> submissions;
}