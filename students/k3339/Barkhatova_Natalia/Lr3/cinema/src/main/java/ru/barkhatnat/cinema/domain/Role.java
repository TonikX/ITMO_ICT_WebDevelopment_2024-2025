package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;
import ru.barkhatnat.cinema.domain.enums.RoleName;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Role {
    @Id
    @UuidGenerator
    private UUID id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @NotNull(message = "Role name cannot be null")
    private RoleName name;

    @OneToMany(mappedBy = "role", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<User> users = new ArrayList<>();

    public Role(RoleName name, List<User> users) {
        this.name = name;
        this.users = users;
    }
}