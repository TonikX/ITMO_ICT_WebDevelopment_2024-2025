package ru.barkhatnat.cinema.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import ru.barkhatnat.cinema.domain.Role;

import java.util.UUID;

public interface RoleRepository extends JpaRepository<Role, UUID>, JpaSpecificationExecutor<Role> {
}