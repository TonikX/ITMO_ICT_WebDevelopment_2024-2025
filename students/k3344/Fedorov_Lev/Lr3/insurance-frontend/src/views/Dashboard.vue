<template>
  <div>
    <component :is="dashboardComponent" />
  </div>
</template>

<script>
import AgentDashboard from '@/views/AgentDashboard.vue';
import DirectorDashboard from '@/views/DirectorDashboard.vue';
import EmployeeDashboard from '@/views/EmployeeDashboard.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import UserService from '@/services/UserService';

export default {
  name: 'UserDashboard',
  data() {
    return {
      role: '',
      isStaff: false,
      dashboardComponent: null,
      userData: {},
    };
  },
  async created() {
    try {
      const user = await UserService.getProfile();
      this.role = user.role;
      this.isStaff = user.position?.is_staff || false;  // Проверяем is_staff
      this.userData = user;
      this.setDashboardComponent();
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
      alert('Ошибка загрузки профиля.');
      this.$router.push('/login');
    }
  },
  methods: {
    setDashboardComponent() {
      console.log('Данные пользователя:', this.userData);
      console.log('is_staff:', this.isStaff);  // Логируем is_staff для проверки

      if (this.role === 'agent') {
        this.dashboardComponent = AgentDashboard;
      }
      else if (this.role === 'employee') {
        if (this.isStaff) {
          this.dashboardComponent = DirectorDashboard;  // Director как is_staff
        } else {
          this.dashboardComponent = EmployeeDashboard;
        }
      }
      else if (this.role === 'admin') {
        this.dashboardComponent = AdminDashboard;
      }
      else {
        this.dashboardComponent = null;
        alert('Неизвестная роль.');
      }
    },
  },
};
</script>
