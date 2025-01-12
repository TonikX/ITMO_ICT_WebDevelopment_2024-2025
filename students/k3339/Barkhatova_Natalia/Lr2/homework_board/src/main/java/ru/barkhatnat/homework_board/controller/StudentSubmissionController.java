package ru.barkhatnat.homework_board.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.homework_board.domain.Homework;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.domain.Student;
import ru.barkhatnat.homework_board.domain.Submission;
import ru.barkhatnat.homework_board.exception.HomeworkNotFoundException;
import ru.barkhatnat.homework_board.exception.UserNotFoundException;
import ru.barkhatnat.homework_board.repository.HomeworkRepository;
import ru.barkhatnat.homework_board.repository.MyUserRepository;
import ru.barkhatnat.homework_board.repository.SubmissionRepository;

import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

@Controller
@RequestMapping("student/submissions")
@RequiredArgsConstructor
public class StudentSubmissionController {

    private final SubmissionRepository submissionRepository;
    private final HomeworkRepository homeworkRepository;
    private final MyUserRepository myUserRepository;

    @PostMapping("/{id}")
    public String createSubmission(@PathVariable UUID id, @ModelAttribute Submission submission) {
        Homework homework = homeworkRepository.findById(id).orElseThrow(
                () -> new HomeworkNotFoundException(id));
        submission.setHomework(homework);
        submission.setStudent((Student) getCurrentUser());
        submission.setSubmissionDate(LocalDate.now());
        submissionRepository.save(submission);
        return "redirect:/student/homeworks";
    }

    @GetMapping("/{id}/create")
    public String showSubmissionForm(@PathVariable UUID id, Model model) {
        MyUser currentUser = getCurrentUser();
        Optional<Submission> existingSubmission = submissionRepository
                .findByHomeworkIdAndStudentId(id, currentUser.getId())
                .stream()
                .findFirst();

        if (existingSubmission.isPresent()) {
            model.addAttribute("submission", existingSubmission.get());
            model.addAttribute("homework_id", id);
            model.addAttribute("alreadySubmitted", true);
            return "student/submission/form";
        }

        model.addAttribute("submission", new Submission());
        model.addAttribute("homework_id", id);
        model.addAttribute("alreadySubmitted", false);
        return "student/submission/form";
    }

    @GetMapping("/{id}")
    public String checkSubmission(@PathVariable UUID id, Model model) {
        MyUser currentUser = getCurrentUser();
        Optional<Submission> submission = submissionRepository.findByHomeworkIdAndStudentId(id, currentUser.getId()).stream()
                .findFirst();
        if (submission.isPresent()) {
            model.addAttribute("hasSubmission", true);
            model.addAttribute("submission", submission.get());
        } else {
            model.addAttribute("hasSubmission", false);
        }

        model.addAttribute("homework_id", id);
        return "student/submission/check";
    }


    protected MyUser getCurrentUser() {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();
        return myUserRepository.findByEmail(email)
                .orElseThrow(() -> new UserNotFoundException(email));
    }
}
