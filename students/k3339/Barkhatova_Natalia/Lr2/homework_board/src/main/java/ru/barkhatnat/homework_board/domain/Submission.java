package ru.barkhatnat.homework_board.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import org.antlr.v4.runtime.misc.NotNull;
import org.hibernate.annotations.UuidGenerator;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Getter
@Setter
@EqualsAndHashCode
public class Submission {
    @Id
    @UuidGenerator
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "homework_id", nullable = false)
    private Homework homework;

    @ManyToOne
    @JoinColumn(name = "student_id", nullable = false)
    private Student student;

    @NotNull
    private LocalDate submissionDate;

    private String content;

    private Integer grade;

    private String feedback;

    @Override
    public String toString() {
        return "Сдача домашней работы " + homework + " студентом " + student.getName();
    }
}