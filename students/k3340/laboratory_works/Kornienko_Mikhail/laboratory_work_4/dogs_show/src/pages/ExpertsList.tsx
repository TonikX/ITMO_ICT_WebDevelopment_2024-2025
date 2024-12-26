import React, { useEffect, useState } from 'react';
import { Table, Button, message, Input } from 'antd';
import { useNavigate } from 'react-router-dom';
import { Expert } from '../shared/types';
import { fetchExperts, deleteExpert } from '../api/api';

const { Search } = Input;

const ExpertsList: React.FC = () => {
    const [experts, setExperts] = useState<Expert[]>([]);
    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();

    const loadExperts = async (search = '') => {
        setLoading(true);
        try {
            const data = await fetchExperts(search);
            setExperts(data);
        } catch (error) {
            message.error('Ошибка при загрузке списка экспертов.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (value: string) => {
        setSearchTerm(value);
        loadExperts(value);
    };

    useEffect(() => {
        loadExperts();
    }, []);

    const handleDelete = async (id: string) => {
        try {
            await deleteExpert(id);
            message.success('Эксперт удалён');
            loadExperts(searchTerm);
        } catch (error) {
            message.error('Ошибка при удалении эксперта');
        }
    };

    const columns = [
        {
            title: 'Фамилия',
            dataIndex: 'last_name',
            key: 'last_name',
        },
        {
            title: 'Имя',
            dataIndex: 'first_name',
            key: 'first_name',
        },
        {
            title: 'Клуб',
            dataIndex: 'club_name',
            key: 'club_name',
        },
        {
            title: 'Обслуживаемые ринги',
            dataIndex: 'rings_assigned',
            key: 'rings_assigned',
        },
        {
            title: 'Действия',
            key: 'actions',
            render: (record: Expert) => (
                <>
                    <Button type="link" onClick={() => navigate(`/experts/edit/${record.id}`)}>
                        Редактировать
                    </Button>
                    <Button type="link" danger onClick={() => handleDelete(record.id)}>
                        Удалить
                    </Button>
                </>
            ),
        },
    ];

    return (
        <div>
            <h1>Список экспертов</h1>
            <Button
                type="primary"
                style={{marginBottom: 16}}
                onClick={() => navigate('/experts/new')}
            >
                Добавить эксперта
            </Button>
            <br/>
            <Search
                placeholder="Поиск экспертов"
                allowClear
                enterButton="Поиск"
                size="large"
                onSearch={handleSearch}
                style={{maxWidth: 400, marginBottom: 16}}
            />
            <Table
                dataSource={experts}
                columns={columns}
                rowKey="id"
                loading={loading}
            />
        </div>
    );
};

export default ExpertsList;
