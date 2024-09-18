// BottomTabs.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BottomNavigation, BottomNavigationAction } from '@mui/material';

const BottomTabs = ({pages}) => {
  const navigate = useNavigate();
  const [value, setValue] = React.useState(0);

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <BottomNavigation
      value={value}
      onChange={(event, newValue) => {
        setValue(newValue);
        handleNavigation(pages[newValue].path);
      }}
      showLabels
      sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }}
    >
      {pages.map((module, index) => (
        <BottomNavigationAction
          key={index}
          label={module.name}
          icon={module.icon}
        />
      ))}
    </BottomNavigation>
  );
};

export default BottomTabs;
