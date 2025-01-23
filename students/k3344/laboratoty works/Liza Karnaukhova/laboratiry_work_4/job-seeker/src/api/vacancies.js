class VacanciesApi {
  constructor(instance) {
    this.API = instance;
  }

  getAll = async (filters) =>
    this.API({
      url: '/vacancies',
      params: filters,
    });

  getById = async (id) => this.API({ url: `/vacancies/${id}` });

  create = async (data) =>
    this.API({
      method: 'POST',
      url: '/vacancies',
      data,
      headers: { 'Content-Type': 'application/json' },
    });

  update = async (id, data) =>
    this.API({
      method: 'PUT',
      url: `/vacancies/${id}`,
      data,
      headers: { 'Content-Type': 'application/json' },
    });

  delete = async (id) =>
    this.API({
      method: 'DELETE',
      url: `/vacancies/${id}`,
    });
}

export default VacanciesApi;
