import React, { useState } from 'react';

const AddItemForm = ({ addItem }) => {
  const [itemName, setItemName] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (itemName) {
      addItem(itemName);
      setItemName('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={itemName}
        onChange={(e) => setItemName(e.target.value)}
        placeholder="Enter Your Stock Market Question Here"
      />
      <button type="submit">Submit Question</button>
    </form>
  );
};

export default AddItemForm;
