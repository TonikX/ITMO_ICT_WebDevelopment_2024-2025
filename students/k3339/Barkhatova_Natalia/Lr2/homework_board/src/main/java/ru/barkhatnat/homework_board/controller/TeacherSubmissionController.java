package ru.barkhatnat.homework_board.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.homework_board.domain.Homework;
import ru.barkhatnat.homework_board.domain.Submission;
import ru.barkhatnat.homework_board.exception.SubjectNotFoundException;
import ru.barkhatnat.homework_board.exception.SubmissionNotFoundException;
import ru.barkhatnat.homework_board.repository.HomeworkRepository;
import ru.barkhatnat.homework_board.repository.MyUserRepository;
import ru.barkhatnat.homework_board.repository.SubmissionRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Controller
@RequestMapping("teacher/submissions")
@RequiredArgsConstructor
public class TeacherSubmissionController {
    private final SubmissionRepository submissionRepository;
    private final HomeworkRepository homeworkRepository;
    private final MyUserRepository myUserRepository;

    @GetMapping("/{homeworkId}")
    public String getSubmissionsForHomework(@PathVariable UUID homeworkId, Model model) {
        Optional<Homework> homework = homeworkRepository.findById(homeworkId);
        if (homework.isEmpty()) {
            return "redirect:/homeworks";
        }
        List<Submission> allSubmissions = submissionRepository.findByHomeworkId(homeworkId);
        List<Submission> ungradedSubmissions = allSubmissions.stream()
                .filter(submission -> submission.getGrade() == null)
                .collect(Collectors.toList());
        List<Submission> gradedSubmissions = allSubmissions.stream()
                .filter(submission -> submission.getGrade() != null)
                .collect(Collectors.toList());
        model.addAttribute("homework", homework.get());
        model.addAttribute("ungradedSubmissions", ungradedSubmissions);
        model.addAttribute("gradedSubmissions", gradedSubmissions);
        return "teacher/submission/list";
    }

    @GetMapping("/{homeworkId}/grade/{submissionId}")
    public String gradeSubmission(@PathVariable UUID homeworkId, @PathVariable UUID submissionId, Model model) {
        Homework homework = homeworkRepository.findById(homeworkId).get();
        Submission submission = submissionRepository.findById(submissionId).orElseThrow(() -> new SubmissionNotFoundException(submissionId));
        model.addAttribute("submission", submission);
        model.addAttribute("homework", homework);
        return "teacher/submission/grade";
    }

    @PostMapping("/{homeworkId}/grade/{submissionId}")
    public String saveGrade(
            @PathVariable UUID homeworkId,
            @PathVariable UUID submissionId,
            @RequestParam("grade") Integer grade,
            @RequestParam("feedback") String feedback) {
        Submission submission = submissionRepository.findById(submissionId)
                .orElseThrow(() -> new SubmissionNotFoundException(submissionId));
        Homework homework = homeworkRepository.findById(homeworkId)
                .orElseThrow(() -> new SubjectNotFoundException(homeworkId));
        int maxGrade = homework.getMaxGrade();
        if (grade <= 0 || grade > maxGrade) {
            throw new IllegalArgumentException("Оценка должна быть в пределах от 1 до " + maxGrade);
        }
        submission.setGrade(grade);
        submission.setFeedback(feedback);
        submissionRepository.save(submission);
        return "redirect:/teacher/submissions/" + homeworkId;
    }

    @GetMapping("/{homeworkId}/view/{submissionId}")
    public String viewSubmissionContent(@PathVariable UUID homeworkId, @PathVariable UUID submissionId, Model model) {
        Submission submission = submissionRepository.findById(submissionId)
                .orElseThrow(() -> new SubmissionNotFoundException(submissionId));
        model.addAttribute("submission", submission);
        model.addAttribute("homeworkId", homeworkId);
        return "teacher/submission/show-content";
    }
}
