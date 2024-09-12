import { Typography } from '@mui/material'
import React from 'react'

function ErrorMsg({errorState}) {
  return (
    errorState.map((error, index) => (
        error && (
            <Typography key={index} color="error" variant="body2" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )
    ))
  )
}

export default ErrorMsg