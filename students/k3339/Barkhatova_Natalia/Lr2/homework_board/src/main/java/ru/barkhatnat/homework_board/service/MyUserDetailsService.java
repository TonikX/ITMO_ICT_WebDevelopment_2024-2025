package ru.barkhatnat.homework_board.service;

import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.InternalAuthenticationServiceException;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.domain.security.UserPrincipal;
import ru.barkhatnat.homework_board.repository.MyUserRepository;

import java.util.List;
import java.util.Optional;

@RequiredArgsConstructor
@Service
public class MyUserDetailsService implements UserDetailsService {
    private final MyUserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        try {
            Optional<MyUser> user = userRepository.findByEmail(email);
            if (user.isEmpty()) {
                throw new UsernameNotFoundException("User not found");
            }
            return UserPrincipal.builder()
                    .userId(user.get().getId())
                    .email(user.get().getEmail())
                    .password(user.get().getPassword())
                    .authorities(List.of(new SimpleGrantedAuthority("ROLE_" + user.get().getRole().toString()))).build();
        } catch (Exception e) {
            throw new InternalAuthenticationServiceException("An internal error occurred while trying to authenticate the user.", e);
        }
    }
}
