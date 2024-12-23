import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Show, Dog, Participation, Expert } from '../shared/types';
import { fetchShows, fetchDogs, fetchExperts, fetchParticipations, createParticipation, createGrade } from '../api/api';
import { Card, Table, Button, Select, Modal, Form, message } from 'antd';

const ShowDetail: React.FC = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [show, setShow] = useState<Show | null>(null);
    const [participants, setParticipants] = useState<Participation[]>([]);
    const [allDogs, setAllDogs] = useState<Dog[]>([]);
    const [experts, setExperts] = useState<Expert[]>([]);
    const [loading, setLoading] = useState(false);

    const [isAddDogModalVisible, setIsAddDogModalVisible] = useState(false);
    const [selectedDogId, setSelectedDogId] = useState<string | null>(null);

    const [isGradeModalVisible, setIsGradeModalVisible] = useState(false);
    const [selectedParticipationId, setSelectedParticipationId] = useState<string | null>(null);
    const [selectedExpertId, setSelectedExpertId] = useState<string | null>(null);
    const [score, setScore] = useState<number>(0);

    const loadShow = async (showId: string) => {
        try {
            const shows = await fetchShows();
            const found = shows.find((s) => s.id === showId);
            if (found) {
                setShow(found);
            }
        } catch (error) {
            message.error('Ошибка при загрузке выставки');
        }
    };

    const loadParticipants = async (showId: string) => {
        setLoading(true);
        try {
            const allParticipations = await fetchParticipations();
            const filtered = allParticipations.filter((p) => p.show_id === showId);
            setParticipants(filtered);
        } catch (error) {
            message.error('Ошибка при загрузке участников');
        } finally {
            setLoading(false);
        }
    };

    const loadAllDogs = async () => {
        try {
            const dogs = await fetchDogs();
            setAllDogs(dogs);
        } catch (error) {
            message.error('Ошибка при загрузке собак');
        }
    };

    const loadExperts = async () => {
        try {
            const exp = await fetchExperts();
            setExperts(exp);
        } catch (error) {
            message.error('Ошибка при загрузке экспертов');
        }
    };

    useEffect(() => {
        if (id) {
            loadShow(id);
            loadParticipants(id);
            loadAllDogs();
            loadExperts();
        }
        // eslint-disable-next-line
    }, [id]);

    const handleAddDog = async () => {
        if (!selectedDogId || !id) return;
        try {
            await createParticipation({
                dog_id: selectedDogId,
                show_id: id,
                participation_type: 'individual',
                medical_exam_passed: false,
                payment_made: false,
            });
            message.success('Собака добавлена на выставку');
            setIsAddDogModalVisible(false);
            loadParticipants(id);
        } catch (error) {
            message.error('Ошибка при добавлении собаки');
        }
    };

    const handleCreateGrade = async () => {
        if (!selectedParticipationId || !selectedExpertId) return;
        try {
            await createGrade({
                participation_id: selectedParticipationId,
                expert_id: selectedExpertId,
                score,
            });
            message.success('Оценка выставлена');
            setIsGradeModalVisible(false);
        } catch (error) {
            message.error('Ошибка при выставлении оценки');
        }
    };

    const columns = [
        {
            title: 'Собака',
            key: 'dogName',
            render: (record: Participation) => (
                <Button type="link" onClick={() => navigate(`/dogs/${record.dog_id}`)}>
                    {record.dog?.name || record.dog_id}
                </Button>
            ),
        },
        {
            title: 'Оплачено',
            dataIndex: 'payment_made',
            key: 'payment_made',
            render: (val: boolean) => (val ? 'Да' : 'Нет'),
        },
        {
            title: 'Медосмотр',
            dataIndex: 'medical_exam_passed',
            key: 'medical_exam_passed',
            render: (val: boolean) => (val ? 'Пройден' : 'Не пройден'),
        },
        {
            title: 'Действия',
            key: 'actions',
            render: (record: Participation) => (
                <Button
                    type="link"
                    onClick={() => {
                        setSelectedParticipationId(record.id);
                        setIsGradeModalVisible(true);
                    }}
                >
                    Поставить оценку
                </Button>
            ),
        },
    ];

    if (!show) return <div>Загрузка...</div>;

    return (
        <div>
            <h1>Детали выставки: {show.name}</h1>
            <Card style={{ marginBottom: 16 }}>
                <p>Тип: {show.type}</p>
                <p>Дата: {show.date}</p>
                <p>Локация: {show.location}</p>
                <p>Спонсор: {show.sponsor}</p>
                <p>Расписание рингов: {show.ring_schedule}</p>
            </Card>

            <h2>Участники выставки</h2>
            <Button type="primary" onClick={() => setIsAddDogModalVisible(true)}>
                Добавить собаку
            </Button>
            <Table
                columns={columns}
                dataSource={participants}
                rowKey="id"
                loading={loading}
                style={{ marginTop: 16 }}
                expandable={{
                    expandedRowRender: (record: Participation) => {
                        if (!record.grades || record.grades.length === 0) {
                            return <p>Нет оценок</p>;
                        }
                        return (
                            <Table
                                columns={[
                                    {
                                        title: 'Эксперт',
                                        dataIndex: ['expert', 'last_name'],
                                        key: 'expert_last_name',
                                        render: (_val, grade) => {
                                            return `${grade.expert?.last_name} ${grade.expert?.first_name}`;
                                        },
                                    },
                                    {
                                        title: 'Оценка',
                                        dataIndex: 'score',
                                        key: 'score',
                                    },
                                ]}
                                dataSource={record.grades}
                                rowKey="id"
                                pagination={false}
                            />
                        );
                    },
                }}
            />

            <Modal
                title="Добавить собаку на выставку"
                visible={isAddDogModalVisible}
                onOk={handleAddDog}
                onCancel={() => setIsAddDogModalVisible(false)}
                okText="Добавить"
                cancelText="Отмена"
            >
                <Select
                    style={{ width: '100%' }}
                    placeholder="Выберите собаку"
                    onChange={(value: string) => setSelectedDogId(value)}
                >
                    {allDogs.map((dog) => (
                        <Select.Option key={dog.id} value={dog.id}>
                            {dog.name} — {dog.breed}
                        </Select.Option>
                    ))}
                </Select>
            </Modal>

            <Modal
                title="Поставить оценку"
                visible={isGradeModalVisible}
                onOk={handleCreateGrade}
                onCancel={() => setIsGradeModalVisible(false)}
                okText="Сохранить"
                cancelText="Отмена"
            >
                <p>Выберите эксперта:</p>
                <Select
                    style={{ width: '100%', marginBottom: 8 }}
                    onChange={(val) => setSelectedExpertId(val)}
                    placeholder="Эксперт"
                >
                    {experts.map((ex) => (
                        <Select.Option key={ex.id} value={ex.id}>
                            {ex.last_name} {ex.first_name} — {ex.club_name}
                        </Select.Option>
                    ))}
                </Select>
                <p>Оценка (баллы):</p>
                <Form.Item>
                    <input
                        type="number"
                        value={score}
                        onChange={(e) => setScore(Number(e.target.value))}
                        style={{ width: '100%', padding: 8 }}
                    />
                </Form.Item>
            </Modal>
        </div>
    );
};

export default ShowDetail;
