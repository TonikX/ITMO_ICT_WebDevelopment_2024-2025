// submissionsApi.js
import axios from 'axios';

// Отправить решение
export async function createSubmission(assignmentId, content) {
    const response = await axios.post('/api/submissions', {
        assignmentId,
        content
    });
    return response.data;
}

// Поставить оценку (Teacher)
export async function gradeSubmission(submissionId, grade) {
    const response = await axios.put(`/api/submissions/${submissionId}/grade`, {
        grade
    });
    return response.data;
}

// Получить все сдачи конкретного задания (Teacher)
export async function getSubmissionsByAssignment(assignmentId) {
    const response = await axios.get(`/api/submissions/by-assignment/${assignmentId}`);
    return response.data;
}

// Получить все свои сдачи (Student)
export async function getMySubmissions() {
    const response = await axios.get('/api/submissions/my');
    return response.data;
}
