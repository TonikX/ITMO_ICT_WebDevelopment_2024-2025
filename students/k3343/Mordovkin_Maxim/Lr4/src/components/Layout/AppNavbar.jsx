import React from 'react';
import { Link } from 'react-router-dom';
import { Group, Text } from '@mantine/core';
import { IconPlane, IconChartBar, IconUser } from '@tabler/icons-react';
import { motion } from 'framer-motion';

const NavLink = ({ to, icon: Icon, label }) => (
    <Link to={to} style={{ textDecoration: 'none', color: 'inherit' }}>
        <Group p="xs" style={{ cursor: 'pointer', borderRadius: 4 }} className="nav-link">
            <Icon size={20} />
            <Text>{label}</Text>
        </Group>
    </Link>
);

const AppNavbar = () => {
    return (
        <motion.div
            initial={{ x: -250 }}
            animate={{ x: 0 }}
            transition={{ duration: 0.5 }}
            style={{ height: '100%', padding: '1rem' }}
        >
            <nav>
                <NavLink to="/" icon={IconPlane} label="Home" />
                <NavLink to="/flights" icon={IconPlane} label="Flights" />
                <NavLink to="/reports" icon={IconChartBar} label="Reports" />
                <NavLink to="/profile" icon={IconUser} label="Profile" />
            </nav>
        </motion.div>
    );
};

export default AppNavbar;
