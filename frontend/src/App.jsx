import React, { useState } from 'react';
import Input from './components/Input/Input';
import Output from './components/Output/Output';

const App = () => {
  const [objective, setObjective] = useState('');
  const [expectedOutput, setExpectedOutput] = useState('');
  const [fileInput, setFileInput] = useState(null);
  const [apiData, setApiData] = useState([]);

  const handleObjectiveSubmit = async () => {
    const data = { objective: objective, expected_output: expectedOutput };
  
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

  const handleFileUpload = async (file) => {
    if (!file) {
      console.error('No file to upload');
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      console.log('File uploaded successfully');
      return response;
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const uploadResponse = await handleFileUpload(fileInput);
    if (uploadResponse && uploadResponse.ok) {
      handleObjectiveSubmit();
    }
  };

  return (
    <div className='md:flex h-96'>
      <div className='md:w-1/2'>
      <Input objective={objective} setObjective={setObjective} setFileInput={setFileInput} fileInput={fileInput} handleSubmit={handleSubmit} />
      </div>
      <div className='md:w-1/2'>
        <Output data={apiData} />
      </div>
    </div>
  );
};

export default App;