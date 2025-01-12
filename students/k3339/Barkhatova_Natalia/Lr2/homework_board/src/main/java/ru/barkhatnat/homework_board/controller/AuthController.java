package ru.barkhatnat.homework_board.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.exception.UserAlreadyExistsException;
import ru.barkhatnat.homework_board.service.MyUserService;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class AuthController {
    private final MyUserService myUserService;

    @GetMapping("/login")
    public String loginPage() {
        return "login";
    }

    @GetMapping("/logout-success")
    public String logoutPage() {
        return "logout";
    }


    @GetMapping("/registration")
    public String registrationForm(Model model) {
        model.addAttribute("roles", MyUser.Role.values());
        return "registration";
    }

    @PostMapping("/registration")
    public String createAccount(@ModelAttribute MyUser myUser, BindingResult bindingResult, Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("errors", bindingResult.getAllErrors());
            model.addAttribute("roles", MyUser.Role.values());
            return "registration";
        } else {
            try {
                myUserService.createUser(myUser);
                return "redirect:/login";
            } catch (UserAlreadyExistsException e) {
                model.addAttribute("error", "Пользователь с таким email уже существует.");
                model.addAttribute("roles", MyUser.Role.values());
                return "registration";
            }
        }
    }

    @GetMapping("/home")
    public String dashboardPage() {
        var authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()) {
            return "redirect:/login";
        }

        List<String> roles = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .toList();

        if (roles.contains("ROLE_TEACHER")) {
            return "teacher/teacher-dashboard";
        } else if (roles.contains("ROLE_STUDENT")) {
            return "student/student-dashboard";
        }
        return "access-denied";
    }
}
