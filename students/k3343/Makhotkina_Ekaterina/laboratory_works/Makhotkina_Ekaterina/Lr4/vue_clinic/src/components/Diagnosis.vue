<template>
  <div class="page-layout">
    <HeaderComponent />

    <main class="content">
      <div class="diagnosis-list-container">
        <h1 class="title">Список диагнозов</h1>

        <v-btn
          color="primary"
          class="add-diagnosis-btn"
          @click="openCreateModal"
        >
          Добавить диагноз
        </v-btn>

        <div v-if="diagnoses.length" class="diagnosis-cards">
          <div v-for="diagnosis in diagnoses" :key="diagnosis.id" class="diagnosis-card">
            <h2>{{ diagnosis.diagnosis }}</h2>
            <p>Тип диагноза: {{ diagnosis.diagnosis_kind }}</p>

            <div class="action-buttons">
              <v-btn
                color="yellow"
                @click="openEditModal(diagnosis)"
                class="action-btn"
              >
                Ред.
              </v-btn>
              <v-btn
                color="red"
                @click="deleteDiagnosis(diagnosis.id)"
                class="action-btn"
              >
                Удалить
              </v-btn>
            </div>
          </div>
        </div>

        <p v-else class="no-data">Нет данных о диагнозах</p>

        <v-dialog v-model="dialog" max-width="500">
          <v-card>
            <v-card-title>
              <span class="headline">{{ isEditing ? 'Редактировать' : 'Добавить' }} диагноз</span>
            </v-card-title>
            <v-card-text>
              <v-form ref="form">
                <v-text-field
                  v-model="formData.diagnosis"
                  label="Диагноз"
                  required
                ></v-text-field>

                <v-select
                  v-model="formData.diagnosis_kind"
                  :items="diagnosisKinds"
                  label="Тип диагноза"
                  item-value="id"
                  item-title="text"
                  required
                ></v-select>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="blue darken-1"
                text
                @click="saveDiagnosis"
              >
                Сохранить
              </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="closeDialog"
              >
                Отмена
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
    </main>
  </div>
</template>



<script>
import HeaderComponent from "@/components/Visual/Header.vue";
import axios from 'axios';

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      diagnoses: [],
      diagnosisKinds: [
        { id: 'circulatory diseases', text: 'Болезни системы кровообращения' },
        { id: 'respiratory diseases', text: 'Болезни органов дыхания' },
        { id: 'digestive diseases', text: 'Болезни органов пищеварения' },
        { id: 'musculoskeletal diseases', text: 'Заболевания опорно-двигательного аппарата' },
        { id: 'urinary diseases', text: 'Болезни мочевыводящих путей' },
        { id: 'blood diseases', text: 'Заболевания крови' },
        { id: 'endocrine diseases', text: 'Заболевания эндокринной системы' },
      ],
      dialog: false,
      isEditing: false,
      formData: {
        id: null,
        diagnosis: '',
        diagnosis_kind: '',
      },
    };
  },
  async created() {
    await this.fetchDiagnoses();
  },
  methods: {
    async fetchDiagnoses() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/clinic/diagnosis/');
        this.diagnoses = response.data;
      } catch (error) {
        console.error('Ошибка при получении данных диагнозов:', error);
      }
    },
    openCreateModal() {
      this.isEditing = false;
      this.formData = {
        id: null,
        diagnosis: '',
        diagnosis_kind: '',
      };
      this.dialog = true;
    },
    openEditModal(diagnosis) {
      this.isEditing = true;
      this.formData = {
        id: diagnosis.id,
        diagnosis: diagnosis.diagnosis,
        diagnosis_kind: diagnosis.diagnosis_kind,
      };
      this.dialog = true;
    },
    async saveDiagnosis() {
      try {
        if (!this.formData.diagnosis || !this.formData.diagnosis_kind) {
          console.error('Ошибка: Пожалуйста, заполните все обязательные поля.');
          return;
        }

        const payload = {
          diagnosis: this.formData.diagnosis,
          diagnosis_kind: this.formData.diagnosis_kind,
        };

        if (this.isEditing) {
          const response = await axios.put(
            `http://127.0.0.1:8000/clinic/diagnosis/${this.formData.id}/`,
            payload
          );
          console.log('Диагноз успешно обновлен', response);
        } else {
          const response = await axios.post(
            'http://127.0.0.1:8000/clinic/diagnosis/',
            payload
          );
          console.log('Диагноз успешно создан', response);
        }

        this.dialog = false;
        await this.fetchDiagnoses();
      } catch (error) {
        console.error('Ошибка при сохранении данных диагноза:', error);

        if (error.response) {
          console.error('Ошибка от сервера:', error.response.data);
        } else {
          console.error('Не удалось отправить запрос:', error.message);
        }
      }
    },
    async deleteDiagnosis(diagnosisId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/clinic/diagnosis/${diagnosisId}/`);
        await this.fetchDiagnoses();
      } catch (error) {
        console.error('Ошибка при удалении диагноза:', error);
      }
    },
    closeDialog() {
      this.dialog = false;
    },
  },
};
</script>

<style scoped>
div {
  width:100%;
}


.diagnosis-list-container {
  padding: 20px;
  text-align: center;
}

.title {
  text-align: center;
}

.add-diagnosis-btn {
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.diagnosis-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  justify-items: center;
}

.diagnosis-card {
  border: 1px solid #ccc;
  padding: 30px;
  width: 300px;
  box-sizing: border-box;
  text-align: left;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
}

.action-btn {
  width: 90px;
  margin-top: 10px;
  font-size: 12px;
}

.no-data {
  text-align: center;
  font-size: 18px;
}

v-btn {
  margin-top: 10px;
}
</style>

