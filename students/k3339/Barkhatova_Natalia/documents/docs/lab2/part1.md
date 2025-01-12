Мой вариант №2 - "Доска домашних заданий"
### Задание:
О домашнем задании должна храниться следующая информация: предмет,
преподаватель, дата выдачи, период выполнения, текст задания, информация о штрафах.
Необходимо реализовать следующий функционал:
- Регистрация новых пользователей.
- Просмотр домашних заданий по всем дисциплинам (сроки выполнения,
описание задания).
- Сдача домашних заданий в текстовом виде.
- Администратор (учитель) должен иметь возможность поставить оценку за
задание средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая оценки
всех учеников класса.
### Стек:
- **Язык:** Java 21.
- **Фреймворк:** Spring Boot
- **База данных:** PostgreSQL
- **Шаблонизатор:** Thymeleaf
- **Безопасность:** Spring Security
- **Дополнительно:** Lombok
- **Система сборки:** Maven.

### Ход работы:
Я реализовала такие сущности как Classroom, Homework, MyUser, Student, Teacher, Subject, Submission и Teacher и настроила связи между ними. Например:
```
@Entity  
@Getter  
@Setter  
public class Classroom {  
    @Id  
    @UuidGenerator    private UUID id;  
  
    @Column(nullable = false, unique = true, length = 10)  
    private String name;  
  
    @ManyToOne  
    @JoinColumn(name = "subject_id", nullable = false)  
    private Subject subject;  
  
    @ManyToOne  
    @JoinColumn(name = "teacher_id", nullable = false)  
    private Teacher teacher;  
  
    @OneToMany(mappedBy = "classroom")  
    private List<Homework> homeworks;  
  
    @ManyToMany  
    private List<Student> students;  
}
```
На основе этих сущностей была автоматически сгенерирована схема базы данных PostgreSQL.

Затем были созданы репозитории
```
@Repository  
public interface ClassroomRepository extends JpaRepository<Classroom, UUID> {  
    List<Classroom> findByTeacherEmail(String email);  
}
```
 И контроллеры 
```
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
  
        Classroom classroom = classroomRepository.findById(id)  
                .orElseThrow(() -> new IllegalArgumentException("Classroom not found"));  
  
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
```
HTML-templates разделены на 2 группы - teacher и student

Настроена форма аутентификации, пользователи будут вводить свои логин и пароль на специальной странице входа. После успешного входа они будут перенаправлены на страницу "/home". Доступ к определенным страницам ограничен ролями: пользователи с ролью "TEACHER" могут заходить на страницы, начинающиеся с "/teacher", а пользователи с ролью "STUDENT" — на страницы, начинающиеся с "/student". Все остальные страницы доступны только аутентифицированным пользователям. Пароли пользователей хранятся в базе в зашифрованном виде с помощью BCrypt. Также настроен выход из системы по URL "/logout", после чего пользователь снова попадет на страницу входа.
```
@Configuration  
@EnableWebSecurity  
public class SecurityConfig {  
  
    @Bean  
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {  
        http  
                .cors(AbstractHttpConfigurer::disable)  
                .csrf(AbstractHttpConfigurer::disable)  
                .securityMatcher("/**")  
                .authorizeHttpRequests(auth -> auth  
                        .requestMatchers("/login").permitAll()  
                        .requestMatchers("/registration").permitAll()  
                        .requestMatchers("/teacher/**").hasRole("TEACHER")  
                        .requestMatchers("/student/**").hasRole("STUDENT")  
                        .anyRequest().authenticated()  
                )  
                .formLogin(form -> form  
                        .loginPage("/login")  
                        .defaultSuccessUrl("/home", true)  
                        .permitAll()  
                )  
                .logout(logout -> logout  
                        .logoutUrl("/logout")  
                        .logoutSuccessUrl("/login")  
                        .permitAll()  
                );  
  
        return http.build();  
    }  
  
    @Bean  
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {  
        return authenticationConfiguration.getAuthenticationManager();  
    }  
  
    @Bean  
    public PasswordEncoder passwordEncoder() {  
        return new BCryptPasswordEncoder();  
    }  
}
```
Были написаны необходимые контроллеры и html templates с использованием bootstrap.