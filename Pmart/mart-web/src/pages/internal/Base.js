import React, { useState } from 'react';
import { Button, Drawer, IconButton, List, ListItem, ListItemText } from '@mui/material';
import DensityMediumIcon from '@mui/icons-material/DensityMedium';

const BaseComponent = ({ children }) => {
  const [open, setOpen] = useState(false);

  const toggleDrawer = (isOpen) => (event) => {
    if (
      event.type === 'keydown' &&
      (event.key === 'Tab' || event.key === 'Shift')
    ) {
      return;
    }
    setOpen(isOpen);
  };

  const DrawerList = () => (
    <List>
      <ListItem button>
        <ListItemText primary="Item 1" />
      </ListItem>
      <ListItem button>
        <ListItemText primary="Item 2" />
      </ListItem>
      <ListItem button>
        <ListItemText primary="Item 3" />
      </ListItem>
    </List>
  );

  return (
    <>
      <IconButton
        edge="start"
        color="inherit"
        aria-label="open drawer"
        onClick={toggleDrawer(true)}
        sx={{ ml: 2 }}
      >
        <DensityMediumIcon />
      </IconButton>

      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList()}
      </Drawer>

      <div style={{ padding: '20px' }}>
        {children}
      </div>
    </>
  );
};

export default BaseComponent;
