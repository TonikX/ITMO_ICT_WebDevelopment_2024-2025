<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Дашборд учебной части</h1>
      </v-col>
    </v-row>
    
    <!-- Статистика -->
    <v-row>
      <v-col cols="12" md="3" v-for="stat in stats" :key="stat.title">
        <v-card class="text-center">
          <v-card-text>
            <v-icon size="48" :color="stat.color" class="mb-4">{{ stat.icon }}</v-icon>
            <h2 class="text-h2">{{ stat.value }}</h2>
            <p class="text-body-1">{{ stat.title }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Студенты и преподаватели -->
    <v-row class="mt-6">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Последние студенты</v-card-title>
          <v-card-text>
            <v-list v-if="recentStudents.length">
              <v-list-item v-for="student in recentStudents" :key="student.student_id">
                <template #prepend>
                  <v-avatar color="primary">
                    <span class="text-white">{{ student.first_name?.[0] || student.last_name?.[0] || '?' }}</span>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ student.full_name }}</v-list-item-title>
                <v-list-item-subtitle>{{ student.group_name || 'Группа не указана' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <p v-else class="text-center py-6">Нет данных</p>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Последние преподаватели</v-card-title>
          <v-card-text>
            <v-list v-if="recentTeachers.length">
              <v-list-item v-for="teacher in recentTeachers" :key="teacher.teacher_id">
                <template #prepend>
                  <v-avatar color="secondary">
                    <span class="text-white">{{ teacher.first_name?.[0] || teacher.last_name?.[0] || '?' }}</span>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ teacher.full_name }}</v-list-item-title>
                <v-list-item-subtitle>{{ teacher.position || 'Должность не указана' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <p v-else class="text-center py-6">Нет данных</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStudents } from '@/composables/useStudents'
import { useTeachers } from '@/composables/useTeachers'
import { useGroups } from '@/composables/useGroups'
import { useSubjects } from '@/composables/useSubjects'

const students = useStudents()
const teachers = useTeachers()
const groups = useGroups()
const subjects = useSubjects()

const stats = ref([
  { title: 'Студентов', value: 0, icon: 'mdi-account-group', color: 'primary' },
  { title: 'Преподавателей', value: 0, icon: 'mdi-account-tie', color: 'secondary' },
  { title: 'Групп', value: 0, icon: 'mdi-account-multiple', color: 'success' },
  { title: 'Дисциплин', value: 0, icon: 'mdi-book-open', color: 'warning' }
])

const recentStudents = computed(() => students.students.value.slice(0, 5))
const recentTeachers = computed(() => teachers.teachers.value.slice(0, 5))

onMounted(async () => {
  await Promise.all([
    students.fetchStudents(),
    teachers.fetchTeachers(),
    groups.fetchGroups(),
    subjects.fetchSubjects()
  ])
  
  stats.value = [
    { title: 'Студентов', value: students.students.value.length, icon: 'mdi-account-group', color: 'primary' },
    { title: 'Преподавателей', value: teachers.teachers.value.length, icon: 'mdi-account-tie', color: 'secondary' },
    { title: 'Групп', value: groups.groups.value.length, icon: 'mdi-account-multiple', color: 'success' },
    { title: 'Дисциплин', value: subjects.subjects.value.length, icon: 'mdi-book-open', color: 'warning' }
  ]
})
</script>