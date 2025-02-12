<template>
  <div>
    <Header />
    <h3 class="mb-4">Список учителей</h3>
    <button @click="showAddForm = true" class="btn btn-primary mb-4">Добавить учителя</button>

    <table class="table table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Класс</th>
          <th>Кабинет</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="teacher in teachers" :key="teacher.id">
          <td>{{ teacher.first_name }}</td>
          <td>{{ teacher.last_name }}</td>
          <td>{{ teacher.leaded_class ? teacher.leaded_class.name : "Нет" }}</td>
          <td>
            {{ teacher.cabinet ? teacher.cabinet.number : "Нет кабинета" }}
            <span v-if="teacher.cabinet?.is_profile">(Профильный)</span>
          </td>
          <td>
            <button @click="editTeacher(teacher)" class="btn btn-warning btn-sm">Редактировать</button>
            <button @click="deleteTeacher(teacher.id)" class="btn btn-danger btn-sm">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма добавления/редактирования -->
    <div v-if="showAddForm || selectedTeacher" class="form-modal">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>{{ selectedTeacher ? 'Редактировать учителя' : 'Добавить учителя' }}</h2>
          <form @submit.prevent="saveTeacher">
            <div class="mb-3">
              <label for="first_name" class="form-label">Имя:</label>
              <input v-model="formData.first_name" type="text" id="first_name" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="last_name" class="form-label">Фамилия:</label>
              <input v-model="formData.last_name" type="text" id="last_name" class="form-control" required />
            </div>

            <!-- Класс -->
            <div class="mb-3">
                <label for="class" class="form-label">Класс:</label>
                <input v-model="formData.leaded_class" type="text" id="class" class="form-control" placeholder="Введите класс" required />
            </div>

            <!-- Кабинет -->
            <div class="mb-3">
                <label for="cabinet" class="form-label">Кабинет:</label>
                <input v-model="formData.cabinet" type="text" id="cabinet" class="form-control" placeholder="Введите номер кабинета" required />
            </div>

            <div class="d-flex justify-content-between">
              <button type="submit" class="btn btn-primary">
                {{ selectedTeacher ? "Сохранить изменения" : "Добавить" }}
              </button>
              <button type="button" @click="cancelEdit" class="btn btn-secondary">Отмена</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import apiClient from "@/api/axios"; // Ваш API клиент

export default {
  data() {
    return {
      teachers: [], 
      classes: [],
      cabinets: [],
      showAddForm: false, // Флаг отображения формы добавления
      selectedTeacher: null, // Выбранный учитель для редактирования
      formData: {
        first_name: "",
        last_name: "",
        leaded_class: "", // Название выбранного класса
        cabinet: "", // Номер выбранного кабинета
      },
    };
  },
  async created() {
    this.loadTeachers();
    this.loadDropdownData();
  },
  methods: {
    async loadTeachers() {
      try {
        const response = await apiClient.get("/school/teachers/");
        this.teachers = response.data.Teachers;
      } catch (error) {
        console.error("Ошибка при загрузке учителей:", error);
        alert("Не удалось загрузить список учителей.");
      }
    },
    async loadDropdownData() {
        try {
            const [classesResponse, cabinetsResponse] = await Promise.all([
            apiClient.get("/school/classes/"),
            apiClient.get("/school/classrooms/"),
            ]);
            
            this.classes = classesResponse.data;
            this.cabinets = cabinetsResponse.data;
            
        } catch (error) {
            console.error("Ошибка при загрузке данных для списков:", error);
            alert("Не удалось загрузить данные для выпадающих списков.");
        }
    },

    async deleteTeacher(id) {
      try {
        if (confirm("Вы уверены, что хотите удалить этого учителя?")) {
          await apiClient.delete(`/school/delete_teacher/${id}/`);
          this.teachers = this.teachers.filter((teacher) => teacher.id !== id);
        }
      } catch (error) {
        console.error("Ошибка при удалении учителя:", error);
        alert("Не удалось удалить учителя.");
      }
    },
    editTeacher(teacher) {
      this.selectedTeacher = teacher;
      this.formData.first_name = teacher.first_name;
      this.formData.last_name = teacher.last_name;
      this.formData.leaded_class = teacher.leaded_class ? teacher.leaded_class.name : "";
      this.formData.cabinet = teacher.cabinet ? teacher.cabinet.number : "";
    },
    async saveTeacher() {
        try {
            console.log("Введенные данные:");
            console.log("Имя:", this.formData.first_name);
            console.log("Фамилия:", this.formData.last_name);
            console.log("Класс:", this.formData.leaded_class);
            console.log("Кабинет:", this.formData.cabinet);

            
            console.log("Список классов:", this.classes);
            console.log("Список кабинетов:", this.cabinets);

            
            const classObj = this.classes.find((cls) => cls.name === this.formData.leaded_class);
            console.log(classObj)
            const leadedClassId = classObj.id
            console.log(leadedClassId)
            const classroomObj = this.cabinets.find((clsroom) => clsroom.number === this.formData.cabinet);
            console.log(classroomObj)
            const ClassroomId = classroomObj.id
            console.log(ClassroomId)

            if (!leadedClassId) {
                alert("Класс не найден.");
                return;
            }

            const payload = {
                first_name: this.formData.first_name,
                last_name: this.formData.last_name,
                leaded_class: leadedClassId,
                cabinet: ClassroomId,
            };

            console.log("Payload для отправки:", payload);

            if (this.selectedTeacher) {
                await apiClient.put(`/school/update_teacher/${this.selectedTeacher.id}/`, payload);
            } else {
                await apiClient.post("/school/add_teacher/", payload);
            }

            this.loadTeachers();
            this.cancelEdit();
        } catch (error) {
            console.error("Ошибка при сохранении учителя:", error);
            alert("Не удалось сохранить изменения.");
        }
    },


    cancelEdit() {
      this.selectedTeacher = null;
      this.showAddForm = false;
      this.formData = {
        first_name: "",
        last_name: "",
        subject_ids: "",
        leaded_class: "",
        cabinet: "",
      };
    },
  },
};
</script>

<style scoped>
* {
  margin-left: 20px; 
  margin-right: 40px;
}

h3 {
  margin-top: 90px;
}

.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-overlay {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
}

.btn {
  border-radius: 8px;
  padding: 6px 12px;
}

.td {
  overflow: hidden;
}
</style>
