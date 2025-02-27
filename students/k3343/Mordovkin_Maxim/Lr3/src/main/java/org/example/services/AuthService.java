package org.example.services;

import jakarta.ejb.Stateless;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.context.RequestScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;

import org.example.entities.AppUser;
import org.example.utils.JwtUtils;
import org.mindrot.jbcrypt.BCrypt;

import java.util.Optional;

/**
 * Сервис для регистрации и логина (получение JWT).
 */

@ApplicationScoped
public class AuthService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    /**
     * Регистрация нового пользователя
     * @param username логин
     * @param rawPassword пароль (в незашифрованном виде)
     * @param role роль пользователя (например, "ADMIN" или "USER")
     * @return строка — JWT-токен
     */
    @Transactional
    public String registerUser(String username, String rawPassword, String role) {
        // Проверяем, нет ли уже пользователя с таким логином
        Optional<AppUser> existingUser = em.createQuery(
                        "SELECT u FROM AppUser u WHERE u.username = :un", AppUser.class
                )
                .setParameter("un", username)
                .getResultStream()
                .findFirst();

        if (existingUser.isPresent()) {
            throw new RuntimeException("Пользователь с таким именем уже существует");
        }

        // Хешируем пароль (используем BCrypt)
        String hashed = BCrypt.hashpw(rawPassword, BCrypt.gensalt());
        AppUser newUser = new AppUser();
        newUser.setUsername(username);
        newUser.setPasswordHash(hashed);
        newUser.setRole(role);

        em.persist(newUser);

        // Сразу выдаём JWT-токен
        return JwtUtils.generateToken(username);
    }

    /**
     * Авторизация (логин) пользователя
     * @param username логин
     * @param rawPassword пароль (в незашифрованном виде)
     * @return строка — JWT-токен
     */
    public String login(String username, String rawPassword) {
        AppUser user = em.createQuery(
                        "SELECT u FROM AppUser u WHERE u.username = :un", AppUser.class
                )
                .setParameter("un", username)
                .getResultStream()
                .findFirst()
                .orElse(null);

        if (user == null) {
            throw new RuntimeException("Неверное имя пользователя или пароль");
        }

        // Сравниваем хеш
        if (!BCrypt.checkpw(rawPassword, user.getPasswordHash())) {
            throw new RuntimeException("Неверное имя пользователя или пароль");
        }

        // Если пароль корректен — выдаём токен
        return JwtUtils.generateToken(username);
    }

    /**
     * Найти пользователя по имени
     */
    public AppUser findByUsername(String username) {
        return em.createQuery(
                        "SELECT u FROM AppUser u WHERE u.username = :un", AppUser.class
                )
                .setParameter("un", username)
                .getResultStream()
                .findFirst()
                .orElse(null);
    }
}
