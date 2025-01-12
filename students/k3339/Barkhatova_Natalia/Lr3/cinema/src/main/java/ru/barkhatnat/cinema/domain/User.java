package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "\"user\"")
public class User {
    @Id
    @UuidGenerator
    private UUID id;

    @Column(unique = true, nullable = false, length = 50)
    @NotBlank(message = "Email cannot be blank")
    @Email(message = "Invalid email format")
    @Size(max = 50, min = 1, message = "Email must be at most 50 characters")
    private String email;

    @Column(nullable = false)
    @NotBlank(message = "Password cannot be blank")
    private String password;

    @Column(nullable = false, length = 50)
    @NotBlank(message = "First name cannot be blank")
    @Size(max = 50, min = 1, message = "First name must be at most 50 characters")
    private String firstName;

    @Column(nullable = false, length = 50)
    @NotBlank(message = "Last name cannot be blank")
    @Size(max = 50, min = 1, message = "Last name must be at most 50 characters")
    private String lastName;

    @Column(nullable = true, length = 50)
    @Size(max = 50, min = 1, message = "Middle name must be at most 50 characters")
    private String middleName;

    @ManyToOne
    @JoinColumn(name = "role_id", nullable = false)
    @NotNull(message = "Role cannot be null")
    private Role role;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Ticket> tickets = new ArrayList<>();

    public User(String email, String password, String firstName, String lastName, String middleName, Role role, List<Ticket> tickets) {
        this.email = email;
        this.password = password;
        this.firstName = firstName;
        this.lastName = lastName;
        this.middleName = middleName;
        this.role = role;
        this.tickets = tickets;
    }
}