# Лабораторная работа 4

## Задание

### Лабораторная часть

Срок сдачи **25.12.2024**

Реализация клиентской части приложения средствами vue.js.

Порядок выполнения работы:<br>
1.	Выполнить практическую работу 4.1 Базовые конструкции языка JavaScript). (https://docs.google.com/document/d/1lurVq_ddbKQ-rORvxF3T9PlPPy-sOgHwFazCI0yEqYY/edit?usp=sharing)
2.	Выполнить практическую работу 4.2. Работа с Vue.JS. (https://docs.google.com/document/d/1kSXkW6Vcis8z-TunNALcapCVmMHps3jaDdIP4rZkV9E/edit?usp=sharing)
3.	Настроить для серверной части, реализованной в лабораторной работе №3 CORS (Cross-origin resource sharing) в соответствии [с Практической работой 4.3](https://docs.google.com/document/d/1diaE5abmxSYEpLCwAp-or9c_h11-wR8ZSGQl3_b0nsc/edit?usp=sharing)
4.	Утвердить с одним из преподавателей список интерфейсов для взаимодействия с серверной частью в соответствии с вашей предметной областью (**это очень важный пункт, тк бывает такое, что не все студенты понимают суть своих вариантов**).
5.	Реализовать интерфейсы авторизации, регистрации и изменения учётных данных и настроить взаимодействие с серверной частью.
Полезные материалы:<br>
    - Настройка авторизации средствами Vue.js и Django REST framework (DjangoSchool) ([ссылка](https://youtu.be/0VuOGByhiKU?list=PLF-NY6ldwAWqP9PqPU3LA7mX2KJVyLhC_))<br>
6.	Реализовать клиентские интерфейсы и настроить взаимодействие с серверной частью (интерфейсы из пункта 4).
Полезные материалы:<br>
    - Пункты 4.2, 4.3, 4.5 в [Практической работе 4.2](https://github.com/TonikX/ITMO_ICT_WebDevelopment_2020-2021)<br>
    - В освоении VUE 3 может помочь данный урок [урок](https://youtu.be/XzLuMtDelGk)
7.	Подключить vuetify или аналогичную библиотеку.
Полезные материалы:<br>
    - Пункт 3.1 в [Практической работе 4.2](https://github.com/TonikX/ITMO_ICT_WebDevelopment_2020-2021)<br>
8.	Реализовать документацию, описывающую работу разработанных интерфейсов средствами MkDocs.

## Вариант

Создать программную систему, предназначенную для завуча школы. Она должна обеспечивать хранение сведений о каждом учителе, классном руководстве, о предметах, которые он преподает в заданный период, номере закрепленного за ним кабинета, о расписании занятий. Существуют учителя, которые не имеют собственного кабинета. Об учениках должны храниться следующие сведения: фамилия и имя, в каком классе учится, какую оценку имеет в текущей четверти по каждому предмету.

Завуч должен иметь возможность добавить сведения о новом учителе или ученике, внести в базу данных четвертные оценки учеников каждого класса по каждому предмету, удалить данные об уволившемся учителе и отчисленном из школы ученике, внести изменения в данные об учителях и учениках, в том числе поменять оценку ученика по тому или иному предмету. В задачу завуча входит также составление расписания.

Завучу могут потребоваться следующие сведения:

- Какой предмет будет в заданном классе, в заданный день недели на заданном уроке?
- Сколько учителей преподает каждую из дисциплин в школе?
- Список учителей, преподающих те же предметы, что и учитель, ведущий информатику в заданном классе.
- Сколько мальчиков и девочек в каждом классе?
- Сколько кабинетов в школе для базовых и профильных дисциплин?

Необходимо предусмотреть возможность получения документа, представляющего собой отчет об успеваемости заданного класса. Отчет включает сведения об успеваемости за четверть по каждому предмету. Необходимо подсчитать средний балл по каждому предмету, по классу в целом, указать общее количество учеников в классе. Для класса указать классного руководителя.

## Code

### Django

```
pip install django-cors-headers
```

settings.py
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'school',
    'django_extensions',
    'corsheaders',
]

# CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:5173',
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

### Vue

index.html
```html
<!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>School</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

main.js
```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(router).mount('#app')

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.auth) {
      next({ name: 'Login' })
    } else {
      next()
    }
  } else {
    next()
  }
})
```

App.vue
```vue
<script setup>
import AppHeader from '@/components/AppHeader.vue'
</script>

<template>
  <div class="app">
    <AppHeader/>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token){
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    }
    else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  }
}
</script>

