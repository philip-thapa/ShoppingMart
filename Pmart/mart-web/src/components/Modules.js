import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const ModuleCard = ({ title, imgSrc, link }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(link);
  };

  return (
    <Card onClick={handleCardClick} sx={{ cursor: 'pointer', textAlign: 'center' }}>
      <img src={imgSrc} alt={title} style={{ width: '100px', margin: 'auto' }} />
      <CardContent>
        <Typography variant="h6">{title}</Typography>
      </CardContent>
    </Card>
  );
};


export default ModuleCard;
