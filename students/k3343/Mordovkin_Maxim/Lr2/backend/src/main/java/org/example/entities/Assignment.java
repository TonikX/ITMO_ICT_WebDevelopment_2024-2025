// Файл: org.example.entities.Assigment
// Переименуйте в Assignment.java

package org.example.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@Entity
@Table(name = "assignments")
public class Assignment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long assignmentId;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private LocalDateTime dueDate; // срок выполнения

    // Кто создал (Teacher)
    @ManyToOne
    @JoinColumn(name = "teacher_id", nullable = false)
    private User teacher;


}
