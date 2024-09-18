import React, { useState } from 'react';
import { AppBar, Button, Drawer, IconButton, List, ListItem, ListItemText, Toolbar, Typography } from '@mui/material';
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

const BaseComponent = ({ title, align='center', actions, children }) => {
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
    <Box sx={{ width: 300 }} role="presentation" onClick={toggleDrawer(false)}>
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
      flexDirection="row"
      justifyContent="flex-start"
      sx={{
        backgroundColor: '#f5f5f5',
        boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', 
      }}
      >

      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <IconButton edge="end" onClick={toggleDrawer(true)}>
              <DensityMediumIcon />
            </IconButton>
            <Box
              sx={{
                flexGrow: 1,
                display: 'flex',
                justifyContent: align,
                alignItems: 'center',
              }}>
              <Typography variant="h6" component="div">
                {title}
              </Typography>
            </Box>
            {actions}
          </Toolbar>
        </AppBar>
      </Box>
    </Box>

      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>

      <div>
        {children}
      </div>
    </>
  );
};

export default BaseComponent;
