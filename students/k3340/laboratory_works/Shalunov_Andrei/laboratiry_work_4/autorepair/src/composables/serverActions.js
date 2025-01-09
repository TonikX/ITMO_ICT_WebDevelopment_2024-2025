import axiosInstance from "@/services/axios.js";

export const fetchAndReturn = async (path, dataRef, loadingRef, errorRef) => {
  try {
    loadingRef.value = true;
    const response = await axiosInstance.get(path);
    dataRef.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке данных:", error);
    errorRef.value = error;
  } finally {
    loadingRef.value = false;
  }
};

export const createContract = async (clientId, autoId, details) => {
  try {
    const response = await axiosInstance.post('contracts/', {
      client: clientId,
      auto: autoId,
      ...details,
    });
    return response.data;
  } catch (error) {
    console.error("Ошибка при создании контракта:", error);
    return null;
  }
};

export const postComment = async (contractId, header, content) => {
  try {
    const response = await axiosInstance.post(`comments/`, {
      contract_id: contractId,
      header: header,
      content_text: content,
    });
    return response.data;
  } catch (error) {
    console.error("Ошибка при отправке комментария:", error);
    return null;
  }
};

export const canEdit = async (contractId) => {
  try {
    const response = await axiosInstance.get(`contracts/${contractId}/canEdit/`);
    return response.data.can_edit;
  } catch (error) {
    console.error("Ошибка при проверке прав редактирования:", error);
    return false;
  }
};