<style>
input {
  width: 300px !important;
}
select {
  width: 320px !important;
}
</style>

<style scoped>

</style>
```

AppHeader.vue
```vue
<template>
  <header>
    <nav>
      <router-link to="/" style="font-size: 30px;"><b>School</b></router-link>
      <router-link to="/students">Students</router-link>
      <router-link to="/teachers">Teachers</router-link>
      <router-link to="/grades">Grades</router-link>
      <router-link to="/schedule">Schedule</router-link>
      <router-link to="/subjects">Subjects</router-link>
      <router-link to="/marks">Marks</router-link>
      <router-link to="/log-in" v-if="!$store.getters.auth">Log In</router-link>
      <router-link to="/sign-up" v-if="!$store.getters.auth">Sign Up</router-link>
      <a href="javascript:void(0)" @click="logout" v-if="$store.getters.auth">Logout</a>
    </nav>
    <hr>
  </header>
</template>

<script>
import axios from 'axios'

export default {
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$store.commit('removeToken')
      axios.defaults.headers.common['Authorization'] = ''
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  color: white;
}
</style>
```

Students.vue
```vue
<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Students</h2>
  <table>
    <thead>
      <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Gender</th>
        <th>Grade</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="student in students" :key="student.id">
        <td>{{ student.first_name }}</td>
        <td>{{ student.last_name }}</td>
        <td>{{ {'M': 'Male', 'F': 'Female'}[student.gender] }}</td>
        <td>{{ `${grades.find(i => i.id == student.grade)['number']}${grades.find(i => i.id == student.grade)['letter']}` }}</td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.student = Object.assign({}, student); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteStudent(student.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchStudents">Update list of students</button>
  <button @click="Object.keys(student).forEach(i => student[i] = ''); update = 0; showDialog()">Create student</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update student</h2>
    <h2 v-else>Create student</h2>
    <form @submit.prevent>
      <label>First Name</label>
      <input
        v-model="student.first_name"
        type="text"
      >
      <label>Last Name</label>
      <input
        v-model="student.last_name"
        type="text"
      >
      <label>Gender</label>
      <select v-model="student.gender">
        <option value="M">Male</option>
        <option value="F">Female</option>
      </select>
      <label>Grade</label>
      <select v-model="student.grade">
        <option v-for="grade in grades" :value="grade.id" :key="grade.id">{{ `${grade.number}${grade.letter}` }}</option>
      </select>
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateStudent(); closeDialog()">Update</button>
        <button v-else @click="createStudent(); closeDialog()">Create</button>
        <button @click="closeDialog">Cancel</button>
      </div>
    </form>
  </dialog>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      students: [],
      student: {},
      grades: [],
      update: 0
    }
  },
  methods: {
    async fetchStudents() {
      const response = await axios.get('/api/student/')
      this.students = response.data
    },
    async fetchGrades() {
      const response = await axios.get('/api/grade/')
      this.grades = response.data
    },
    async createStudent() {
      await axios.post('/api/student/', {
        marks: this.student.marks || [],
        first_name: this.student.first_name,
        last_name: this.student.last_name,
        gender: this.student.gender,
        grade: this.student.grade,
      })
      this.fetchStudents()
    },
    async deleteStudent(studentId){
      await axios.delete(`/api/student/${studentId}/`)
      this.fetchStudents()
    },
    async updateStudent(){
      console.log(this.student.id, this.student.name)
      await axios.put(`/api/student/${this.student.id}/`, { 
        id: this.student.id,
        marks: this.student.marks || [],
        first_name: this.student.first_name,
        last_name: this.student.last_name,
        gender: this.student.gender,
        grade: this.student.grade,
      })
      this.fetchStudents()
    }
  },
  mounted() {
    this.fetchStudents()
    this.fetchGrades()
  }
}
</script>

<style scoped>

