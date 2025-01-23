class CompaniesApi {
  constructor(instance) {
    this.API = instance;
  }

  getCompanyByUser = async () => this.API({ url: '/companies/my' });

  updateCompany = async (data) =>
    this.API({
      method: 'PUT',
      url: '/companies/my',
      data,
      headers: { 'Content-Type': 'application/json' },
    });
}

export default CompaniesApi;
