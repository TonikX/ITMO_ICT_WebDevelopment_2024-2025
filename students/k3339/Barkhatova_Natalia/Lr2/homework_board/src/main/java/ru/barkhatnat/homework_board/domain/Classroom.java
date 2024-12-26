package ru.barkhatnat.homework_board.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.UuidGenerator;

import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
public class Classroom {
    @Id
    @UuidGenerator
    private UUID id;

    @Column(nullable = false, unique = true, length = 10)
    private String name;

    @ManyToOne
    @JoinColumn(name = "subject_id", nullable = false)
    private Subject subject;

    @ManyToOne
    @JoinColumn(name = "teacher_id", nullable = false)
    private Teacher teacher;

    @OneToMany(mappedBy = "classroom",cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Homework> homeworks;

    @ManyToMany
    private List<Student> students;
}