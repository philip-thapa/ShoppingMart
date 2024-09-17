import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid2, Card, CardContent, Typography } from '@mui/material';
import { INTERNAL_MODULES } from './constants';
import BaseComponent from './Base';


function Home() {
  const navigate = useNavigate();

  const handleCardClick = (path) => {
    navigate(path);
  };

  return (
    <BaseComponent>
    <div style={{ padding: '20px' }}>
      <Typography variant="h4" gutterBottom>
        Mart Modules
      </Typography>
      <Grid2 container spacing={3}>
        {INTERNAL_MODULES.map((module, index) => (
          <Grid2 item xs={12} sm={6} md={4} lg={2} key={index}>
            <Card 
              onClick={() => handleCardClick(module.path)} 
              sx={{ cursor: 'pointer', '&:hover': { boxShadow: 6 } }}
            >
              <CardContent>
                <Typography variant="h6" align="center">
                  {module.name}
                </Typography>
              </CardContent>
            </Card>
          </Grid2>
        ))}
      </Grid2>
    </div>
    </BaseComponent>
  );
}

export default Home;