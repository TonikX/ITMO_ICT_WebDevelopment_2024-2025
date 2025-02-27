import React, { useEffect, useState } from 'react';
import { FaBook, FaClipboardList, FaChartBar } from 'react-icons/fa';
import { fetchAssignments } from '../components/AssigmentApi';
import { createSubmission, getMySubmissions } from '../components/SubmissionApi';
import { getClassPerformance } from '../components/PerfomanceApi';
import '../components/css/MainPage.css';

const StudentPage = () => {
    const [assignments, setAssignments] = useState([]);
    const [submissions, setSubmissions] = useState([]);
    const [classStats, setClassStats] = useState([]);
    const [selectedAssignment, setSelectedAssignment] = useState(null);
    const [content, setContent] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        // 1) Загрузить все задания
        fetchAssignments()
            .then(data => setAssignments(data))
            .catch(err => setError(err.message));

        // 2) Загрузить свои сдачи
        getMySubmissions()
            .then(data => setSubmissions(data))
            .catch(err => setError(err.message));

        // 3) Загрузить успеваемость класса
        getClassPerformance()
            .then(data => setClassStats(data))
            .catch(err => setError(err.message));
    }, []);

    const handleSubmit = async () => {
        if (!selectedAssignment || !content.trim()) {
            setError('Please enter your submission content');
            return;
        }

        try {
            await createSubmission(selectedAssignment.assignmentId, content);
            const updatedSub = await getMySubmissions();
            setSubmissions(updatedSub);
            setContent('');
            setSelectedAssignment(null);
            setError('');
        } catch (err) {
            setError(err.response?.data?.message || err.message);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/';
    };

    return (
        <div className="page-container">
            <header className="page-header">
                <h1 className="page-title">Student Dashboard</h1>
                <button onClick={handleLogout} className="logout-btn">Sign Out</button>
            </header>

            {error && <div className="error-message">{error}</div>}

            <div className="card">
                <div className="section-title">
                    <FaBook /> Current Assignments
                </div>
                <div className="table-container">
                    <table className="harvard-table">
                        <thead>
                        <tr>
                            <th>Assignment</th>
                            <th>Due Date</th>
                            <th>Action</th>
                        </tr>
                        </thead>
                        <tbody>
                        {assignments.map(a => (
                            <tr key={a.assignmentId}>
                                <td>{a.title}</td>
                                <td>{new Date(a.dueDate).toLocaleDateString()}</td>
                                <td>
                                    <button
                                        className="btn btn-primary"
                                        onClick={() => setSelectedAssignment(a)}
                                    >
                                        Submit
                                    </button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {selectedAssignment && (
                <div className="card">
                    <h3 className="section-title">Submit Assignment: {selectedAssignment.title}</h3>
                    <textarea
                        className="input-field"
                        rows={6}
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        placeholder="Enter your submission here..."
                    />
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <button className="btn btn-primary" onClick={handleSubmit}>
                            Submit
                        </button>
                        <button
                            className="btn btn-secondary"
                            onClick={() => setSelectedAssignment(null)}
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}

            <div className="card">
                <div className="section-title">
                    <FaClipboardList /> My Submissions
                </div>
                <div className="table-container">
                    <table className="harvard-table">
                        <thead>
                        <tr>
                            <th>Assignment</th>
                            <th>Submission</th>
                            <th>Grade</th>
                            <th>Submitted</th>
                        </tr>
                        </thead>
                        <tbody>
                        {submissions.map(s => (
                            <tr key={s.submissionId}>
                                <td>{s.assignment?.title}</td>
                                <td>{s.content}</td>
                                <td>{s.grade != null ? s.grade : '—'}</td>
                                <td>{new Date(s.submittedAt).toLocaleString()}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="card">
                <div className="section-title">
                    <FaChartBar /> Class Performance
                </div>
                <div className="table-container">
                    <table className="harvard-table">
                        <thead>
                        <tr>
                            <th>Assignment</th>
                            <th>Class Average</th>
                        </tr>
                        </thead>
                        <tbody>
                        {classStats.map(stat => (
                            <tr key={stat.assignmentId}>
                                <td>{stat.title}</td>
                                <td>
                                    {stat.avgGrade !== null
                                        ? `${stat.avgGrade.toFixed(2)}%`
                                        : '—'
                                    }
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default StudentPage;