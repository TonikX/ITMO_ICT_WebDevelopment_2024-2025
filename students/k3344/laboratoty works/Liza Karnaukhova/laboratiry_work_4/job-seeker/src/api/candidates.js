class CandidatesApi {
  constructor(instance) {
    this.API = instance;
  }

  // Получение информации о профиле
  getProfile = async () => {
    return this.API({ url: '/candidates/profile' });
  };

  // Обновление информации о профиле
  updateProfile = async (data) => {
    return this.API({
      method: 'PUT',
      url: '/candidates/profile',
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  };
}

export default CandidatesApi;
