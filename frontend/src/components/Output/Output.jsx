import React from 'react';

const Output = () => {
  return (
    <div className='flex flex-col items-center justify-center h-screen py-20'>
      <div className='bg-gray-200 p-8 rounded-lg shadow-lg h-full'>
        <h2 className='text-3xl font-bold mb-4'>Output</h2>
        <div className='flex'>
          <div className='mb-4'>
            <label htmlFor='prompt' className='text-lg'>
              Prompt:
            </label>
            <div className='bg-white px-4 py-2 border border-gray-300 rounded-md shadow-sm w-96'>
              Output Text Here
            </div>
          </div>
          <div className='mb-4 mx-3'>
            <label htmlFor='score' className='text-lg'>
              Score:
            </label>
            <div className='bg-white px-4 py-2 border border-gray-300 rounded-md shadow-sm'>
              Output Score Here
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Output;
