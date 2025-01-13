import getAPI from '../axios-api.js';
import { createStore } from 'vuex';

export default createStore({
  state: {
    accessToken: null,
    refreshToken: null,
  },
  mutations: {
    updateState(state, { accessToken, refreshToken }) {
      state.accessToken = accessToken;
      state.refreshToken = refreshToken;
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
    },
  },
  getters: {
    loggedIn(state) {
      state.accessToken !== null
    }
  },
  actions: {
    userLogin(context, userCredentials) {
      return new Promise((resolve, reject) => {
        getAPI
          .post('http://127.0.0.1:8000/api/token/', {
            username: userCredentials.username,
            password: userCredentials.password,
          })
          .then(response => {
            context.commit('updateState', {
              accessToken: response.data.access,
              refreshToken: response.data.refresh,
            });
            resolve();
          })
          .catch(error => {
            reject(error);
          });
      });
    },

    userLogout(context) {
      if (context.getters.loggedIn) {
        context.commit('destroyToken')
      }
    },

    getUserProfile(context) {
      const token = context.rootState.accessToken;
      return new Promise((resolve, reject) => {
        getAPI
          .get('http://127.0.0.1:8000/auth/users/me/', {
            // refresh: context.state.refreshToken,
            headers: {
              Authorization: `JWT ${token}`,
            },
          })
          .then(response => {
            resolve(response.data); // Возвращаем данные API через resolve
          })
          .catch(error => {
            reject(error);
          });
          })

      },

    updateUserProfile(context, userProfile) {
      const token = context.rootState.accessToken;
      return new Promise((resolve, reject) => {
        getAPI
          .put('http://127.0.0.1:8000/auth/users/me/', userProfile, {
            headers: {
              Authorization: `JWT ${token}`,
            },
          })
          .then(response => {
            resolve(response.data); // Возвращаем данные API через resolve
          })
          .catch(error => {
            reject(error);
          });
        })
      },
  },

  modules: {
    HenStore: {
      namespaced: true,
      state: {
        hens: [],
      },
      mutations: {
        updateHens(state, hens) {
          state.hens = hens;
        },
      },
      actions: {
        fetchHens(context) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .get('http://127.0.0.1:8000/hens/', {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.commit('updateHens', response.data);
            })
            .catch(error => {
              console.error('Error fetching hens:', error);
              throw error;
            });
        },
        createHen(context, hen) { // Добавление новой курицы
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .post('http://127.0.0.1:8000/hens/create/', hen, {
              headers: {
                Authorization: `JWT ${token}`,
              },
              body: JSON.stringify(hen),
            })
            .then(response => {
              // context.commit('updateHens', response.data);
              context.dispatch('fetchHens');
            })
            .catch(error => {
              console.error('Error creating hen:', error);
              throw error;
            })
          },

        updateHen(context, { id, hen }) { // Добавление новой курицы
          console.log(hen);
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .put(`http://127.0.0.1:8000/hens/${id}/update/`, hen, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchHens');
            })
            .catch(error => {
              console.error('Error creating hen:', error);
              throw error;
            })
          },

          deleteHen(context, henId) { // Удаление курицы
            const token = context.rootState.accessToken;
            if (!token) {
              console.error('Access token is missing');
              return Promise.reject(new Error('Access token is missing'));
            }

            return getAPI
              .delete(`http://127.0.0.1:8000/hens/${henId}/delete/`, {
                headers: {
                  Authorization: `JWT ${token}`,
                },
              })
              .then(response => {
                context.dispatch('fetchHens');
              })
              .catch(error => {
                console.error('Error deleting hen:', error);
                throw error;
              })
          },


        },
    },

    WorkshopStore: {
      namespaced: true,
      state: {
        workshops: [],
      },
      mutations: {
        updateWorkshops(state, workshops) {
          state.workshops = workshops;
        },
      },
      actions: {
        fetchWorkshops(context) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .get('http://127.0.0.1:8000/workshops/', {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.commit('updateWorkshops', response.data);
            })
            .catch(error => {
              console.error('Error fetching workshops:', error);
              throw error;
            })
        },

        updateWorkshop(context, { id, workshop }) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .put(`http://127.0.0.1:8000/workshops/${id}/update/`, workshop, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchWorkshops');
            })
            .catch(error => {
              console.error('Error updating workshop:', error);
              throw error;
            })
        },
      },
    },

    CageStore: {
      namespaced: true,
      state: {
        cages: [],
      },
      mutations: {
        updateCages(state, cages) {
          state.cages = cages;
        },
      },
      actions: {
        fetchCages(context) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .get('http://127.0.0.1:8000/cages/', {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.commit('updateCages', response.data);
            })
            .catch(error => {
              console.error('Error fetching cages:', error);
              throw error;
            });
        },

        createCage(context, cage) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .post('http://127.0.0.1:8000/cages/create/', cage, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchCages');
            })
            .catch(error => {
              console.error('Error creating cage:', error);
              throw error;
          })
        },

        updateCage(context, { id, cage }) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .put(`http://127.0.0.1:8000/cages/${id}/update/`, cage, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchCages');
            })
            .catch(error => {
              console.error('Error updating cage:', error);
              throw error;
            })
        },
        deleteCage(context, id) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .delete(`http://127.0.0.1:8000/cages/${id}/delete/`, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchCages');
            })
            .catch(error => {
              console.error('Error deleting cage:', error);
              throw error;
            })
        }
      },
    },

    DietStore: {
      namespaced: true,
      state: {
        diets: [],
      },
      mutations: {
        updateDiets(state, diets) {
          state.diets = diets;
        },
      },
      actions: {
        fetchDiets(context) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .get('http://127.0.0.1:8000/diets/', {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.commit('updateDiets', response.data);
            })
            .catch(error => {
              console.error('Error fetching diets:', error);
              throw error;
            });
        },
        createDiet(context, diet) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
          }

          return getAPI
            .post('http://127.0.0.1:8000/diets/create/', diet, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchDiets');
            })
            .catch(error => {
              console.error('Error creating diet:', error);
              throw error;
            })
        },
        updateDiet(context, { id, diet }) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
          }

          return getAPI
            .put(`http://127.0.0.1:8000/diets/${id}/update/`, diet, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchDiets');
            })
            .catch(error => {
              console.error('Error updating diet:', error);
              throw error;
            })
        },
        deleteDiet(context, id) {
          const token = context.rootState.accessToken;
          if (!token) {
            console.error('Access token is missing');
          }

          return getAPI
            .delete(`http://127.0.0.1:8000/diets/${id}/delete/`, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchDiets');
            })
            .catch(error => {
              console.error('Error deleting diet:', error);
              throw error;
            })
        },
      },
    },

    BreedStore: {
      namespaced: true,
      state: {
        breeds: [],
      },
      mutations: {
        updateBreeds(state, breeds) {
          state.breeds = breeds;
        },
      },
      actions: {
        fetchBreeds(context) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .get('http://127.0.0.1:8000/breeds/', {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.commit('updateBreeds', response.data);
            })
            .catch(error => {
              console.error('Error fetching breeds:', error);
              throw error;
            });
        },

        createBreed(context, breed) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .post('http://127.0.0.1:8000/breeds/create/', breed, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchBreeds');
            })
            .catch(error => {
              console.error('Error creating breed:', error);
              throw error;

          })
        },

        updateBreed(context, { id, breed }) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .put(`http://127.0.0.1:8000/breeds/${id}/update/`, breed, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchBreeds');
            })
            .catch(error => {
              console.error('Error updating breed:', error);
              throw error;
            })
        },

        deleteBreed(context, id) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .delete(`http://127.0.0.1:8000/breeds/${id}/delete/`, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchBreeds');
            })
            .catch(error => {
              console.error('Error deleting breed:', error);
              throw error;
            })
        },
      },
    },

    EmployeeStore: {
      namespaced: true,
      state: {
        employees: [],
      },
      mutations: {
        updateEmployees(state, employees) {
          state.employees = employees;
        },
      },
      actions: {
        fetchEmployees(context) {
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .get('http://127.0.0.1:8000/employees/', {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.commit('updateEmployees', response.data);
            })
            .catch(error => {
              console.error('Error fetching employees:', error);
              throw error;
            });
        },

        createEmployee(context, employee) { // Добавление нового сотрудника
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .post('http://127.0.0.1:8000/employees/create/', employee, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchEmployees'); // Обновление списка сотрудников после создания
            })
            .catch(error => { // Обработка ошибок
              console.error('Error creating employee:', error);
              throw error;
            }
            );
        },

        updateEmployee(context, { id, employee }) { // Обновление существующего сотрудника
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .put(`http://127.0.0.1:8000/employees/${id}/update/`, employee, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchEmployees'); // Обновление списка сотрудников после обновления
            })
            .catch(error => { // Обработка ошибок
              console.error('Error updating employee:', error);
              throw error;
            }
            );
        },

        deleteEmployee(context, id) { // Удаление сотрудника
          const token = context.rootState.accessToken; // Доступ к глобальному состоянию
          if (!token) {
            console.error('Access token is missing');
            return Promise.reject(new Error('Access token is missing'));
          }

          return getAPI
            .delete(`http://127.0.0.1:8000/employees/${id}/delete/`, {
              headers: {
                Authorization: `JWT ${token}`,
              },
            })
            .then(response => {
              context.dispatch('fetchEmployees'); // Обновление списка сотрудников после удаления
            })
            .catch(error => { // Обработка ошибок
              console.error('Error deleting employee:', error);
              throw error;
            }
            );
          }
      },
    },
  },
});
