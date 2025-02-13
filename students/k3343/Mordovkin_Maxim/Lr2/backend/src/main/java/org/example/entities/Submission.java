package org.example.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
//import org.hibernate.sql.ast.tree.update.Assignment;

import java.time.LocalDateTime;

@Getter
@Setter
@Entity
@Table(name = "submissions")
public class Submission {

    // Геттеры/сеттеры
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long submissionId;

    // Связь с assignment. (многие сдачи -> одно задание)
    @ManyToOne
    @JoinColumn(name = "assignment_id", nullable = false)
    private Assignment assignment;

    // Кто (ученик) сдал
    @ManyToOne
    @JoinColumn(name = "student_id", nullable = false)
    private User student;

    // Текст ответа
    @Column(nullable = false)
    private String content;

    // Оценка 0..100
    private Integer grade;

    // Когда сдал
    @Column(nullable = false)
    private LocalDateTime submittedAt;


}
