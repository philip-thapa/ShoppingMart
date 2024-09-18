import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, Typography } from '@mui/material';
import Grid from '@mui/material/Grid';

import { INTERNAL_MODULES } from './constants';
import BaseComponent from '../../components/Internal/Base';


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
      <Grid container spacing={3}>
        {INTERNAL_MODULES.slice(1).map((module, index) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={index}>
            <Card 
              onClick={() => handleCardClick(module.additionalPath)} 
              sx={{ cursor: 'pointer', '&:hover': { boxShadow: 6 } }}
            >
              <CardContent>
                <Typography variant="h6" align="center">
                  {module.name}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
    </BaseComponent>
  );
}

export default Home;