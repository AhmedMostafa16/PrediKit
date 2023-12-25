import '@mantine/core/styles.css';
import '@mantine/dropzone/styles.css';
import '@mantine/nprogress/styles.css';
import '@mantine/notifications/styles.css';
import './globals.css';
import ReactDOM from 'react-dom/client';
import React from 'react';
import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import App from './App';
import { theme } from './theme';
import { StoreContext, store } from './stores/store';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <StoreContext.Provider value={store}>
      <MantineProvider theme={theme} defaultColorScheme="dark">
        <Notifications />
        <App />
      </MantineProvider>
    </StoreContext.Provider>
  </React.StrictMode>
);
