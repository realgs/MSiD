import React from 'react';
import './App.css'
import Header from './components/Header';
import Wallet from './components/Wallet';

function App() {
  return (
    <div className='main-app'>
      <Header/>
      <Wallet/>
    </div>
  );
}

export default App;
