class ResponsesApi {
  constructor(instance) {
    this.API = instance;
  }

  getAllForVacancy = async (vacancyId) =>
    this.API({ url: `/responses?vacancyId=${vacancyId}` });

  markAsSuitable = async (id) =>
    this.API({
      method: 'PUT',
      url: `/responses/${id}/suitable`,
    });

  delete = async (id) =>
    this.API({
      method: 'DELETE',
      url: `/responses/${id}`,
    });

  create = async (data) =>
    this.API({
      method: 'POST',
      url: '/responses',
      data,
      headers: { 'Content-Type': 'application/json' },
    });
}

export default ResponsesApi;
