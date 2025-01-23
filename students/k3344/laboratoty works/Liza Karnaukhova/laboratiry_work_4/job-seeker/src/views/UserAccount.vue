<template>
  <base-layout>
    <HeaderComponent />
    <main-details-layout>
      <h1 class="text-center mb-4">Личный кабинет </h1>
      <section-layout>
        <UserInfo v-if="userInfoVisible" :email="userEmail" />
      </section-layout>
      <section-layout>
        <ResumeTable :resumes="userResumes" @add-resume="showResumeModal" />
      </section-layout>
    </main-details-layout>
    <ResumeModal v-if="isModalVisible" @close="isModalVisible = false" @submit="addResume" />
    <FooterComponent />
  </base-layout>
</template>

<script>
  import { ref, onMounted } from 'vue';
  import { useUsersStore } from '@/stores/users';
  import { useResumesStore } from '@/stores/resumes';
  import HeaderComponent from '@/components/HeaderComponent.vue';
  import FooterComponent from '@/components/FooterComponent.vue';
  import UserInfo from '@/components/UserInfo.vue';
  import ResumeTable from '@/components/ResumeTable.vue';
  import ResumeModal from '@/components/ResumeModal.vue';
  import BaseLayout from "@/layout/BaseLayout.vue";
  import MainDetailsLayout from "@/layout/MainDetailsLayout.vue";
  import SectionLayout from "@/layout/SectionLayout.vue";

  export default {
    components: {
      HeaderComponent,
      FooterComponent,
      UserInfo,
      ResumeTable,
      ResumeModal,
      BaseLayout,
      MainDetailsLayout,
      SectionLayout,
    },
    setup() {
      const usersStore = useUsersStore();
      const resumesStore = useResumesStore();
      const isModalVisible = ref(false);
      const userInfoVisible = ref(false);
      const userEmail = ref('');
      const userResumes = ref([]);

      onMounted(async () => {
        await usersStore.loadProfile();
        await resumesStore.loadResumes();
        userEmail.value = usersStore.profile?.email || '';
        userResumes.value = resumesStore.resumes;
        userInfoVisible.value = !!usersStore.profile;
      });

      const showResumeModal = () => {
        isModalVisible.value = true;
      };

      const addResume = async (resumeData) => {
        await resumesStore.createResume(resumeData);
        userResumes.value = resumesStore.resumes; // Обновляем список резюме
        isModalVisible.value = false; // Закрываем модальное окно
      };

      return {
        isModalVisible,
        userInfoVisible,
        userEmail,
        userResumes,
        showResumeModal,
        addResume,
      };
    },
  };
</script>

<style scoped>
  /* Добавьте стили, если необходимо */
</style>
