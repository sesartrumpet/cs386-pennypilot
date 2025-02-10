import React from 'react';

function Home() {
    return (

        <div style={{ textAlign: 'center', padding: '50px' }}>
            <h1>Welcome to Penny Pilot</h1>
            <p>Your go to platform for financial insights and stock tracking.</p>
            <button style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>
                Get Started
            </button>


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
