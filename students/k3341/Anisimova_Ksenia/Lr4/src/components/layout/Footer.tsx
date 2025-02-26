import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer: React.FC = () => {
    return (
        <Box component="footer" sx={{ p: 2, textAlign: 'center', backgroundColor: '#f5f5f5', marginTop: '2rem' }}>
            <Typography variant="body2" color="text.secondary">
                © {new Date().getFullYear()} Ksyusha's Newspaper App. No rights reserved.
            </Typography>
        </Box>
    );
};

export default Footer;
