<template>
  <HeaderComponent />
  <v-container class="service-management-container">
    <v-card>
      <v-card-title class="title">Управление услугами</v-card-title>
      <v-card-text>
        <v-btn color="primary" class="add-service-btn" @click="openDialog">Добавить услугу</v-btn>

        <v-text-field
          v-model="search"
          class="search-field"
          label="Поиск услуг"
          append-icon="mdi-magnify"
          clearable
          outlined
        ></v-text-field>

        <v-data-table
          :headers="headers"
          :items="filteredServices"
          item-value="id"
          class="elevation-1"
        >
          <template v-slot:actions="{ item }">
            <v-btn icon @click="editService(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteService(item.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ dialogTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-text-field
              v-model="serviceForm.service_name"
              :rules="[rules.required]"
              label="Название услуги"
            ></v-text-field>
            <v-textarea
              v-model="serviceForm.service_description"
              :rules="[rules.required]"
              label="Описание"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDialog">Отмена</v-btn>
          <v-btn color="blue darken-1" text :disabled="!formValid" @click="saveService">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
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
      services: [],
      search: "",
      headers: [
        { text: "ID", value: "id" },
        { text: "Название", value: "service_name" },
        { text: "Описание", value: "service_description" },
        { text: "Действия", value: "actions", sortable: false },
      ],
      dialog: false,
      dialogTitle: "Добавить услугу",
      serviceForm: {
        id: null,
        service_name: "",
        service_description: "",
      },
      formValid: false,
      rules: {
        required: (value) => !!value || "Поле обязательно",
      },
    };
  },
  computed: {
    filteredServices() {
      return this.services.filter((service) =>
        service.service_name.toLowerCase().includes(this.search.toLowerCase())
      );
    },
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/services/");
        this.services = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке услуг:", error);
      }
    },
    openDialog() {
      this.dialogTitle = "Добавить услугу";
      this.serviceForm = {
        id: null,
        service_name: "",
        service_description: "",
      };
      this.dialog = true;
    },
    editService(service) {
      this.dialogTitle = "Редактировать услугу";
      this.serviceForm = { ...service };
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    async saveService() {
      if (this.serviceForm.id) {
        try {
          await axios.put(`http://127.0.0.1:8000/clinic/services/${this.serviceForm.id}/`, this.serviceForm);
          this.fetchServices();
          this.dialog = false;
        } catch (error) {
          console.error("Ошибка при обновлении услуги:", error);
        }
      } else {
        try {
          await axios.post("http://127.0.0.1:8000/clinic/services/", this.serviceForm);
          this.fetchServices();
          this.dialog = false;
        } catch (error) {
          console.error("Ошибка при создании услуги:", error);
        }
      }
    },
    async deleteService(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/clinic/services/${id}/`);
        this.fetchServices();
      } catch (error) {
        console.error("Ошибка при удалении услуги:", error);
      }
    },
  },
  created() {
    this.fetchServices();
  },
};
</script>

<style scoped>
.service-management-container {
  padding: 20px;
  text-align: center;
}

.title {
  text-align: center;
}

.add-service-btn {
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.search-field {
  width: 100%;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  display: block;
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

