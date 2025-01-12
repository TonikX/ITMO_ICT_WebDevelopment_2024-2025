package ru.barkhatnat.cinema.util;

import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationCredentialsNotFoundException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import ru.barkhatnat.cinema.security.CustomUserDetails;

@Component
@RequiredArgsConstructor
public class SecurityUtil {

    public Authentication getAuthentication() {
        return SecurityContextHolder.getContext().getAuthentication();
    }

    public CustomUserDetails getCurrentUserDetails() throws AuthenticationException {
        Authentication authentication = getAuthentication();
        if (authentication != null && authentication.isAuthenticated() && authentication.getPrincipal() instanceof UserDetails) {
            return (CustomUserDetails) authentication.getPrincipal();
        }
        throw new AuthenticationCredentialsNotFoundException("User is not authenticated");
    }
}
