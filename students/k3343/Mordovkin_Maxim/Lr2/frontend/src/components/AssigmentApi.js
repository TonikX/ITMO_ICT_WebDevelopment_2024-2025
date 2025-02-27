// assignmentsApi.js
import axios from 'axios';

export async function fetchAssignments() {
    const response = await axios.get('/api/assignments');
    return response.data; // список
}

// Создание нового задания (только Teacher)
export async function createAssignment(title, dueDate) {
    const response = await axios.post('/api/assignments', {
        title,
        dueDate
    });
    return response.data;
}
