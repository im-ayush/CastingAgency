import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import reportWebVitals from './reportWebVitals';
import Routes from './Routes'

import { Auth0Provider } from "@auth0/auth0-react";

ReactDOM.render(
  <Auth0Provider
    domain="auth0trials.us.auth0.com"
    clientId="1WvlHX2yuFYBkpRGgSiUHqNr06aiTlpX"
    redirectUri= {window.location.origin}
    audience="agency"
    scope="get:actors get:movies post:actors post:movies
    patch:actors patch:movies delete:actors delete:movies"
    >
    <Routes />,
    </Auth0Provider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
