package ru.barkhatnat.homework_board.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import ru.barkhatnat.homework_board.domain.Homework;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.domain.Student;
import ru.barkhatnat.homework_board.domain.Teacher;
import ru.barkhatnat.homework_board.exception.UserNotFoundException;
import ru.barkhatnat.homework_board.repository.HomeworkRepository;
import ru.barkhatnat.homework_board.repository.MyUserRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Controller
@RequiredArgsConstructor
public abstract class HomeworkController {
    protected final HomeworkRepository homeworkRepository;
    protected final MyUserRepository myUserRepository;

    @GetMapping
    public String getHomeworks(Model model) {
        MyUser currentUser = getCurrentUser();
        List<Homework> homeworks = findHomeworksForUser(currentUser);
        model.addAttribute("homeworks", homeworks);
        return determineViewForUser(currentUser) + "/list";
    }

    protected List<Homework> findHomeworksForUser(MyUser user) {
        if (user instanceof Student student) {
            return homeworkRepository.findByStudentId(student.getId());
        } else if (user instanceof Teacher teacher) {
            return homeworkRepository.findByTeacherId(teacher.getId());
        } else {
            throw new IllegalArgumentException("Unknown user type");
        }
    }

    protected String determineViewForUser(MyUser user) {
        if (user instanceof Student) {
            return "student/homework";
        } else if (user instanceof Teacher) {
            return "teacher/homework";
        } else {
            throw new IllegalArgumentException("Unknown user type");
        }
    }

    protected MyUser getCurrentUser() {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();
        return myUserRepository.findByEmail(email)
                .orElseThrow(() -> new UserNotFoundException(email));
    }

    @GetMapping("/{id}")
    public String getHomeworkDetails(@PathVariable UUID id, Model model) {
        MyUser currentUser = getCurrentUser();
        Optional<Homework> homework = homeworkRepository.findById(id);
        if (homework.isPresent()) {
            model.addAttribute("homework", homework.get());
            return determineViewForUser(currentUser) + "/details";
        } else {
            return "redirect:/" + determineViewForUser(currentUser);
        }
    }
}
