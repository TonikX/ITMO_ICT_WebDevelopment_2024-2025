<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-h5 text-center">🔑 Смена пароля</v-card-title>
          <v-card-text>
            <!-- Форма смены пароля -->
            <v-form @submit.prevent="changePassword">
              <v-text-field
                v-model="currentPassword"
                label="Текущий пароль"
                type="password"
                placeholder="Введите текущий пароль"
                required
              ></v-text-field>
              <v-text-field
                v-model="newPassword"
                label="Новый пароль"
                type="password"
                placeholder="Введите новый пароль"
                required
              ></v-text-field>
              <v-text-field
                v-model="reNewPassword"
                label="Подтверждение нового пароля"
                type="password"
                placeholder="Повторите новый пароль"
                required
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-3"
                :disabled="isLoading"
              >
                Сменить пароль
              </v-btn>
            </v-form>

            <!-- Сообщения об ошибке и успехе -->
            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
            >
              {{ error }}
            </v-alert>
            <v-alert
              v-if="success"
              type="success"
              class="mt-3"
            >
              {{ success }}
            </v-alert>
          </v-card-text>
        </v-card>

        <!-- Индикатор загрузки -->
        <v-row v-if="isLoading" justify="center" class="mt-3">
          <v-progress-circular
            indeterminate
            color="primary"
            size="50"
          ></v-progress-circular>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
