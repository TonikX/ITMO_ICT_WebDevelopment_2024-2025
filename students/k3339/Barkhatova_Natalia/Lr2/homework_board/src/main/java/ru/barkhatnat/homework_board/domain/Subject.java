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
public class Subject {
    @Id
    @UuidGenerator
    private UUID id;

    @Column(nullable = false)
    private String name;

    @ManyToOne
    @JoinColumn(name = "teacher_id", nullable = false)
    private Teacher teacher;

    @OneToMany(mappedBy = "subject")
    private List<Classroom> classrooms;

    @Override
    public String toString() {
        return name;
    }
}