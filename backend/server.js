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

// Start the server
app.listen(PORT, () => {
	console.log(`Server running on http://localhost:${PORT}`);
});