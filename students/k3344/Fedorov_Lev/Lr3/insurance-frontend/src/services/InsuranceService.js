import apiClient from './apiClient';

export default {
    // Получение всех страховых случаев
    getInsuranceCases() {
        return apiClient.get('/insurance/insurance_cases/')
            .then(response => response.data)
            .catch(error => {
                console.error('Ошибка загрузки страховых случаев:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Создание нового страхового случая
    submitInsuranceCase(newCase) {
        return apiClient.post('/insurance/insurance_cases/', newCase)
            .then(response => response.data)
            .catch(error => {
                console.error('Ошибка подачи страхового случая:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Обновление страхового случая
    updateInsuranceCase(updatedCase) {
        return apiClient.patch(`/insurance/insurance_cases/${updatedCase.id}/`, updatedCase)
            .then(response => response.data)
            .catch(error => {
                console.error('Ошибка обновления страхового случая:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Получение списка контрактов
    getContracts() {
        return apiClient.get('/insurance/contracts/')
            .then(response => response.data)
            .catch(error => {
                console.error('Ошибка загрузки контрактов:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Создание нового контракта
    createContract(newContract) {
        return apiClient.post('/insurance/contracts/', newContract)
            .then(response => {
                console.log('Контракт успешно создан:', response.data);
                return response.data;
            })
            .catch(error => {
                console.error('Ошибка при создании контракта:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Удаление контракта (разрыв)
    terminateContract(contractId) {
        return apiClient.delete(`/insurance/contracts/${contractId}/terminate/`)
            .then(response => {
                console.log(`Контракт ${contractId} успешно удален`);
                return response.data;
            })
            .catch(error => {
                console.error('Ошибка при удалении контракта:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Получение списка агентов
    getAgents() {
        return apiClient.get('/insurance/agents/')
            .then(response => response.data)
            .catch(error => {
                console.error('Ошибка загрузки агентов:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Получение агента по user_id
    getAgentByUserId(userId) {
        return apiClient.get(`/insurance/agents/?user_id=${userId}`)
            .then(response => response.data[0])  // Берем первого в списке
            .catch(error => {
                console.error('Ошибка при получении агента по user_id:', error.response ? error.response.data : error.message);
                throw error;
            });
    },

    // Получение агента по username (НОВЫЙ МЕТОД)
    async getAgentByUsername(username) {
        try {
            const response = await apiClient.get('/insurance/agents/');
            const agent = response.data.find(agent => agent.first_name === username);

            if (!agent) {
                throw new Error(`Агент с username "${username}" не найден.`);
            }

            return agent;
        } catch (error) {
            console.error('Ошибка при получении агента по username:', error.response ? error.response.data : error.message);
            throw error;
        }
    }
};
