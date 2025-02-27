package org.example.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import jakarta.enterprise.context.ApplicationScoped;
import java.security.Key;
import java.util.Date;

@ApplicationScoped
public class JwtUtil {

    // Секретный ключ для подписи JWT
    private final Key key = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    // Генерация JWT
    public String generateToken(String username) {
        long nowMillis = System.currentTimeMillis();
        long expMillis = nowMillis + 3600000; // Токен действителен 1 час
        Date exp = new Date(expMillis);

        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(new Date(nowMillis))
                .setExpiration(exp)
                .signWith(key)
                .compact();
    }

    // Валидация JWT
    public String validateToken(String token) throws JwtException {
        Jws<Claims> claims = Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token);
        return claims.getBody().getSubject();
    }
}
