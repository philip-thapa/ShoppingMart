import React, { useState } from 'react';
import { Drawer, IconButton, List, ListItem, ListItemText, Typography } from '@mui/material';
import DensityMediumIcon from '@mui/icons-material/DensityMedium';
import ListItemIcon from '@mui/material/ListItemIcon';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import ListItemButton from '@mui/material/ListItemButton';
import { useNavigate } from 'react-router-dom';
import { removeAccessToken } from '../../authHelper';
import { useDispatch } from 'react-redux';
import LogoutIcon from '@mui/icons-material/Logout';
import { checkAuthStatus } from '../../redux/authSlice';
import { INTERNAL_MODULES } from '../../pages/internal/constants';

const BaseComponent = ({ title='Mart', children }) => {
  const [open, setOpen] = useState(false);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const toggleDrawer = (isOpen) => (event) => {
    if (
      event.type === 'keydown' &&
      (event.key === 'Tab' || event.key === 'Shift')
    ) {
      return;
    }
    setOpen(isOpen);
  };

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      <List>
        {INTERNAL_MODULES.map((module, index) => (
          <ListItem key={index} disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {module.icon}
              </ListItemIcon>
              <ListItemText primary={module.name} onClick={() => navigate(module.additionalPath)} />
            </ListItemButton>
          </ListItem>
        ))}
        <Divider />
        <ListItem sx={{padding: 0}}>
            <ListItemButton>
              <ListItemIcon>
                <LogoutIcon />
              </ListItemIcon>
              <ListItemText primary="Logout" onClick={() => {
                removeAccessToken().then(res=>{
                  dispatch(checkAuthStatus())
                })
              }}/>
            </ListItemButton>
          </ListItem>
      </List>
      <Divider />
    </Box>
  );

  return (
    <>
    <Box
      display="flex" 
      alignItems="center" 
      flexDirection="row"
      justifyContent="space-between" 
      sx={{ padding: '10px 20px', backgroundColor: '#f5f5f5' }}>
      <IconButton
          edge="start"
          color="inherit"
          aria-label="open drawer"
          onClick={toggleDrawer(true)}
          sx={{ ml: 2 }}
        >
        <DensityMediumIcon />
      </IconButton>
      <Typography variant="h6" component="div" sx={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
          {title}
      </Typography>
    </Box>
      
      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>

      <div style={{ padding: '20px' }}>
        {children}
      </div>
    </>
  );
};

export default BaseComponent;
