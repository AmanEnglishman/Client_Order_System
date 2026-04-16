import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [clients, setClients] = useState([]);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    // Для аутентификации нужно токен, но пока без него
    axios.get('http://127.0.0.1:8000/crm/api/clients/')
      .then(response => setClients(response.data))
      .catch(error => console.error(error));

    axios.get('http://127.0.0.1:8000/crm/api/orders/')
      .then(response => setOrders(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="App">
      <h1>Client Order System - React UI</h1>
      <div>
        <h2>Clients</h2>
        <ul>
          {clients.map(client => (
            <li key={client.id}>{client.name} - {client.phone}</li>
          ))}
        </ul>
      </div>
      <div>
        <h2>Orders</h2>
        <ul>
          {orders.map(order => (
            <li key={order.id}>{order.client} - ${order.total_price}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
