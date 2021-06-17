import './App.css';

import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import Home from './components/Home.js';
import Error from './components/Error.js';
import NavBar from './components/NavBar.js';

import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";


function App() {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [accessToken, setAccessToken]=useState('')

  const [error, setError] = useState(false)

  useEffect(() => {
		const getToken = async () => {
			try {
				const accessToken = await getAccessTokenSilently({
					audience: 'agency',
				});
        setAccessToken(accessToken)
        console.log(accessToken);
		}
		catch (e) {
			console.log(e.message);
      setError(e.message)
		}
	}
	getToken();
});

  return (
    <div>
      <NavBar isAuthenticated={isAuthenticated} user={user}/>

      <div className="App container bg-light mt-5">
        <Home
          user={user}
          accessToken={accessToken}
          isAuthenticated={isAuthenticated}
          />
        {error && <Error errorMsg={error} />}
      </div>
  </div>


  );
}

export default App;
