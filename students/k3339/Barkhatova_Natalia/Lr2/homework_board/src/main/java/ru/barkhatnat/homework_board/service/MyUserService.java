package ru.barkhatnat.homework_board.service;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.barkhatnat.homework_board.domain.MyUser;
import ru.barkhatnat.homework_board.domain.Student;
import ru.barkhatnat.homework_board.domain.Teacher;
import ru.barkhatnat.homework_board.exception.UserAlreadyExistsException;
import ru.barkhatnat.homework_board.repository.MyUserRepository;
import ru.barkhatnat.homework_board.repository.StudentRepository;
import ru.barkhatnat.homework_board.repository.TeacherRepository;

import java.util.Collections;

@Service
@RequiredArgsConstructor
public class MyUserService {
    private final MyUserRepository userRepository;
    private final StudentRepository studentRepository;
    private final TeacherRepository teacherRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public MyUser createUser(MyUser myUser) throws UserAlreadyExistsException {
        if (userRepository.findByEmail(myUser.getEmail()).isPresent()) {
            throw new UserAlreadyExistsException("User with email " + myUser.getEmail() + " already exists");
        }
        String encodedPassword = passwordEncoder.encode(myUser.getPassword());
        MyUser user;
        if (myUser.getRole() == MyUser.Role.STUDENT) {
            user = studentRepository.save(new Student(myUser.getEmail(),
                    encodedPassword, myUser.getRole(), myUser.getName(),
                    myUser.getLastName(), myUser.getMiddleName(),
                    Collections.emptyList(), Collections.emptyList(), Collections.emptyList()));
        } else {
            user = teacherRepository.save(new Teacher(myUser.getEmail(),
                    encodedPassword, myUser.getRole(), myUser.getName(),
                    myUser.getLastName(), myUser.getMiddleName(),
                    Collections.emptyList()));
        }
        return user;
    }
}
