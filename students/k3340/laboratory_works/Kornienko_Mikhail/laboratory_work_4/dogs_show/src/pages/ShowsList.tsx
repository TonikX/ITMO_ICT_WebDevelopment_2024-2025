import React, { useEffect, useState } from 'react';
import { Table, Button, message, Input } from 'antd';
import { useNavigate } from 'react-router-dom';
import { Show } from '../shared/types';
import { fetchShows, deleteShow } from '../api/api';

const { Search } = Input;

const ShowsList: React.FC = () => {
    const [shows, setShows] = useState<Show[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();

    const loadShows = async (search = '') => {
        setLoading(true);
        try {
            const data = await fetchShows(search);
            setShows(data);
        } catch (error) {
            message.error('Ошибка при загрузке списка выставок.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (value: string) => {
        setSearchTerm(value);
        loadShows(value);
    };

    useEffect(() => {
        loadShows();
    }, []);

    const handleDelete = async (id: string) => {
        try {
            await deleteShow(id);
            message.success('Выставка удалена');
            loadShows(searchTerm);
        } catch (error) {
            message.error('Ошибка при удалении выставки');
        }
    };

    const columns = [
        {
            title: 'Название',
            dataIndex: 'name',
            key: 'name',
            render: (text: string, record: Show) => (
                <Button type="link" onClick={() => navigate(`/shows/${record.id}`)}>
                    {text}
                </Button>
            ),
        },
        {
            title: 'Дата',
            dataIndex: 'date',
            key: 'date',
        },
        {
            title: 'Тип',
            dataIndex: 'type',
            key: 'type',
        },
        {
            title: 'Локация',
            dataIndex: 'location',
            key: 'location',
        },
        {
            title: 'Спонсор',
            dataIndex: 'sponsor',
            key: 'sponsor',
        },
        {
            title: 'Действия',
            key: 'actions',
            render: (record: Show) => (
                <>
                    <Button type="link" onClick={() => navigate(`/shows/edit/${record.id}`)}>
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
            <h1>Список выставок</h1>
            <Button
                type="primary"
                style={{marginBottom: 16}}
                onClick={() => navigate('/shows/new')}
            >
                Добавить выставку
            </Button>
            <br/>
            <Search
                placeholder="Поиск выставок"
                allowClear
                enterButton="Поиск"
                size="large"
                onSearch={handleSearch}
                style={{maxWidth: 400, marginBottom: 16}}
            />
            <Table
                dataSource={shows}
                columns={columns}
                rowKey="id"
                loading={loading}
            />
        </div>
    );
};

export default ShowsList;
