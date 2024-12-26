package ru.barkhatnat.homework_board.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.homework_board.domain.*;
import ru.barkhatnat.homework_board.exception.ClassroomNotFoundException;
import ru.barkhatnat.homework_board.exception.UserNotFoundException;
import ru.barkhatnat.homework_board.repository.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Controller
@RequestMapping("teacher/classrooms")
@RequiredArgsConstructor
public class ClassroomController {

    private final ClassroomRepository classroomRepository;
    private final MyUserRepository myUserRepository;
    private final StudentRepository studentRepository;
    private final SubjectRepository subjectRepository;
    private final SubmissionRepository submissionRepository;
    private final HomeworkRepository homeworkRepository;

    @GetMapping
    public String getAllClassrooms(Model model) {
        List<Classroom> classrooms = classroomRepository.findAll();
        model.addAttribute("classrooms", classrooms);
        return "teacher/classroom/list";
    }

    @GetMapping("/create")
    public String showCreateForm(Model model) {
        MyUser teacher = getCurrentUser();
        List<Subject> teacherSubjects = subjectRepository.findByTeacherEmail(teacher.getEmail());
        model.addAttribute("teacherSubjects", teacherSubjects);
        model.addAttribute("classroom", new Classroom());
        model.addAttribute("subject", new Subject());
        model.addAttribute("students", studentRepository.findAll());
        return "teacher/classroom/form";
    }

    @PostMapping
    public String createClassroom(@ModelAttribute Classroom classroom) {
        MyUser teacher = getCurrentUser();
        classroom.setTeacher((Teacher) teacher);
        for (Student student : classroom.getStudents()) {
            student.getClassrooms().add(classroom);
        }
        classroomRepository.save(classroom);
        return "redirect:/teacher/classrooms";
    }

    @GetMapping("/{id}/edit")
    public String showEditForm(@PathVariable UUID id, Model model) {
        Classroom classroom = classroomRepository.findById(id)
                .orElseThrow(() -> new ClassroomNotFoundException(id));
        List<Subject> teacherSubjects = subjectRepository.findByTeacherEmail(classroom.getTeacher().getEmail());
        model.addAttribute("classroom", classroom);
        model.addAttribute("teacherSubjects", teacherSubjects);
        model.addAttribute("subject", new Subject());
        model.addAttribute("students", studentRepository.findAll());
        return "teacher/classroom/form";
    }

    @PostMapping("/edit")
    public String updateClassroom(@ModelAttribute Classroom classroom) {
        Classroom existingClassroom = classroomRepository.findById(classroom.getId()).get();
        existingClassroom.setName(classroom.getName());
        existingClassroom.setStudents(classroom.getStudents());
        classroomRepository.save(existingClassroom);
        return "redirect:/teacher/classrooms";
    }

    @GetMapping("/{id}/delete")
    public String deleteClassroom(@PathVariable UUID id) {
        classroomRepository.deleteById(id);
        return "redirect:/teacher/classrooms";
    }

    @GetMapping("/students/{id}/classroom")
    public String getClassroomDetails(@PathVariable UUID id, Model model) {
        List<Student> students = studentRepository.findByClassroomId(id);
        model.addAttribute("students", students);
        return "teacher/classroom/students";
    }

    private MyUser getCurrentUser() {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();
        return myUserRepository.findByEmail(email)
                .orElseThrow(() -> new UserNotFoundException(email));
    }

    @GetMapping("/{id}/grades")
    public String viewClassroomGrades(
            @PathVariable UUID id,
            Model model) {

        // Получаем класс
        Classroom classroom = classroomRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Classroom not found"));

        // Получаем всех студентов и задания для класса
        List<Student> students = studentRepository.findByClassroomId(id);
        List<Homework> homeworks = homeworkRepository.findByClassroomId(id);
        List<Submission> submissions = submissionRepository.findByClassroomId(id);
        Map<Student, Map<Integer, Submission>> studentGrades = new HashMap<>();
        for (Student student : students) {
            studentGrades.put(student, new HashMap<>());
        }
        for (Submission submission : submissions) {
            Student student = submission.getStudent();
            if (studentGrades.containsKey(student)) {
                studentGrades.get(student).put(submission.getHomework().getNumber(), submission);
            }
        }
        model.addAttribute("classroom", classroom);
        model.addAttribute("students", students);
        model.addAttribute("studentGrades", studentGrades);
        model.addAttribute("homeworks", homeworks);

        return "teacher/classroom/journal";
    }
}
