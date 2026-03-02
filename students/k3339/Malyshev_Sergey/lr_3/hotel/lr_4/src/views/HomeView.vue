<template>
  <v-container fluid class="pa-6">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <!-- Приветствие и статус авторизации -->
        <v-card class="mb-8 elevation-4">
          <v-card-title class="text-h4 primary--text">
            Добро пожаловать в систему управления гостиницей
          </v-card-title>

          <v-card-text>
            <div v-if="auth.isAuthenticated">
              <p class="text-subtitle-1 mb-4">
                Вы вошли как: <strong>{{ auth.user?.username || 'Пользователь' }}</strong>
              </p>

              <v-btn color="error" outlined @click="auth.logout">
                Выйти из системы
              </v-btn>
            </div>

            <div v-else>
              <v-alert type="warning" class="mb-4">
                Для доступа к функциям системы необходимо войти в аккаунт
              </v-alert>

              <v-btn color="primary" to="/login" class="mr-4">
                Войти
              </v-btn>

              <v-btn color="secondary" to="/register">
                Зарегистрироваться
              </v-btn>
            </div>
          </v-card-text>
        </v-card>

        <!-- Быстрый доступ (только для авторизованных) -->
        <v-card v-if="auth.isAuthenticated" class="elevation-4">
          <v-card-title class="text-h5">
            Быстрый доступ
          </v-card-title>

          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="4" lg="3">
                <v-card hover class="pa-4 text-center elevation-2">
                  <v-icon x-large color="primary" class="mb-4">mdi-bed-king</v-icon>
                  <v-btn block color="primary" to="/rooms" large>
                    Номера
                  </v-btn>
                  <div class="mt-2 caption">Просмотр и управление номерами</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="4" lg="3">
                <v-card hover class="pa-4 text-center elevation-2">
                  <v-icon x-large color="primary" class="mb-4">mdi-account-group</v-icon>
                  <v-btn block color="primary" to="/guests" large>
                    Гости
                  </v-btn>
                  <div class="mt-2 caption">Список гостей и поиск</div>
                </v-card>
              </v-col>


              <v-col cols="12" sm="6" md="4" lg="3">
                <v-card hover class="pa-4 text-center elevation-2">
                  <v-icon x-large color="primary" class="mb-4">mdi-calendar-check</v-icon>
                  <v-btn block color="primary" to="/bookings" large>
                    Бронирования
                  </v-btn>
                  <div class="mt-2 caption">Текущие и будущие брони</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="4" lg="3">
                <v-card hover class="pa-4 text-center elevation-2">
                  <v-icon x-large color="primary" class="mb-4">mdi-chart-bar</v-icon>
                  <v-btn block color="primary" to="/reports/quarter" large>
                    Отчёты
                  </v-btn>
                  <div class="mt-2 caption">Доходы и статистика</div>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Если не авторизован — показываем приглашение -->
        <v-card v-else class="mt-8 elevation-4">
          <v-card-title class="text-h5 primary--text">
            Начните работу с системой
          </v-card-title>
          <v-card-text class="text-subtitle-1">
            <p>
              После входа в систему вы получите доступ к управлению номерами, гостями, бронированиями, сотрудниками и отчётам.
            </p>
            <p class="mt-4">
              <strong>Функции доступны после авторизации:</strong>
            </p>
            <ul>
              <li>Просмотр свободных и занятых номеров</li>
              <li>Заселение и выселение гостей</li>
              <li>Контроль расписания уборки</li>
              <li>Генерация отчётов за квартал</li>
            </ul>
          </v-card-text>
          <v-card-actions class="justify-center pb-6">
            <v-btn x-large color="primary" to="/login">
              Войти в систему
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-icon {
  font-size: 48px !important;
}
</style>
