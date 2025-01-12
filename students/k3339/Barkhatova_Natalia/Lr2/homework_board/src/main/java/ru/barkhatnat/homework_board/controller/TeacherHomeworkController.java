package ru.barkhatnat.homework_board.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.homework_board.domain.Classroom;
import ru.barkhatnat.homework_board.domain.Homework;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.exception.ClassroomNotFoundException;
import ru.barkhatnat.homework_board.exception.HomeworkNotFoundException;
import ru.barkhatnat.homework_board.repository.ClassroomRepository;
import ru.barkhatnat.homework_board.repository.HomeworkRepository;
import ru.barkhatnat.homework_board.repository.MyUserRepository;

import java.util.List;
import java.util.UUID;

@Controller
@RequestMapping("teacher/homeworks")
public class TeacherHomeworkController extends HomeworkController {
    private final ClassroomRepository classroomRepository;

    public TeacherHomeworkController(HomeworkRepository homeworkRepository,
                                     MyUserRepository myUserRepository,
                                     ClassroomRepository classroomRepository) {
        super(homeworkRepository, myUserRepository);
        this.classroomRepository = classroomRepository;
    }

    @GetMapping("/create")
    public String showCreateForm(Model model) {
        model.addAttribute("homework", new Homework());
        MyUser teacher = getCurrentUser();
        List<Classroom> teacherClasses = classroomRepository.findByTeacherEmail(teacher.getEmail());

        model.addAttribute("teacherClasses", teacherClasses);
        model.addAttribute("classroom", new Classroom());
        return "teacher/homework/form";
    }

    @PostMapping
    public String createHomework(@ModelAttribute Homework homework) {
        if (homework.getClassroom() == null || homework.getClassroom().getId() == null) {
            throw new IllegalArgumentException("Classroom ID is required");
        }
        MyUser teacher = getCurrentUser();
        UUID classroomId = homework.getClassroom().getId();
        Classroom classroom = classroomRepository.findById(classroomId)
                .orElseThrow(() -> new ClassroomNotFoundException(classroomId));
        homework.setClassroom(classroom);
        homework.setActive(true);
        homeworkRepository.save(homework);

        return "redirect:/teacher/homeworks";
    }

    @GetMapping("/{id}/edit")
    public String showEditForm(@PathVariable UUID id, Model model) {
        Homework homework = homeworkRepository.findById(id)
                .orElseThrow(() -> new HomeworkNotFoundException(id));
        List<Classroom> teacherClasses = classroomRepository.findByTeacherEmail(homework.getClassroom().getTeacher().getEmail());
        model.addAttribute("homework", homework);
        model.addAttribute("teacherClasses", teacherClasses);
        return "teacher/homework/form";
    }

    @PostMapping("/edit")
    public String updateHomework(@ModelAttribute Homework homework) {
        Homework existingHomework = homeworkRepository.findById(homework.getId()).get();
        existingHomework.setActive(homework.isActive());
        existingHomework.setDescription(homework.getDescription());
        existingHomework.setClassroom(homework.getClassroom());
        existingHomework.setMaxGrade(homework.getMaxGrade());
        existingHomework.setNumber(homework.getNumber());
        existingHomework.setExecutionPeriod(homework.getExecutionPeriod());
        existingHomework.setPenaltyInfo(homework.getPenaltyInfo());
        existingHomework.setDueDate(homework.getDueDate());
        homeworkRepository.save(existingHomework);
        return "redirect:/teacher/classrooms";
    }

    @GetMapping("/{id}/delete")
    public String deleteHomework(@PathVariable UUID id) {
        homeworkRepository.deleteById(id);
        return "redirect:/teacher/homeworks";
    }
}

