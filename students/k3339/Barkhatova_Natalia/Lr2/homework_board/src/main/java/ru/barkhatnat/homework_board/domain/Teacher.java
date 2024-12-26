package ru.barkhatnat.homework_board.domain;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Teacher extends MyUser {

    @OneToMany(mappedBy = "teacher", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Subject> subjects;

    public Teacher(String email, String password, Role role, String name, String lastName, String middleName, List<Subject> subjects) {
        super(email, password, role, name, lastName, middleName);
        this.subjects = subjects;
    }
}
