import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Dog, Show, Participation, Expert } from '../shared/types';
import { fetchDogs, fetchShows, fetchParticipations, createParticipation, createGrade, fetchExperts } from '../api/api';
import { Card, Table, Button, Select, Modal, Form, message } from 'antd';

const DogDetail: React.FC = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [dog, setDog] = useState<Dog | null>(null);
    const [participations, setParticipations] = useState<Participation[]>([]);
    const [allShows, setAllShows] = useState<Show[]>([]);
    const [experts, setExperts] = useState<Expert[]>([]);
    const [loading, setLoading] = useState(false);

    const [isAddParticipationModalVisible, setIsAddParticipationModalVisible] = useState(false);
    const [selectedShowId, setSelectedShowId] = useState<string | null>(null);

    const [isGradeModalVisible, setIsGradeModalVisible] = useState(false);
    const [selectedParticipationId, setSelectedParticipationId] = useState<string | null>(null);
    const [selectedExpertId, setSelectedExpertId] = useState<string | null>(null);
    const [score, setScore] = useState<number>(0);

    const loadDog = async (dogId: string) => {
        try {
            const dogs = await fetchDogs();
            const found = dogs.find((d) => d.id === dogId);
            if (found) setDog(found);
        } catch (error) {
            message.error('Ошибка при загрузке собаки');
        }
    };

    const loadParticipations = async (dogId: string) => {
        setLoading(true);
        try {
            const allParticipations = await fetchParticipations();
            const filtered = allParticipations.filter((p) => p.dog_id === dogId);
            setParticipations(filtered);
        } catch (error) {
            message.error('Ошибка при загрузке участий');
        } finally {
            setLoading(false);
        }
    };

    const loadShows = async () => {
        try {
            const shows = await fetchShows();
            setAllShows(shows);
        } catch (error) {
            message.error('Ошибка при загрузке выставок');
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
            loadDog(id);
            loadParticipations(id);
            loadShows();
            loadExperts();
        }
        // eslint-disable-next-line
    }, [id]);

    const handleAddParticipation = async () => {
        if (!selectedShowId || !id) return;
        try {
            await createParticipation({
                dog_id: id,
                show_id: selectedShowId,
                participation_type: 'individual',
                medical_exam_passed: false,
                payment_made: false,
            });
            message.success('Участие добавлено');
            setIsAddParticipationModalVisible(false);
            loadParticipations(id);
        } catch (error) {
            message.error('Ошибка при добавлении участия');
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

    if (!dog) return <div>Загрузка...</div>;

    const columns = [
        {
            title: 'Выставка',
            key: 'showName',
            render: (record: Participation) => (
                <Button type="link" onClick={() => navigate(`/shows/${record.show_id}`)}>
                    {record.show?.name || record.show_id}
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

    return (
        <div>
            <h1>Детали собаки: {dog.name}</h1>
            <Card style={{ marginBottom: 16 }}>
                <p>Порода: {dog.breed}</p>
                <p>Возраст: {dog.age}</p>
                <p>Классность: {dog.class_name}</p>
                <p>Клуб: {dog.club_name}</p>
                <p>Владелец: {dog.owner?.last_name} {dog.owner?.first_name}</p>
            </Card>

            <h2>Участия собаки</h2>
            <Button type="primary" onClick={() => setIsAddParticipationModalVisible(true)}>
                Добавить участие
            </Button>
            <Table
                columns={columns}
                dataSource={participations}
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
                title="Добавить участие"
                visible={isAddParticipationModalVisible}
                onOk={handleAddParticipation}
                onCancel={() => setIsAddParticipationModalVisible(false)}
                okText="Добавить"
                cancelText="Отмена"
            >
                <p>Выберите выставку:</p>
                <Select
                    style={{ width: '100%' }}
                    onChange={(val) => setSelectedShowId(val)}
                    placeholder="Выберите выставку"
                >
                    {allShows.map((sh) => (
                        <Select.Option key={sh.id} value={sh.id}>
                            {sh.name} — {sh.date}
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
                            {ex.last_name} {ex.first_name}
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

export default DogDetail;
