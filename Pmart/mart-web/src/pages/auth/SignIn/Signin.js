import React, { useEffect, useState, useCallback } from 'react';
import { useDispatch } from 'react-redux';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import useAxios from '../../../useAxios';
import { sendSignInOtpService, signInService } from './Signin.service';
import { setAccessToken } from '../../../authHelper';
import { login } from '../../../redux/authSlice';
import CircularProgressLoader from '../../../components/CircularProgress';
import Validator from '../../../utils/Validators';
import ErrorMsg from '../../../components/ErrorMsg';
import { Link } from 'react-router-dom';

const SignIn = () => {
  const [form, setForm] = useState({ email: '', password: '', otp: '' });
  const [isOtp, setIsOtp] = useState(false);
  const [otpSent, setOtpSent] = useState(false);

  const [signInData, signInError, signInLoading, postSignIn, setSignInError] = useAxios();
  const [sendOTPData, sendOtpError, sendOtpLoading, fetchOtp, setSendOtpError] = useAxios();

  const dispatch = useDispatch();

  useEffect(() => {
    if (signInData?.success) {
      setAccessToken(signInData.access, signInData.refresh).then(() => {
        dispatch(login(true))
      }).catch(err=>{
        console.log(err)
      })
    }
  }, [signInData, dispatch]);

  useEffect(() => {
    if (sendOTPData?.success) {
      setOtpSent(true);
    }
  }, [sendOTPData]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = useCallback(() => {
    if (!form.email) return 'Email is required';
    if (!Validator.isValidEmail(form.email)) return 'Please enter a valid email';
    if (!isOtp && !form.password) return 'Password is required';
    if (isOtp && otpSent && !form.otp) return 'Please enter OTP';
    return null;
  }, [form, isOtp, otpSent]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = validateForm();
    if (error) {
      setSignInError(error);
      return;
    }

    const payload = {
      email: form.email,
      ...(isOtp ? { otp: form.otp.trim() } : { password: form.password }),
    };
    postSignIn(signInService(payload));
  };

  const generateOtp = () => {
    if (!Validator.isValidEmail(form.email)) {
      setSignInError('Please enter a valid email');
      return;
    }
    setSignInError('');
    fetchOtp(sendSignInOtpService({ email: form.email }));
  };

  const resetStates = () => {
    setForm({ email: '', password: '', otp: '' });
    setSignInError('');
    setSendOtpError('');
    setOtpSent(false);
    setIsOtp((prev) => !prev);
  };

  const renderButton = (text, onClick, loading) => (
    <Button type='submit' onClick={onClick} fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
      {loading ? <CircularProgressLoader /> : text}
    </Button>
  );

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 8,
        }}
      >
        <Typography component="h1" variant="h5">Sign In</Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '100%' }}>
          <TextField
            margin="normal" fullWidth label="Email Address" name="email" autoComplete="email"
            autoFocus required value={form.email} onChange={handleInputChange}
            slotProps={{ input: {readOnly: isOtp && otpSent}, }}
          />
          {isOtp && otpSent && (
            <TextField
              margin="normal" fullWidth name="otp" label="OTP" type="number" value={form.otp}
              onChange={handleInputChange}
            />
          )}
          {!isOtp && (
            <TextField
              margin="normal" fullWidth name="password" label="Password" type="password"
              autoComplete="current-password" value={form.password} onChange={handleInputChange}
            />
          )}
          {(signInError || sendOtpError) && <ErrorMsg errorState={[signInError, sendOtpError]} />}
          {(!otpSent && isOtp) && <Button onClick={generateOtp} fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
          {sendOtpLoading ? <CircularProgressLoader /> : 'Generate OTP'}
          </Button>}
          {(isOtp && otpSent || !isOtp) && renderButton('Login', handleSubmit, signInLoading)}
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Typography variant="subtitle1" sx={{ cursor: 'pointer', color: 'primary.main' }}>
            <Link to='/signup'>Sign Up</Link>
          </Typography>
          <Typography
            variant="subtitle1" sx={{ cursor: 'pointer', color: 'primary.main' }}
            onClick={resetStates}
          >
            Login with {isOtp ? 'Password' : 'OTP'}
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default SignIn;