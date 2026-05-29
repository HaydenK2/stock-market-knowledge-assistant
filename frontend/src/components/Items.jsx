import React, { useEffect, useState } from 'react';
import api from '../api.js';
import AddItemForm from './AddItemForm.jsx';

const ItemList = () => {
  const [items, setItems] = useState([]);

  const fetchItems = async () => {
    try {
      const response = await api.get('/items');
      setItems(response.data.items);
    } catch (error) {
      console.error('Error fetching items', error);
    }
  };

  const addItem = async (itemName) => {
    try {
      await api.post('/items', { name: itemName, price: 0, is_offer: false });
      fetchItems();
    } catch (error) {
      console.error('Error adding item', error);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <div>
      <h2>Items List</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item.name}</li>
        ))}
      </ul>
      <AddItemForm addItem={addItem} />
    </div>
  );
};

export default ItemList;
