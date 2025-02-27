package org.example.repositories;

import org.example.entities.User;
import java.util.List;

public interface UserRepository {
    void createUser(User user);
    User findUserById(Long id);
    List<User> findAllUsers();
    void updateUser(User user);
    void deleteUser(Long id);

    // Добавленный метод
    User findByUsername(String username);
}
