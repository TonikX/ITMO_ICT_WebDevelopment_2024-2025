package ru.barkhatnat.homework_board.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.domain.Subject;
import ru.barkhatnat.homework_board.domain.Teacher;
import ru.barkhatnat.homework_board.exception.SubjectNotFoundException;
import ru.barkhatnat.homework_board.exception.UserNotFoundException;
import ru.barkhatnat.homework_board.repository.MyUserRepository;
import ru.barkhatnat.homework_board.repository.SubjectRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Controller
@RequestMapping("teacher/subjects")
@RequiredArgsConstructor
public class SubjectController {

    private final SubjectRepository subjectRepository;
    private final MyUserRepository myUserRepository;

    @GetMapping
    public String getAllSubjects(Model model) {
        List<Subject> subjects = subjectRepository.findAll();
        model.addAttribute("subjects", subjects);
        return "teacher/subject/list";
    }

    @GetMapping("/create")
    public String showCreateForm(Model model) {
        model.addAttribute("subject", new Subject());
        return "teacher/subject/form";
    }

    @PostMapping
    public String createSubject(@ModelAttribute Subject subject) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String email = authentication.getName();

        Optional<MyUser> teacher = myUserRepository.findByEmail(email);
        if (teacher.isPresent()) {
            subject.setTeacher((Teacher) teacher.get());
        } else {
            throw new UserNotFoundException(email);
        }
        subjectRepository.save(subject);
        return "redirect:/teacher/subjects";
    }

    @GetMapping("/{id}/edit")
    public String showEditForm(@PathVariable UUID id, Model model) {
        Subject subject = subjectRepository.findById(id)
                .orElseThrow(() -> new SubjectNotFoundException(id));
        model.addAttribute("subject", subject);
        return "teacher/subject/form";
    }

    @PostMapping("/edit")
    public String updateSubject(@ModelAttribute Subject subject) {
        Subject existingSubject = subjectRepository.findById(subject.getId()).get();
        existingSubject.setName(subject.getName());
        subjectRepository.save(existingSubject);
        return "redirect:/teacher/subjects";
    }

    @GetMapping("/{id}/delete")
    public String deleteSubject(@PathVariable UUID id) {
        subjectRepository.deleteById(id);
        return "redirect:/teacher/subjects";
    }
}