</style>
```

Другие аналогично:

- `Teachers.vue`
- `Grades.vue`
- `Schedule.vue`
- `Subjects.vue`
- `Marks.vue`

Для `Main.vue` сгенерировал описание выдуманной школы с помощью ChatGPT.

Report.vue
```vue
<template>
  <h2>Report {{ grade }}</h2>
  <h3>Total students: {{ report.total_students }}</h3>
  <h3>Teacher: {{ report.teacher }}</h3>
  <h3>Average marks:</h3>
  <p v-for="(value, name) in report.average_marks" :key="name">{{ name }}: {{ value }}</p>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      report: {},
      grade: '',
    }
  },
  methods: {
    async fetchReport() {
      const response = await axios.get(`/api/grade/${this.$route.params.id}/report/`)
      this.report = response.data
    },
    async fetchGrades() {
      const response = await axios.get('/api/grade/')
      this.grade = response.data.find(i => i.id == this.$route.params.id)['number'] + response.data.find(i => i.id == this.$route.params.id)['letter']
    }
  },
  mounted() {
    this.fetchReport()
    this.fetchGrades()
  }
}
</script>

<style scoped>

</style>
```

router/router.js
```javascript
import {createRouter, createWebHistory} from 'vue-router'
import Main from '@/views/Main.vue'
import Students from '@/views/Students.vue'
import Teachers from '@/views/Teachers.vue'
import Grades from '@/views/Grades.vue'
import Schedule from '@/views/Schedule.vue'
import Subjects from '@/views/Subjects.vue'
import Marks from '@/views/Marks.vue'
import Report from '@/views/Report.vue'
import LogIn from '@/views/LogIn.vue'
import SignUp from '@/views/SignUp.vue'

const routes = [
  {
    path: '/',
    component: Main
  },
  {
    path: '/students',
    component: Students,
    meta: { requiresAuth: true }
  },
  {
    path: '/teachers',
    component: Teachers,
    meta: { requiresAuth: true }
  },
  {
    path: '/grades',
    component: Grades,
    meta: { requiresAuth: true }
  },
  {
    path: '/schedule',
    component: Schedule,
    meta: { requiresAuth: true }
  },
  {
    path: '/subjects',
    component: Subjects,
    meta: { requiresAuth: true }
  },
  {
    path: '/marks',
    component: Marks,
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id',
    component: Report,
    meta: { requiresAuth: true }
  },
  {
    path: '/log-in',
    component: LogIn,
    name: 'Login'
  },
  {
    path: '/sign-up',
    component: SignUp
  }
]

const router = createRouter({routes, history: createWebHistory()})

export default router
```

#### Авторизация

LogIn.vue
```vue
<template>
  <h2>Log In</h2>
  <form @submit.prevent="submitForm">
    <label>Username</label>
    <input
      v-model="username"
      type="text"
    >
    <label>Password</label>
    <input
      v-model="password"
      type="password"
    >
    <button>Log In</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    async submitForm() {
      const response = await axios.post('/api/auth/token/login/', {
        username: this.username,
        password: this.password,
      })
      const token = response.data.auth_token
      this.$store.commit('setToken', token)
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
      localStorage.setItem('token', token)
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>

</style>
```

SignUp.vue
```vue
<template>
  <h2>Sign Up</h2>
  <form @submit.prevent="submitForm">
    <label>Username</label>
    <input
      v-model="username"
      type="text"
    >
    <label>Email</label>
    <input
      v-model="email"
      type="text"
    >
    <label>Password</label>
    <input
      v-model="password"
      type="password"
    >
    <button>Sign Up</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
    }
  },
  methods: {
    async submitForm() {
      await axios.post('/api/auth/users/', {
        username: this.username,
        email: this.email,
        password: this.password,
      })
      this.$router.push('/log-in')
    }
  }
}
</script>

<style scoped>

</style>
```

store/index.js
```javascript
import { createStore } from 'vuex'

export default createStore({
  state: {
    token: ''
  },
  getters: {
    auth(state){
      return Boolean(state.token)
    }
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')){
        state.token = localStorage.getItem('token')
      }
      else {
        state.token = ''
      }
    },
    setToken(state, token) {
      state.token = token
    },
    removeToken(state) {
      state.token = ''
    }
  },
  actions: {

  },
  modules: {

  },
})
```