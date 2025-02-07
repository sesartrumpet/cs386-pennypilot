import React, { useState } from 'react';
import { TextField, Button, Tabs, Tab, Box } from '@mui/material';
import { Link, useNavigate } from "react-router-dom";
import { styled } from '@mui/material/styles';

const Login = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try{
            const response = await fetch('http://localhost:3000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            })
        
            const data = await response.json();

            if (response.ok && data.success) {
                localStorage.setItem('username', username);
                localStorage.setItem('email', email);
                localStorage.setItem('password', password);
                navigate('/Profile');
            }
            else{
                setMessage(data.message || 'Login failed');
            }
        }
        catch (error) {
            console.error('Error:', error);
            setMessage('An unexpected error occurred, please try again.')
        }
    }

    return (
        <Box
            sx={{
                padding: 3,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
            }}
        >
            <h2>Log in</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Box centered="true">
                    <TextField
                        variant="outlined"
                        label="Username"
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        inputProps={{ maxLength: 24 }}
                        sx={{ marginBottom: 2, minWidth: 500 }}
                    />
                </Box>
                <Box centered="true">
                    <TextField
                        variant="outlined"
                        label="Email"
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        inputProps={{ maxLength: 64 }}
                        sx={{ marginBottom: 2, minWidth: 500 }}
                    />
                </Box>
                <Box centered="true">
                    <TextField
                        variant="outlined"
                        label="Password"
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        inputProps={{ maxLength: 64 }}
                        sx={{ marginBottom: 2, minWidth: 500 }}
                    />
                </Box>
                <Button
                    type="submit"
                    centered="true"
                    variant="contained"
                    sx={{ marginBottom: 2, minWidth: 500 }}
                >
                    Log in
                </Button>
            </form>
            <p>Don't have an account? <Link to="/Register">Sign up</Link></p>
            <p>{message}</p>
        </Box>
    );
};

export default Login;