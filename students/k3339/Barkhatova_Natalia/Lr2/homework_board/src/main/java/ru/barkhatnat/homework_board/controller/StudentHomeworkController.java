package ru.barkhatnat.homework_board.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import ru.barkhatnat.homework_board.repository.HomeworkRepository;
import ru.barkhatnat.homework_board.repository.MyUserRepository;


@Controller
@RequestMapping("student/homeworks")
public class StudentHomeworkController extends HomeworkController {
    public StudentHomeworkController(HomeworkRepository homeworkRepository, MyUserRepository myUserRepository) {
        super(homeworkRepository, myUserRepository);
    }
}
