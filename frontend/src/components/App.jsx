import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import Footer from './Footer';

function App() {
    return (
        <Router>
            <Navbar/>
            <Routes>
                <Route path="/" element={<Home/>} />
            </Routes>
            <Footer />
        </Router>
    );
}

export default App;