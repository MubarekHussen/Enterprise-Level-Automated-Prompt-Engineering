import React, { useState } from 'react';
import Input from './components/Input/Input';
import Output from './components/Output/Output';

const App = () => {
  const [objective, setObjective] = useState('');
  const [apiData, setApiData] = useState([]);

  const handleSubmit = async () => {
    const data = { objective: objective };
  
    try {
      const response = await fetch('http://localhost:8000/generate-and-evaluate-prompts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const jsonResponse = await response.json();
      setApiData(jsonResponse);
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    }
  };

  return (
    <div className='md:flex h-96'>
      <div className='md:w-1/2'>
        <Input objective={objective} setObjective={setObjective} handleSubmit={handleSubmit} />
      </div>
      <div className='md:w-1/2'>
        <Output data={apiData} />
      </div>
    </div>
  );
};

export default App;