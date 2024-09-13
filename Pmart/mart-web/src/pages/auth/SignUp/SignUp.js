import React, {useState, useCallback, useEffect } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import CircularProgressLoader from '../../../components/CircularProgress';
import { Link, useNavigate } from 'react-router-dom';
import useAxios from '../../../useAxios';
import SendIcon from '@mui/icons-material/Send';
import { sendOtpService, signUpService, verifyOtpService } from './SignUp.service';
import Validator from '../../../utils/Validators';

const SignUp = () => {
  const OTP_STATUS = {
    NOT_SENT: 'NOT_SENT',
    SENT: 'SENT',
  }
  const navigate = useNavigate();
  const [form, setForm] = useState({ firstName: '', lastName: '', email: '', otp: '', password: ''});
  const [otpStatus, setOtpStatus] = useState(OTP_STATUS.NOT_SENT);

  const [sendOTPData, sendOtpError, sendOtpLoading, fetchOtp] = useAxios();
  const [signUpData, signUpError, signUpLoading, fetchSignup] = useAxios();

  useEffect(() => {
    if (sendOTPData?.success){
      setOtpStatus(OTP_STATUS.SENT);
    }
  }, [sendOTPData])

  useEffect(() => {
    if (signUpData?.success){
      navigate('/signin')
    }
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = useCallback(() => {
    if (!form.email) return 'Email is required';
    if (!Validator.isValidEmail(form.email)) return 'Please enter a valid email';
    if (!form.otp) return 'Please enter otp';
    if (!form.password) return 'Please enter password';
    return null;
  }, [form]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = validateForm();
    if (error) {
      signUpError(error);
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
      fetchOtp(sendOtpService({
        'email': form.email
      }))
  }

  const renderButton = (text, onClick, loading) => (
    <Button onClick={onClick} fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
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
        <Typography component="h1" variant="h5">Sign Up</Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '100%' }}>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '100%', display: 'flex', flexDirection: 'row', }}>
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
            slotProps={{ input: {readOnly: otpStatus == OTP_STATUS.SENT }, }}
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
            required value={form.password} onChange={handleInputChange}
          />
          <Button type='submit' fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
            Sign Up
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