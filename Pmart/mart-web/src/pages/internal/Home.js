import { Box } from '@mui/material'
import React from 'react'
import ModuleCard from '../../components/Modules'

function Home() {
  return (
    <>
        <Box 
        sx={{
            display: 'flex', flexDirection: 'row', alignItems: 'center', marginTop: 8,
        }}>
            <ModuleCard title={'Users'} imgSrc={''} link={''} />

        </Box>
    </>
    
  )
}

export default Home