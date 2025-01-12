package ru.barkhatnat.homework_board.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.barkhatnat.homework_board.domain.MyUser;

import java.util.Optional;
import java.util.UUID;
@Repository
public interface MyUserRepository extends JpaRepository<MyUser, UUID> {
    Optional<MyUser> findByEmail(String email);
}