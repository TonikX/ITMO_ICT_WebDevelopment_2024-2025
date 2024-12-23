import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { fetchOwners, deleteOwner } from '../api/api';
import { Owner } from '../shared/types';
import Search from "antd/es/input/Search";

const OwnersList: React.FC = () => {
    const [owners, setOwners] = useState<Owner[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const navigate = useNavigate();

    const loadOwners = async (search: string = '') => {
        setLoading(true);
        try {
            const data = await fetchOwners(search);
            setOwners(data);
        } catch (error) {
            message.error('Ошибка при загрузке списка владельцев.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadOwners();
    }, []);

    const handleSearch = (value: string) => {
        setSearchTerm(value);
        loadOwners(value);
    };

    const handleDelete = async (id: string) => {
        try {
            await deleteOwner(id);
            message.success('Владелец удалён.');
            loadOwners();
        } catch (error) {
            message.error('Ошибка при удалении.');
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
            title: 'Контакты',
            dataIndex: 'contact_info',
            key: 'contact_info',
        },
        {
            title: 'Действия',
            key: 'actions',
            render: (record: Owner) => (
                <>
                    <Button
                        type="link"
                        onClick={() => navigate(`/owners/edit/${record.id}`)}
                    >
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
            <h1>Owners</h1>
            <Button
                type="primary"
                style={{ marginBottom: 16 }}
                onClick={() => navigate('/owners/new')}
            >
                Создать нового владельца
            </Button>
            <br/>
            <Search
                placeholder="Поиск владельцев"
                allowClear
                enterButton="Поиск"
                size="large"
                onSearch={handleSearch}
                style={{ maxWidth: 400, marginBottom: 16 }}
            />
            <Table
                dataSource={owners}
                columns={columns}
                rowKey="id"
                loading={loading}
            />
        </div>
    );
};

export default OwnersList;
