<template>
  <div>
    <!-- Модальное окно -->
    <div class="modal fade" id="vacancyModal" tabindex="-1" aria-labelledby="vacancyModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="vacancyModalLabel">Отклик на вакансию</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="submitResponse">
            <div class="modal-body">
              <div class="mb-3">
                <label for="vacancyName" class="form-label">Ваше имя</label>
                <input
                  type="text"
                  class="form-control"
                  id="vacancyName"
                  v-model="responseData.full_name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="vacancyEmail" class="form-label">Ваш email</label>
                <input
                  type="email"
                  class="form-control"
                  id="vacancyEmail"
                  v-model="responseData.email"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="resumeSelect" class="form-label">Ваше резюме</label>
                <select
                  class="form-select"
                  id="resumeSelect"
                  v-model="responseData.resumeId"
                  required
                >
                  <option value="">Выберите резюме</option>
                  <option v-for="resume in resumes" :key="resume.id" :value="resume.id">
                    {{ resume.title }}
                  </option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="submit" class="btn btn-primary">Отправить</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";


export default {
  name: "ResponseModal",
  props: {
    vacancyId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      resumes: [], // Список резюме
      responseData: {
        full_name: "",
        email: "",
        resumeId: "",
      },
    };
  },
  methods: {
    async loadResumes() {
      try {
        const currentUser = JSON.parse(localStorage.getItem("currentUser"));
        if (!currentUser || !currentUser.id) {
          console.error("Пользователь не авторизован");
          return;
        }
        const response = await axios.get(
          `http://localhost:3000/resumes?userId=${currentUser.id}`
        );
        this.resumes = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке резюме:", error);
      }
    },
    async submitResponse() {
      try {
        const currentUser = JSON.parse(localStorage.getItem("currentUser"));
        if (!currentUser || !currentUser.id) {
          alert("Вы должны быть авторизованы, чтобы откликнуться на вакансию.");
          return;
        }

        const responsePayload = {
          ...this.responseData,
          userId: currentUser.id,
          vacancyId: this.vacancyId,
        };

        const response = await axios.post(
          "http://localhost:3000/responses",
          responsePayload
        );
        console.log("Отклик успешно отправлен:", response.data);

        // Очистить форму и закрыть модальное окно
        this.responseData = {
          full_name: "",
          email: "",
          resumeId: "",
        };
        const modalElement = document.getElementById("vacancyModal");
        const modalInstance = Modal.getInstance(modalElement);

        modalInstance.hide();
      } catch (error) {
        console.error("Ошибка при отправке отклика:", error);
        alert("Произошла ошибка при отправке отклика.");
      }
    },
  },
  mounted() {
    const modalElement = document.getElementById("vacancyModal");
    modalElement.addEventListener("show.bs.modal", this.loadResumes);
  },
};
</script>

<style scoped>
.modal-title {
  font-weight: bold;
}
</style>
