import React from 'react';
import Input from './components/Input/Input';
import Output from './components/Output/Output';

const App = () => {
  return (
    <div className='md:flex h-96'>
      <div className='md:w-1/2'>
        <Input />
      </div>
      <div className='md:w-1/2'>
        <Output />
      </div>
    </div>
  );
};

export default App;
