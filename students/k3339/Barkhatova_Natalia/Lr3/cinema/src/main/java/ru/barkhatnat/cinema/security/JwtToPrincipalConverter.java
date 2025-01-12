package ru.barkhatnat.cinema.security;

import com.auth0.jwt.interfaces.DecodedJWT;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;
import ru.barkhatnat.cinema.domain.User;
import ru.barkhatnat.cinema.repository.UserRepository;

import java.util.List;
import java.util.UUID;

@Component
@RequiredArgsConstructor
public class JwtToPrincipalConverter {
    private final UserRepository userRepository;
    public CustomUserDetails convert(DecodedJWT jwt) {
        UUID userId = UUID.fromString(jwt.getSubject());

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found with ID: " + userId));

        return CustomUserDetails.builder()
                .user(user)
                .build();
    }

    private List<SimpleGrantedAuthority> extractAuthoritiesFromClaim(DecodedJWT jwt) {
        var claim = jwt.getClaim("roles");
        if (claim.isNull() || claim.isMissing()) {
            return List.of();
        }
        return claim.asList(SimpleGrantedAuthority.class);
    }
}
