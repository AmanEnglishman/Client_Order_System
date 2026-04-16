import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [clients, setClients] = useState([]);
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.defaults.withCredentials = true;

    const fetchClients = axios.get('/crm/api/clients/');
    const fetchOrders = axios.get('/crm/api/orders/');

    Promise.all([fetchClients, fetchOrders])
      .then(([clientsResponse, ordersResponse]) => {
        setClients(clientsResponse.data);
        setOrders(ordersResponse.data);
      })
      .catch(err => {
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          setError('Для доступа к данным нужна авторизация. Войдите через /accounts/login/.');
        } else {
          setError('Не удалось загрузить данные. Проверьте сервер или сеть.');
          console.error(err);
        }
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Client Order System</h1>
      </header>

      {error ? (
        <div className="App-error">
          <p>{error}</p>
          <p>
            <a href="/accounts/login/">Войти в систему</a>
          </p>
        </div>
      ) : (
        <div className="App-content">
          <section>
            <h2>Clients</h2>
            <ul>
              {clients.length === 0 ? (
                <li>Нет клиентов для отображения.</li>
              ) : (
                clients.map(client => (
                  <li key={client.id}>{client.name} — {client.phone}</li>
                ))
              )}
            </ul>
          </section>

          <section>
            <h2>Orders</h2>
            <ul>
              {orders.length === 0 ? (
                <li>Нет заказов для отображения.</li>
              ) : (
                orders.map(order => (
                  <li key={order.id}>Order #{order.id}: {order.client} — ${order.total_price}</li>
                ))
              )}
            </ul>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;
