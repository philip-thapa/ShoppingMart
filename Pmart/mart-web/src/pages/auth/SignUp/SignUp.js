import React, {useState, useCallback, useEffect } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import CircularProgressLoader from '../../../components/CircularProgress';
import { Link } from 'react-router-dom';
import useAxios from '../../../useAxios';
import { sendSignUpOtpService, signUpService } from './SignUp.service';
import Validator from '../../../utils/Validators';
import ErrorMsg from '../../../components/ErrorMsg';
import { setAccessToken, storeToken } from '../../../authHelper';
import { login } from '../../../redux/authSlice';
import { useDispatch } from 'react-redux';

const SignUp = () => {
  const OTP_STATUS = {
    NOT_SENT: 'NOT_SENT',
    SENT: 'SENT',
  }
  const [form, setForm] = useState({ firstName: '', lastName: '', email: '', otp: '', password: '', confirmPassword: ''});
  const [otpStatus, setOtpStatus] = useState(OTP_STATUS.NOT_SENT);

  const [sendOTPData, sendOtpError, sendOtpLoading, fetchOtp, setSendOtpError] = useAxios();
  const [signUpData, signUpError, signUpLoading, fetchSignup, setSignUpError] = useAxios();

  const dispatch = useDispatch();

  useEffect(() => {
    if (sendOTPData?.success){
      setOtpStatus(OTP_STATUS.SENT);
    }
  }, [sendOTPData])

  useEffect(() => {

    const handleSignUp = async () => {
      if (signUpData?.success){
        setAccessToken(signUpData?.access, signUpData?.refresh);
        dispatch(login());
      }
    }
    handleSignUp();
  }, [signUpData, dispatch])

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = useCallback(() => {
    if (!form.firstName) return 'First Name is required'
    if (!form.email) return 'Email is required';
    if (!Validator.isValidEmail(form.email)) return 'Invalid Email';
    if (otpStatus === OTP_STATUS.NOT_SENT){
      return 'Verify the Email'
    }
    if (!form.otp) return 'OTP is required';
    if (!form.password) return 'Password is required';
    if (form.password !== form.confirmPassword) return 'Password doesnot match'
    return null;
  }, [form]);

  const resetStates = () => {
    setSendOtpError(() => '');
    setSignUpError(() => '');
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    resetStates();
    const error = validateForm();
    if (error) {
      setSignUpError(error);
      return;
    }

    const payload = {
      firstName: form.firstName,
      lastName: form.lastName,
      email: form.email,
      otp: form.otp,
      password: form.password
    };
    fetchSignup(signUpService(payload));
  };

  const handleOtp = () => {
      resetStates();
      fetchOtp(sendSignUpOtpService({
        'email': form.email
      }))
  }

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 8,
        }}
      >
        <Typography component="h1" variant="h5">Sign Up</Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '100%' }}>
          <Box sx={{ mt: 1, width: '100%', display: 'flex', flexDirection: 'row', }}>
            <TextField
              margin="normal" fullWidth label="First Name" name="firstName"
              autoFocus required value={form.firstName} onChange={handleInputChange}
            />
            <TextField
                margin="normal" fullWidth label="Last Name" name="lastName"
                value={form.lastName} onChange={handleInputChange}
            />
          </Box>
          
          <TextField
            margin="normal" fullWidth label="Email Address" name="email"
            required value={form.email} onChange={handleInputChange}
            slotProps={{ input: {readOnly: otpStatus === OTP_STATUS.SENT }, }}
            autoComplete="username"
          />
          {
            otpStatus === OTP_STATUS.NOT_SENT && form.email && 
            <Button onClick={handleOtp} variant="outlined" color='success' size="small">{sendOtpLoading ? <CircularProgressLoader /> :'Verify Email'}</Button>
          }
          {otpStatus === OTP_STATUS.SENT && 
          <TextField
            margin="normal" fullWidth label="Otp" name="otp"
            required value={form.otp} onChange={handleInputChange}
          />}
          {
            otpStatus === OTP_STATUS.SENT && 
            <Button onClick={handleOtp} variant="outlined" color='success' size="small">{sendOtpLoading ? <CircularProgressLoader /> :'Send OTP again'}</Button>
          }
          <TextField
            margin="normal" fullWidth name="password" label="Password" type="password"
            required value={form.password} onChange={handleInputChange} autoComplete="new-password" 
          />
          <TextField
            margin="normal" fullWidth name="confirmPassword" label="Confirm Password" type="password"
            required value={form.confirmPassword} onChange={handleInputChange}
          />
          {(signUpError || sendOtpError) && <ErrorMsg errorState={[signUpError, sendOtpError]} />}
          <Button type='submit' fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
            {signUpLoading ? <CircularProgressLoader /> :'Sign Up'}
          </Button>
        </Box>
        <Box
          sx={{
            display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'start'
          }}>
            <Typography variant="subtitle1" sx={{ cursor: 'pointer', color: 'primary.main' }}>
              <Link to='/signin'>Sign In</Link>
            </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default SignUp;