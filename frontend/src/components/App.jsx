import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import Footer from './Footer';
import Login from './Login';

function App() {
    const [username, setUsername] = useState(localStorage.getItem('username') || '');
    const [searchTerms, setSearchTerms] = useState('');
    const [filter, setFilter] = useState('ALL')

    useEffect(() => {
        const storedUsername = localStorage.getItem('username');
        if (storedUsername) {
            setUsername(storedUsername);
        }
    }, []);

    return (
        <Router>
            <Navbar/>
            <Routes>
                <Route path="/" element={<Home/>} />
                <Route path="/Login" element={<Login/>}/>
            </Routes>
            <Footer />
        </Router>
    );
}

export default App;