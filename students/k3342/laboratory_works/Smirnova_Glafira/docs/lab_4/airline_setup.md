# Реализация фронтэнда на Vue

###  Настройка CORS в Django REST framework

Установка django-cors-headers:

    pip install django-cors-headers


Обновление settings.py файла проекта:  

    INSTALLED_APPS = (
        ##...
        'corsheaders'
    )


Добавление corsheaders.middleware.CorsMiddleware в “MIDDLEWARE_CLASSES” в settings.py:

    MIDDLEWARE_CLASSES = (
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.BrokenLinkEmailsMiddleware',
        'django.middleware.common.CommonMiddleware',
        #...
    )


Подключение CORS для всех доменов: 

    CORS_ORIGIN_ALLOW_ALL = True

HTTP-запросы на сервер будут отправляться с помощью библиотеки axios. К каждому запросу будет автоматически прикреплен токен юзера.

```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/', 
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
```

### Маршрутизация

```js
import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '@/views/Welcome.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import Planes from '@/views/Planes.vue';
import Flights from '@/views/Flights.vue';
import FlightDetail from "@/views/FlightDetail.vue";
import Crews from '@/views/Crews.vue';
import Maintenances from '@/views/Maintenances.vue';
import Routes from '@/views/Routes.vue';
import Employees from '@/views/Employees.vue';
import RouteStats from "@/views/RouteStats.vue";
import PlaneStats from "@/components/PlaneStats.vue";
import Profile from '@/views/Profile.vue';
import ChangePassword from '@/components/ChangePassword.vue';
import UpdateProfile from '@/components/UpdateProfile.vue';
import sn from "@/views/sn.vue"



const routes = [
  { path: '/', name: 'Welcome', component: Welcome },
  { path: '/register', name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login },
  { path: '/planes', name: 'Planes', component: Planes },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/change-password', name: 'ChangePassword', component: ChangePassword },
  { path: '/update-profile', name: 'UpdateProfile', component: UpdateProfile },
  { path: '/flights', name: 'Flights', component: Flights },
  { path: `/flights/:flightId`, name: 'FlightDetail', component: FlightDetail, props: true },
  { path: '/routes-stats', name: 'RouteStats', component: RouteStats },
  { path: '/planes-stats', name: 'PlaneStats', component: PlaneStats },
  { path: '/maintenances', name: 'Maintenances', component: Maintenances},
  { path: '/employees', name: 'Employees', component: Employees},
  { path: '/crews', name: 'Crews', component: Crews},
  { path: '/routes', name: 'Routes', component: Routes},
  { path: '/sn', name: 'sn', component: sn}

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```

### Реализация интерфейсов .vue

Рассмотрим реализацию интерфейсов на примере страницы "Ремонты". 

Под тэгом ```<template>``` указан шаблон
элементов страницы - фильтров, списков, пагинации, модальных окон, кнопок и текста.

Под тэгом `<script>` приведены функции и методы, которые необходимо вызвать в различных кейсах (при загрузке страницы, при нажатии на определенную кнопку и т.д.)

Под тэгом `<style>` перечислены стили элементов, применимые для всего поекта или только в рамках данного компонента (`scoped`)

