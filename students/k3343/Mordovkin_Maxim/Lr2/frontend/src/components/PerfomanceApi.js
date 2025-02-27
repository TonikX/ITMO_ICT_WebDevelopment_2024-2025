// PerformanceApi.js
import axios from 'axios';

/**
 * Запрашивает у бэкенда статистику успеваемости класса
 * (для текущего ученика, извлекаемого из JWT).
 *
 * Ожидается, что бэкенд реализует эндпойнт:
 *    GET /api/performance/my-class
 * который возвращает массив объектов типа:
 *    {
 *      "assignmentId": number,
 *      "title": string,
 *      "avgGrade": number
 *    }
 */
export async function getClassPerformance() {
    const response = await axios.get('/api/performance/my-class');
    return response.data;
}
