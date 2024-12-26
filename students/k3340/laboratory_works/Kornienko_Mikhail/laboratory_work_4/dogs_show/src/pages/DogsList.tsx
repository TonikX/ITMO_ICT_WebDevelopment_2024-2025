import React, { useEffect, useState } from 'react';
import { Table, Button, message, Tag } from 'antd';
import { useNavigate } from 'react-router-dom';
import { fetchDogs, disqualifyDog, deleteDog } from '../api/api';
import { Dog } from '../shared/types';
import Search from "antd/es/input/Search";

const DogsList: React.FC = () => {
    const [dogs, setDogs] = useState<Dog[]>([]);
    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const navigate = useNavigate();

    const loadDogs = async (search: string = '') => {
        setLoading(true);
        try {
            const data = await fetchDogs(search);
            setDogs(data);
        } catch (error) {
            message.error('Ошибка при загрузке списка собак.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (value: string) => {
        setSearchTerm(value);
        loadDogs(value);
    };

    useEffect(() => {
        loadDogs();
    }, []);

    const handleDisqualify = async (id: string) => {
        try {
            const res = await disqualifyDog(id);
            message.info(res.status);
            loadDogs();
        } catch (error) {
            message.error('Ошибка при дисквалификации собаки.');
        }
    };

    const handleDelete = async (id: string) => {
        try {
            const res = await deleteDog(id);
            message.info(res.status);
            loadDogs();
        } catch (error) {
            message.error('Ошибка при дисквалификации собаки.');
        }
    };

    const columns = [
        {
            title: 'Кличка',
            dataIndex: 'name',
            key: 'name',
            render: (text: string, record: Dog) => (
                <Button type="link" onClick={() => navigate(`/dogs/${record.id}`)}>
                    {text}
                </Button>
            ),
        },
        {
            title: 'Порода',
            dataIndex: 'breed',
            key: 'breed',
        },
        {
            title: 'Клуб',
            dataIndex: 'club_name',
            key: 'club_name',
        },
        {
            title: 'Дисквалифицирована',
            dataIndex: 'disqualified',
            key: 'disqualified',
            render: (disqualified: boolean) =>
                disqualified ? <Tag color="red">Да</Tag> : <Tag color="green">Нет</Tag>,
        },
        {
            title: 'Действия',
            key: 'actions',
            render: (record: Dog) => (
                <>
                    <Button
                        type="link"
                        onClick={() => navigate(`/dogs/edit/${record.id}`)}
                    >
                        Редактировать
                    </Button>
                    {!record.disqualified && (
                        <Button
                            type="link"
                            danger
                            onClick={() => handleDisqualify(record.id)}
                        >
                            Дисквалифицировать
                        </Button>
                    )}
                    <Button
                        type="link"
                        danger
                        onClick={() => handleDelete(record.id)}
                    >
                        Удалить
                    </Button>
                </>
            ),
        },
    ];

    return (
        <div>
            <h1>Dogs</h1>
            <Button
                type="primary"
                style={{marginBottom: 16}}
                onClick={() => navigate('/dogs/new')}
            >
                Добавить собаку
            </Button>
            <br/>
            <Search
                placeholder="Поиск собаки"
                allowClear
                enterButton="Поиск"
                size="large"
                onSearch={handleSearch}
                style={{maxWidth: 400, marginBottom: 16}}
            />
            <Table
                dataSource={dogs}
                columns={columns}
                rowKey="id"
                loading={loading}
            />
        </div>
    );
};

export default DogsList;