`Maintenances.vue` - список всех ремонтов, фильтрация, поиск, создание нового ремонта, кнопки удаления и редактирования
```vue
<template>
  <v-container>
    <Snackbar ref="snackbar" />

    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Ремонты самолетов</h1>
      </v-col>
    </v-row>

    <!-- Фильтры -->
    <v-row>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.plane"
          :items="choices.planes"
          label="Фильтр по самолету"
          item-value="name"
          item-title="name"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.status"
          :items="choices.statuses"
          label="Фильтр по статусу"
          item-value="value"
          item-title="label"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="filters.date"
          label="Фильтр по дате начала"
          type="date"
          clearable
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- Кнопка добавления -->
    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="openCreateDialog">Добавить ремонт</v-btn>
      </v-col>
    </v-row>

    <!-- Диалог редактирования -->
    <EditMaintenanceDialog
      v-if="selectedMaintenance"
      ref="editMaintenanceDialog"
      :dialog="editDialog"
      @update:dialog="editDialog = $event"
      :initial-maintenance="selectedMaintenance"
      :choices="choices"
      @maintenance-updated="updateMaintenance"
    />

    <!-- Диалог создания -->
    <CreateMaintenanceDialog
      ref="createMaintenanceDialog"
      :dialog="createDialog"
      :choices="choices"
      @update:dialog="createDialog = $event"
      @maintenance-created="addMaintenance"
    />

    <!-- Список ремонтов -->
    <v-row>
      <v-col
        cols="12"
        md="6"
        v-for="maintenance in filteredAndPaginatedMaintenances"
        :key="maintenance.id"
      >
        <v-card class="compact-card mb-6" elevation="2">
          <v-card-title>
            Самолет: {{ maintenance.plane }}
          </v-card-title>
          <v-card-text>
            <p><strong>Дата начала:</strong> {{ formatDate(maintenance.start_date) }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Дата завершения:</strong> {{ maintenance.end_date ? formatDate(maintenance.end_date) : 'Не завершено' }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Описание:</strong> {{ maintenance.description }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Статус:</strong> {{ maintenance.status }}</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="warning" @click="openEditDialog(maintenance)">Редактировать</v-btn>
            <v-btn color="error" @click="openDeleteDialog(maintenance)">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

     <!-- Диалог удаления -->
    <DeleteMaintenanceDialog
      v-if="selectedMaintenance"
      :dialog="deleteDialog"
      :maintenance="selectedMaintenance"
      @update:dialog="deleteDialog = $event"
      @maintenance-deleted="handleMaintenanceDeleted"
    />

    <!-- Пагинация -->
    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="5"
        ></v-pagination>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import apiClient from "@/services/api";
import CreateMaintenanceDialog from "@/components/CreateMaintenanceDialog.vue";
import Snackbar from "@/components/Snackbar.vue";
import EditMaintenanceDialog from "@/components/EditMaintenanceDialog.vue";
import DeleteMaintenanceDialog from "@/components/DeleteMaintenanceDialog.vue";

export default {
  components: {DeleteMaintenanceDialog, EditMaintenanceDialog, Snackbar, CreateMaintenanceDialog},
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 4,
      maintenances: [],
      filters: {
        plane: null,
        status: null,
        date: null,
      },
      choices: {
        planes: [],
        statuses: [],
      },
      createDialog: false,
      editDialog: false,
      deleteDialog: false,

      selectedMaintenance: null,
    };
  },
  computed: {
    filteredMaintenances() {
      let filtered = this.maintenances;
      console.log("фильтры", this.filters)
      if (this.filters.plane) {
        filtered = filtered.filter(m => m.plane === this.filters.plane);
      }
      if (this.filters.status) {
        filtered = filtered.filter(m => m.status === this.filters.status);
      }
      if (this.filters.date) {
        filtered = filtered.filter(m => m.start_date.startsWith(this.filters.date));
      }
      console.log("подходит", filtered)

      return filtered;
    },
    filteredAndPaginatedMaintenances() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredMaintenances.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredMaintenances.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchMaintenances() {
      try {
        const response = await apiClient.get("/maintenances/");
        console.log(response.data)
        this.maintenances = response.data;
      } catch (error) {
        console.error("Ошибка загрузки ремонтов:", error.response?.data || error.message);
        alert("Ошибка загрузки ремонтов");
      }
    },
    async fetchChoices() {
      try {
        const response = await apiClient.get("/maintenances/choices/");
        this.choices = response.data;
      } catch (error) {
        console.error("Ошибка загрузки фильтров:", error.response?.data || error.message);
        alert("Ошибка загрузки фильтров");
      }
    },
    async addMaintenance(newMaintenance) {
      try {
        await apiClient.post("/maintenances/", newMaintenance);
        alert("Ремонт успешно добавлен!");
        await this.fetchMaintenances();
        this.$refs.createMaintenanceDialog.closeDialog();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.$refs.createMaintenanceDialog.setErrors(error.response.data);
        } else {
          console.error("Ошибка создания ремонта:", error.response?.data || error.message);
          alert("Ошибка создания ремонта.");
        }
      }
    },
    openCreateDialog() {
      this.createDialog = true;
    },
     openEditDialog(maintenance) {
      this.selectedMaintenance = maintenance
      console.log(this.selectedMaintenance)
      this.editDialog = true;
    },
    openDeleteDialog(maintenance) {
      this.selectedMaintenance = maintenance;
      this.deleteDialog = true;
    },
    async updateMaintenance(updatedMaintenance) {
      try {
        await apiClient.put(`/maintenances/${updatedMaintenance.id}/`, updatedMaintenance);
        this.$refs.snackbar.showSnackbar("Ремонт успешно обновлен!", "green");
        this.$refs.editMaintenanceDialog.closeDialog();
        this.editDialog = false;
        await this.fetchMaintenances();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.$refs.editMaintenanceDialog.setErrors(error.response.data);
        } else {
          console.error("Ошибка обновления ремонта:", error.response?.data || error.message);
          this.$refs.snackbar.showSnackbar("Ошибка обновления ремонта", "red");
        }
      }
    },
    async handleMaintenanceDeleted(maintenanceId) {
      try {
        await apiClient.delete(`/maintenances/${maintenanceId}/`);
        this.maintenances = this.maintenances.filter(m => m.id !== maintenanceId);
        this.$refs.snackbar.showSnackbar("Ремонт успешно удалён!");
      } catch (error) {
        console.error("Ошибка удаления ремонта:", error.response?.data || error.message);
        this.$refs.snackbar.showSnackbar("Ошибка удаления ремонта", "red");
      }
    },
     formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0'); 
      const year = date.getFullYear();
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');

      return `${day}.${month}.${year} ${hours}:${minutes}`;
    },
  },
  async created() {
    await Promise.all([this.fetchMaintenances(), this.fetchChoices()]);
  },
};
</script>
```

