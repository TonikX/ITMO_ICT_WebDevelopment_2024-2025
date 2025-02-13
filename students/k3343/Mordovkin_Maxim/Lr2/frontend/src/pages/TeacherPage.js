import React, { useEffect, useState } from 'react';
import { FaPlus, FaClipboardCheck, FaGraduationCap } from 'react-icons/fa';
import { fetchAssignments, createAssignment } from '../components/AssigmentApi';
import { getSubmissionsByAssignment, gradeSubmission } from '../components/SubmissionApi';
import '../components/css/MainPage.css';

const TeacherPage = () => {
    const [assignments, setAssignments] = useState([]);
    const [title, setTitle] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [selectedAssignment, setSelectedAssignment] = useState(null);
    const [submissions, setSubmissions] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        loadAssignments();
    }, []);

    const loadAssignments = () => {
        fetchAssignments()
            .then(data => setAssignments(data))
            .catch(err => setError(err.message));
    };

    const handleCreate = async () => {
        setError('');
        if (!title.trim() || !dueDate) {
            setError('Please enter both title and due date');
            return;
        }

        try {
            await createAssignment(title, dueDate);
            await loadAssignments();
            setTitle('');
            setDueDate('');
        } catch (err) {
            setError(err.response?.data?.message || err.message);
        }
    };

    const handleViewSubmissions = async (assignment) => {
        try {
            const subs = await getSubmissionsByAssignment(assignment.assignmentId);
            setSelectedAssignment(assignment);
            setSubmissions(subs);
        } catch (err) {
            setError(err.response?.data?.message || err.message);
        }
    };

    const handleGrade = async (submissionId, newGrade) => {
        if (newGrade < 0 || newGrade > 100) {
            setError('Grade must be between 0 and 100');
            return;
        }

        try {
            await gradeSubmission(submissionId, newGrade);
            const subs = await getSubmissionsByAssignment(selectedAssignment.assignmentId);
            setSubmissions(subs);
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
                <h1 className="page-title">Teacher Dashboard</h1>
                <button onClick={handleLogout} className="logout-btn">Sign Out</button>
            </header>

            {error && <div className="error-message">{error}</div>}

            <div className="card">
                <div className="section-title">
                    <FaPlus /> Create Assignment
                </div>
                <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: '1fr 1fr auto' }}>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Assignment Title"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                    />
                    <input
                        type="datetime-local"
                        className="input-field"
                        value={dueDate}
                        onChange={e => setDueDate(e.target.value)}
                    />
                    <button className="btn btn-primary" onClick={handleCreate}>
                        Create
                    </button>
                </div>
            </div>

            <div className="card">
                <div className="section-title">
                    <FaClipboardCheck /> Active Assignments
                </div>
                <div className="table-container">
                    <table className="harvard-table">
                        <thead>
                        <tr>
                            <th>Title</th>
                            <th>Due Date</th>
                            <th>Action</th>
                        </tr>
                        </thead>
                        <tbody>
                        {assignments.map(a => (
                            <tr key={a.assignmentId}>
                                <td>{a.title}</td>
                                <td>{new Date(a.dueDate).toLocaleString()}</td>
                                <td>
                                    <button
                                        className="btn btn-primary"
                                        onClick={() => handleViewSubmissions(a)}
                                    >
                                        View Submissions
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
                    <div className="section-title">
                        <FaGraduationCap /> Submissions for: {selectedAssignment.title}
                    </div>
                    <div className="table-container">
                        <table className="harvard-table">
                            <thead>
                            <tr>
                                <th>Student</th>
                                <th>Class</th>
                                <th>Submission</th>
                                <th>Current Grade</th>
                                <th>Update Grade</th>
                            </tr>
                            </thead>
                            <tbody>
                            {submissions.map(sub => (
                                <tr key={sub.submissionId}>
                                    <td>{sub.student?.username}</td>
                                    <td>{sub.student?.classNumber || '—'}</td>
                                    <td>{sub.content}</td>
                                    <td>{sub.grade != null ? `${sub.grade}%` : '—'}</td>
                                    <td>
                                        <input
                                            type="number"
                                            className="input-field"
                                            min="0"
                                            max="100"
                                            placeholder="Grade (0-100)"
                                            onChange={(e) => handleGrade(sub.submissionId, e.target.value)}
                                        />
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TeacherPage;