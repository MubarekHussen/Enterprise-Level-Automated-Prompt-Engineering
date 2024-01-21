import React, { useState } from 'react';

const Input = ({ objective, setObjective, setFileInput, fileInput, handleSubmit }) => {
  const [expectedOutput, setExpectedOutput] = useState('');

  const handleObjectiveChange = (event) => {
    setObjective(event.target.value);
  };

  const handleExpectedOutputChange = (event) => {
    setExpectedOutput(event.target.value);
  };

  const handleFileInputChange = (event) => {
    setFileInput(event.target.files[0]);
  };

  return (
    <>
      <div className='flex flex-col  justify-center h-screen py-20 mx-20'>
        <div className='bg-gray-200 p-8 rounded-lg shadow-lg h-full'>
          <h2 className='text-3xl font-bold mb-4'>Chat Input</h2>
          <div className='mb-4'>
            <label htmlFor='text1' className='text-lg'>
              Objective
            </label>
            <textarea
              id='text1'
              value={objective}
              onChange={handleObjectiveChange}
              className='w-full px-4 py-2 h-40 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200'
            />
          </div>
          <div className='mb-4'>
            <label htmlFor='text2' className='text-lg'>
              Expected Output
            </label>
            <input
              id='text2'
              type='text'
              value={expectedOutput}
              onChange={handleExpectedOutputChange}
              className='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200'
            />
          </div>
          <div className='mb-4'>
            <label htmlFor='file' className='text-lg'>
              File Input
            </label>
            <input
              id='file'
              type='file'
              onChange={handleFileInputChange}
              className='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200'
            />
          </div>
          <button
            onClick={handleSubmit}
            disabled={!fileInput}
            className='bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-200'
          >
            Submit
          </button>
        </div>
      </div>
    </>
  );
};

export default Input;