`CreateMaintenanceDialog.vue` - модальное окно создания ремонта

```vue
<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Добавление нового ремонта</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-select
            v-model="newMaintenance.plane"
            :items="choices.planes"
            label="Самолет"
            item-value="id"
            item-title="name"
            :error-messages="errors.plane || []"
            @update:model-value="clearFieldError('plane')"
            required
          />
          <v-text-field
            v-model="newMaintenance.start_date"
            label="Дата начала"
            type="datetime-local"
            :error-messages="errors.start_date || []"
            @input="clearFieldError('start_date')"
            required
          />
          <v-text-field
            v-model="newMaintenance.end_date"
            label="Дата завершения"
            type="datetime-local"
            :error-messages="errors.end_date || []"
            @input="clearFieldError('end_date')"
          />
          <v-select
            v-model="newMaintenance.status"
            :items="choices.statuses"
            label="Статус"
            item-value="value"
            item-title="label"
            :error-messages="errors.status || []"
            @update:model-value="clearFieldError('status')"
            required
          />
          <v-textarea
            v-model="newMaintenance.description"
            label="Описание"
            :error-messages="errors.description || []"
            @input="clearFieldError('description')"
            required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="createMaintenance">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: { type: Boolean, required: true },
    choices: { type: Object, required: true },
  },
  emits: ["update:dialog", "maintenance-created"],
  data() {
    return {
      newMaintenance: {
        plane: null,
        start_date: "",
        end_date: "",
        status: null,
        description: "",
      },
      errors: {},
    };
  },
  methods: {
    setErrors(serverErrors) {
      this.errors = serverErrors; // Устанавливаем ошибки с сервера
    },
    emitDialogUpdate(value) {
      this.$emit("update:dialog", value);
    },
    closeDialog() {
      this.$emit("update:dialog", false);
      this.resetForm();
    },
    resetForm() {
      this.newMaintenance = {
        plane: null,
        start_date: "",
        end_date: "",
        status: null,
        description: "",
      };
      this.errors = {};
    },
    clearFieldError(fieldName) {
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
    },
    async createMaintenance() {
      if (
        !this.newMaintenance.plane ||
        !this.newMaintenance.start_date ||
        !this.newMaintenance.status ||
        !this.newMaintenance.description
      ) {
        alert("Заполните все обязательные поля!");
        return;
      }
      try {
        await this.$emit("maintenance-created", { ...this.newMaintenance });
      } catch (error) {
        if (error.response && error.response.data) {
          this.errors = error.response.data;
        }
      }
    },
  },
};
</script>
```
`DeleteMaintenanceDialog.vue` - модальное окно удаления ремонта

