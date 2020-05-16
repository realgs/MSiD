import React from 'react';
import './App.css'
import Header from './components/Header';
import Wallet from './components/Wallet';

function App() {
  return (
    <div className='main-app'>
      <Header></Header>
      <Wallet></Wallet>
    </div>
  );
}

export default App;
