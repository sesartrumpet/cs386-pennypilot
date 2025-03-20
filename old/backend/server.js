const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require("path");
const sharp = require('sharp');
const cors = require('cors');
const dotenv = require('dotenv');

// Load environment variables
//dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/pennypilotDB', {
    useNewUrlParser: true
})
	.then(() => console.log('Connected to MongoDB'))
	.catch(err => console.error('Error connecting to MongoDB:', err));

// Function to log a user in
const loginUser = async (username, email, password) => {
    try {
        const user = await User.findOne({username, email, password});
        if (user){
            return user
        }
        return null;
    }
    catch (err) {
        console.error('Error logging in1', err)
    }
}

// Endpoint for user registration
app.post('/api/register', async (req, res) => {
        const { username, password, confPassword, email } = req.body;
        const likes = [];
        const posts = [];

        if (!username || !password || !confPassword || !email) {
                return res.send('Please fill all fields.');
        }
        if (password !== confPassword) {
                return res.send('Passwords do not match.');
        }
        
        try {
            const newUser = new User({username, password, email, likes, posts});
            await newUser.save();
            res.send('User registered successfully!');
        } catch (error) {
            console.error('Error during user registration: ', error);
            res.send('Error registering user.');
        }
});


// Start the server
app.listen(PORT, () => {
	console.log(`Server running on http://localhost:${PORT}`);
});