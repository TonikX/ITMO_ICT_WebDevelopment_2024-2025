package org.example.entities;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString(exclude = "password")
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    // Роли: "Teacher" или "Student"
    @Column(nullable = false)
    private String role;

    // Поле для ученика (1..11). Для учителя может быть null
    private Integer classNumber;

    @JsonIgnore
    @Column(nullable = false)
    private String passwordHash;

    @Transient
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    private String password;

    // Пример: можно добавить fullName, если нужно
    // private String fullName;
}
