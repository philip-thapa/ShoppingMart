import React, { useEffect, useState } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import useAxios from '../../../useAxios';
import { signInService } from './Signin.service';
import { storeToken } from '../../../authHelper';
import { login } from '../../../redux/authSlice';
import { useDispatch } from 'react-redux';
import CircularProgressLoader from '../../../components/CircularProgress';
import Validator from '../../../utils/Validators';
import ErrorMsg from '../../../components/ErrorMsg';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [isOtp, setIsOtp] = useState(false);
  const [otpSent, setIsOtpSent] = useState(false);

  const [signInData, signInError, signInLoading, postSignIn, setSignInError] = useAxios();
  const [sendOTPData, sendOtpError, sendOtpLoading, fetchOtp] = useAxios();

  const errorState = [signInError, sendOtpError];

  const dispatch = useDispatch();

  useEffect(() => {
    if (signInData?.success){
      storeToken(signInData?.access, signInData?.refresh);
      dispatch(login())
    }
  }, [signInData])

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!email) {
      setSignInError('Email is required');
      return;
    }

    if (!Validator.isValidEmail(email)){
      setSignInError('Please enter a valid email');
      return;
    }

    if(isOtp){
      if (otpSent) {
        if(!otp) {
          setSignInError("Please enter OTP");
          return;
        }
      } else {

      }

    } else {
      if (!password){
        setSignInError('Password is required');
        return;
      }
    }

    postSignIn(signInService({
      'email': email,
      'password': password
    }))

  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 8,
        }}>
        <Typography component="h1" variant="h5">Sign In</Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '100%' }}>
          <TextField margin="normal" fullWidth label="Email Address" id="email" name="email" autoComplete="email" autoFocus 
            value={email} onChange={(e) => setEmail(e.target.value)} sx={{width: '100%'}} />
          {
            isOtp && otpSent  &&
            <TextField
              margin="normal" fullWidth
              name="otp"
              label="OTP"
              type="number"
              id="otp"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />
          }
          { !isOtp &&
            <TextField
              margin="normal" fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          }
          {
            errorState && <ErrorMsg errorState={errorState} />
          }
          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} >
            {signInLoading ? <CircularProgressLoader /> : 'Login'}
          </Button>
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', width: '100%'}}>
          <Typography variant="subtitle1" gutterBottom
            sx={{cursor: 'pointer', color: 'primary.main'}}>
            Sign Up
          </Typography>
          <Typography variant="subtitle1" gutterBottom sx={{cursor: 'pointer', color: 'primary.main'}}
            onClick={() => {
              setEmail('');
              setSignInError('');
              setIsOtpSent(false);
              setIsOtp(!isOtp);

            }}>
            Login with {isOtp ? ' Password': ' OTP'}
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default SignIn;