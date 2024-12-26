import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, List } from 'antd';
import { Show } from '../shared/types';
import { fetchDogs, fetchExperts, fetchShows, fetchParticipations } from '../api/api';

const Dashboard: React.FC = () => {
    const [dogsCount, setDogsCount] = useState(0);
    const [expertsCount, setExpertsCount] = useState(0);
    const [showsCount, setShowsCount] = useState(0);
    const [participationsCount, setParticipationsCount] = useState(0);
    const [upcomingShows, setUpcomingShows] = useState<Show[]>([]);
    const [pastShows, setPastShows] = useState<Show[]>([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        const [dogs, experts, shows, participations] = await Promise.all([
            fetchDogs(),
            fetchExperts(),
            fetchShows(),
            fetchParticipations(),
        ]);

        setDogsCount(dogs.length);
        setExpertsCount(experts.length);
        setShowsCount(shows.length);
        setParticipationsCount(participations.length);

        const now = new Date();
        const upcoming = shows.filter((show) => new Date(show.date) > now);
        const past = shows.filter((show) => new Date(show.date) <= now);

        upcoming.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
        past.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

        setUpcomingShows(upcoming.slice(0, 5));
        setPastShows(past.slice(0, 5));
    };

    return (
        <div>
            <h1>Дашборд</h1>
            <Row gutter={16}>
                <Col span={6}>
                    <Card>
                        <Statistic title="Собаки" value={dogsCount}/>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic title="Эксперты" value={expertsCount}/>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic title="Выставки" value={showsCount}/>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic title="Участия" value={participationsCount}/>
                    </Card>
                </Col>
            </Row>

            <h2 style={{marginTop: 24}}>Предстоящие выставки</h2>
            <List
                bordered
                dataSource={upcomingShows}
                renderItem={(show) => (
                    <List.Item>
                        <div>
                            <strong>{show.name}</strong> — {show.date} ({show.location})
                        </div>
                    </List.Item>
                )}
            />

            <h2 style={{marginTop: 24}}>Прошедшие выставки</h2>
            <List
                bordered
                dataSource={pastShows}
                renderItem={(show) => (
                    <List.Item>
                        <div>
                            <strong>{show.name}</strong> — {show.date} ({show.location})
                        </div>
                    </List.Item>
                )}
            />
        </div>
    );
};

export default Dashboard;
