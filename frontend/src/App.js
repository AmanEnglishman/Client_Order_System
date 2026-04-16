import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const CLIENT_STATUSES = ['new', 'in_progress', 'done', 'canceled'];
const initialClientForm = {
  name: '',
  phone: '',
  secondary_phone: '',
  email: '',
  address: '',
  tags: '',
  notes: '',
};

const initialOrderForm = {
  client: '',
  total_price: '',
  status: 'new',
};

function App() {
  const [clients, setClients] = useState([]);
  const [orders, setOrders] = useState([]);
  const [view, setView] = useState('dashboard');
  const [clientForm, setClientForm] = useState(initialClientForm);
  const [orderForm, setOrderForm] = useState(initialOrderForm);
  const [selectedClient, setSelectedClient] = useState(null);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    refreshAll();
  }, []);

  const api = axios.create({
    baseURL: '/',
    withCredentials: true,
  });

  const refreshAll = () => {
    setError(null);
    Promise.all([fetchClients(), fetchOrders()])
      .catch(() => {});
  };

  const fetchClients = async () => {
    try {
      const response = await api.get('/crm/api/clients/');
      setClients(response.data);
      return response.data;
    } catch (err) {
      return handleApiError(err);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await api.get('/crm/api/orders/');
      setOrders(response.data);
      return response.data;
    } catch (err) {
      return handleApiError(err);
    }
  };

  const handleApiError = (err) => {
    if (err.response && (err.response.status === 401 || err.response.status === 403)) {
      setError('Для доступа к данным нужна авторизация. Войдите на /accounts/login/.');
    } else {
      setError('Не удалось загрузить данные. Проверьте сервер или сеть.');
      console.error(err);
    }
    return null;
  };

  const openClientForm = (client = null) => {
    setError(null);
    setMessage(null);
    if (client) {
      setClientForm({
        name: client.name || '',
        phone: client.phone || '',
        secondary_phone: client.secondary_phone || '',
        email: client.email || '',
        address: client.address || '',
        tags: client.tags || '',
        notes: client.notes || '',
      });
      setSelectedClient(client);
    } else {
      setClientForm(initialClientForm);
      setSelectedClient(null);
    }
    setView('client-form');
  };

  const openOrderForm = (order = null) => {
    setError(null);
    setMessage(null);
    if (order) {
      setOrderForm({
        client: order.client || order.client_id || '',
        total_price: order.total_price || '',
        status: order.status || 'new',
      });
      setSelectedOrder(order);
    } else {
      setOrderForm(initialOrderForm);
      setSelectedOrder(null);
    }
    setView('order-form');
  };

  const createClient = async () => {
    try {
      await api.post('/crm/api/clients/', clientForm);
      setMessage('Клиент успешно сохранён.');
      setView('clients');
      refreshAll();
    } catch (err) {
      handleApiError(err);
    }
  };

  const updateClient = async () => {
    try {
      await api.put(`/crm/api/clients/${selectedClient.id}/`, clientForm);
      setMessage('Клиент обновлён.');
      setView('clients');
      refreshAll();
    } catch (err) {
      handleApiError(err);
    }
  };

  const deleteClient = async (client) => {
    if (!window.confirm(`Удалить клиента ${client.name}?`)) {
      return;
    }
    try {
      await api.delete(`/crm/api/clients/${client.id}/`);
      setMessage('Клиент удалён.');
      refreshAll();
    } catch (err) {
      handleApiError(err);
    }
  };

  const createOrder = async () => {
    try {
      const payload = {
        client: orderForm.client,
        total_price: orderForm.total_price,
        status: orderForm.status,
      };
      await api.post('/crm/api/orders/', payload);
      setMessage('Заказ создан.');
      setView('orders');
      refreshAll();
    } catch (err) {
      handleApiError(err);
    }
  };

  const updateOrder = async () => {
    try {
      const payload = {
        client: orderForm.client,
        total_price: orderForm.total_price,
        status: orderForm.status,
      };
      await api.put(`/crm/api/orders/${selectedOrder.id}/`, payload);
      setMessage('Заказ обновлён.');
      setView('orders');
      refreshAll();
    } catch (err) {
      handleApiError(err);
    }
  };

  const deleteOrder = async (order) => {
    if (!window.confirm(`Удалить заказ #${order.id}?`)) {
      return;
    }
    try {
      await api.delete(`/crm/api/orders/${order.id}/`);
      setMessage('Заказ удалён.');
      refreshAll();
    } catch (err) {
      handleApiError(err);
    }
  };

  const renderButtons = () => (
    <div className="App-actions">
      <button type="button" onClick={() => setView('dashboard')}>Главная</button>
      <button type="button" onClick={() => setView('clients')}>Клиенты</button>
      <button type="button" onClick={() => setView('orders')}>Заказы</button>
      <a className="App-link-button" href="/accounts/login/">Войти</a>
    </div>
  );

  const renderDashboard = () => (
    <div className="App-content">
      <section>
        <h2>Клиенты</h2>
        <p>Всего клиентов: <strong>{clients.length}</strong></p>
        <button type="button" onClick={() => setView('clients')}>Посмотреть клиентов</button>
      </section>
      <section>
        <h2>Заказы</h2>
        <p>Всего заказов: <strong>{orders.length}</strong></p>
        <button type="button" onClick={() => setView('orders')}>Посмотреть заказы</button>
      </section>
    </div>
  );

  const renderClients = () => (
    <section>
      <div className="App-section-header">
        <h2>Клиенты</h2>
        <button type="button" onClick={() => openClientForm()}>Добавить клиента</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Имя</th>
            <th>Телефон</th>
            <th>Email</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {clients.map(client => (
            <tr key={client.id}>
              <td>{client.name}</td>
              <td>{client.phone}</td>
              <td>{client.email || '-'}</td>
              <td>
                <button type="button" onClick={() => openClientForm(client)}>Редактировать</button>
                <button type="button" className="danger" onClick={() => deleteClient(client)}>Удалить</button>
              </td>
            </tr>
          ))}
          {clients.length === 0 && (
            <tr>
              <td colSpan="4">Нет клиентов.</td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  );

  const renderOrders = () => (
    <section>
      <div className="App-section-header">
        <h2>Заказы</h2>
        <button type="button" onClick={() => openOrderForm()}>Добавить заказ</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Клиент</th>
            <th>Сумма</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.client_name || order.client}</td>
              <td>{order.total_price}</td>
              <td>{order.status}</td>
              <td>
                <button type="button" onClick={() => openOrderForm(order)}>Редактировать</button>
                <button type="button" className="danger" onClick={() => deleteOrder(order)}>Удалить</button>
              </td>
            </tr>
          ))}
          {orders.length === 0 && (
            <tr>
              <td colSpan="5">Нет заказов.</td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  );

  const renderClientForm = () => (
    <section>
      <div className="App-section-header">
        <h2>{selectedClient ? 'Редактировать клиента' : 'Создать клиента'}</h2>
      </div>
      <form className="App-form" onSubmit={(event) => {
        event.preventDefault();
        selectedClient ? updateClient() : createClient();
      }}>
        <label>
          Имя
          <input value={clientForm.name} onChange={(e) => setClientForm({...clientForm, name: e.target.value})} required />
        </label>
        <label>
          Телефон
          <input value={clientForm.phone} onChange={(e) => setClientForm({...clientForm, phone: e.target.value})} required />
        </label>
        <label>
          Второй телефон
          <input value={clientForm.secondary_phone} onChange={(e) => setClientForm({...clientForm, secondary_phone: e.target.value})} />
        </label>
        <label>
          Email
          <input value={clientForm.email} onChange={(e) => setClientForm({...clientForm, email: e.target.value})} />
        </label>
        <label>
          Адрес
          <textarea value={clientForm.address} onChange={(e) => setClientForm({...clientForm, address: e.target.value})} />
        </label>
        <label>
          Теги (через запятую)
          <input value={clientForm.tags} onChange={(e) => setClientForm({...clientForm, tags: e.target.value})} />
        </label>
        <label>
          Примечания
          <textarea value={clientForm.notes} onChange={(e) => setClientForm({...clientForm, notes: e.target.value})} />
        </label>
        <div className="App-form-actions">
          <button type="submit">Сохранить</button>
          <button type="button" className="secondary" onClick={() => setView('clients')}>Отмена</button>
        </div>
      </form>
    </section>
  );

  const renderOrderForm = () => (
    <section>
      <div className="App-section-header">
        <h2>{selectedOrder ? 'Редактировать заказ' : 'Создать заказ'}</h2>
      </div>
      <form className="App-form" onSubmit={(event) => {
        event.preventDefault();
        selectedOrder ? updateOrder() : createOrder();
      }}>
        <label>
          Клиент
          <select value={orderForm.client} onChange={(e) => setOrderForm({...orderForm, client: e.target.value})} required>
            <option value="">Выберите клиента</option>
            {clients.map(client => (
              <option key={client.id} value={client.id}>{client.name}</option>
            ))}
          </select>
        </label>
        <label>
          Сумма
          <input type="number" step="0.01" value={orderForm.total_price} onChange={(e) => setOrderForm({...orderForm, total_price: e.target.value})} required />
        </label>
        <label>
          Статус
          <select value={orderForm.status} onChange={(e) => setOrderForm({...orderForm, status: e.target.value})}>
            {CLIENT_STATUSES.map(status => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </label>
        <div className="App-form-actions">
          <button type="submit">Сохранить</button>
          <button type="button" className="secondary" onClick={() => setView('orders')}>Отмена</button>
        </div>
      </form>
    </section>
  );

  return (
    <div className="App">
      <header className="App-header">
        <h1>Client Order System</h1>
        {renderButtons()}
      </header>

      {message && <div className="App-message">{message}</div>}
      {error && <div className="App-error"><p>{error}</p></div>}

      {view === 'dashboard' && renderDashboard()}
      {view === 'clients' && renderClients()}
      {view === 'client-form' && renderClientForm()}
      {view === 'orders' && renderOrders()}
      {view === 'order-form' && renderOrderForm()}
    </div>
  );
}

export default App;
