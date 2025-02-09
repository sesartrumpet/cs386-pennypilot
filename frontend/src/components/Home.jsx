import React, { useEffect, useState } from 'react';

function Home() {
    return (
        <div>
            <header>
                <h1>Welcome to PennyPilot</h1>
                <p>Track your expenses and stay on budget!</p>
            </header>

            <main>
            {/* add more here */}
                <h2>
                    Current Expenses
                </h2>
            {/* expense list here */}
            </main>

            <footer>
                <p>&copy; 
                    2025 PennyPilot
                </p>
            </footer>
        </div>
    );
}

export default Home;