package ru.barkhatnat.homework_board.domain;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.OneToMany;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;
import java.util.Objects;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Student extends MyUser {

    @ManyToMany
    private List<Homework> homeworks;

    @ManyToMany(mappedBy = "students")
    private List<Classroom> classrooms;

    @OneToMany(mappedBy = "student",cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Submission> submissions;

    public Student(String email, String password, Role role, String name, String lastName, String middleName, List<Homework> homeworks, List<Submission> submissions, List<Classroom> classrooms) {
        super(email, password, role, name, lastName, middleName);
        this.homeworks = homeworks;
        this.submissions = submissions;
        this.classrooms = classrooms;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        if (!super.equals(o)) return false;
        Student student = (Student) o;
        return Objects.equals(homeworks, student.homeworks) &&
                Objects.equals(classrooms, student.classrooms) &&
                Objects.equals(submissions, student.submissions);
    }

    @Override
    public int hashCode() {
        return Objects.hash(super.hashCode(), homeworks, classrooms, submissions);
    }
}