```vue
<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="400"
  >
    <v-card>
      <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить ремонт для самолёта "{{ maintenance.plane }}"?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
        <v-btn color="red" @click="confirmDelete">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: {
      type: Boolean,
      required: true,
    },
    maintenance: {
      type: Object,
      required: true,
    },
  },
  emits: ['update:dialog', 'maintenance-deleted'],
  methods: {
    emitDialogUpdate(value) {
      this.$emit('update:dialog', value);
    },
    closeDialog() {
      this.$emit('update:dialog', false); 
    },
    confirmDelete() {
      this.$emit('maintenance-deleted', this.maintenance.id);
      this.closeDialog();
    },
  },
};
</script>


```

`EditMaintenanceDialog.vue` - модальное окно редактирования ремонта
```vue
<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Редактирование ремонта</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-textarea
            v-model="maintenance.description"
            label="Описание ремонта"
            :error-messages="errors.description || []"
            @input="clearFieldError('description')"
            required
          />
          <v-text-field
            v-model="maintenance.start_date"
            label="Дата начала"
            type="datetime-local"
            :error-messages="errors.start_date || []"
            @input="clearFieldError('start_date')"
            required
          />
          <v-text-field
            v-model="maintenance.end_date"
            label="Дата завершения"
            type="datetime-local"
            :error-messages="errors.end_date || []"
            @input="clearFieldError('end_date')"
          />
          <v-select
            v-model="maintenance.status"
            :items="choices.statuses"
            label="Статус"
            item-value="value"
            item-title="label"
            :error-messages="errors.status || []"
            @update:model-value="clearFieldError('status')"
            required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="updateMaintenance">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: { type: Boolean, required: true },
    choices: { type: Object, required: true },
    initialMaintenance: { type: Object, required: true },
  },
  emits: ["update:dialog", "maintenance-updated"],
  data() {
    return {
      maintenance: { ...this.initialMaintenance,
      start_date: this.formatDateTime(this.initialMaintenance.start_date),
      end_date: this.formatDateTime(this.initialMaintenance.end_date),}, 
      errors: {},
    };
  },
  watch: {
    dialog(val) {
      if (val) {
        this.initializeMaintenance();
      }
    },
  },
  methods: {
    setErrors(serverErrors) {
      this.errors = serverErrors; 
    },
    emitDialogUpdate(value) {
      this.$emit("update:dialog", value);
    },
    closeDialog() {
      this.$emit("update:dialog", false);
      this.maintenance = { ...this.initialMaintenance };
      this.errors = {};
      console.log()
    },
    clearFieldError(fieldName) {
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
    },
    initializeMaintenance() {
      this.maintenance = {
        ...this.initialMaintenance,
        start_date: this.formatDateTime(this.initialMaintenance.start_date),
        end_date: this.formatDateTime(this.initialMaintenance.end_date),
      };
    },
    async updateMaintenance() {
      try {
        const updatedMaintenance = {
          ...this.maintenance,
          start_date: this.unformatDateTime(this.maintenance.start_date),
          end_date: this.unformatDateTime(this.maintenance.end_date),
        };
        delete updatedMaintenance.plane; 

        this.maintenance.id = this.initialMaintenance.id

        await this.$emit("maintenance-updated", updatedMaintenance);
      } catch (error) {
        console.error("Ошибка обновления ремонта:", error.response?.data || error.message);
        if (error.response && error.response.data) {
          this.errors = error.response.data; 
        }
      }
    },
    formatDateTime(datetime) {
    if (!datetime) return ""; 
    const date = new Date(datetime);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  },
    unformatDateTime(formattedDateTime) {
    return new Date(formattedDateTime).toISOString();
  },
  },
};
</script>

```