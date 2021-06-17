import React, { useEffect, useState } from "react";
import {Redirect} from 'react-router-dom';
import Error from '../Error.js';
import NavBar from '../NavBar.js';
import {API} from '../../backend.js';

const ActorAdd = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user
	// console.log(accessToken);
	// console.log(isAuthenticated);

	const [error, setError] = useState(false)

	const [state, setState] = useState({
		name: '',
		age: '',
		gender: '',
		movies: ''
	})
	const [isCreated, setIsCreated] = useState(false)

	const	handleChange = (event) => {
		const value = event.target.value;
	  setState({
	    ...state,
	    [event.target.name]: value
	  });
	}

	const addActor = (event) => {
		event.preventDefault();
			fetch(`${API}actors`, {
	        method: 'POST',
	        headers: {
						Authorization: `Bearer ${accessToken}`,
						'Content-Type': 'application/json'
					},
	        body: JSON.stringify(state)
		    })
	        .then(response => response.json())
	        .then(json => {
						if (json.success){
							setIsCreated(true)
					} else{
						setError(json.message)
					}
				}).catch(e => {
					setError(e.message);
				});
		}

	useEffect(() => {
			document.title = "Actor | New"
	}, []);

	if (error) {
			return (
				<div>
					<Error errorMsg={error} />
				</div>
			)
	}

	else if (isCreated) {
				return (
					<Redirect to={{
							pathname:"/actors",
							state:{
								isAuthenticated:isAuthenticated,
								accessToken:accessToken,
								user:user
							}
						}}
					/>
				)
			}

			else {
				return (
					<div>
						<NavBar isAuthenticated={isAuthenticated} user={user}/>
				<div className="App bg-light container">
					<form className="vertical-center">
						<div className="row mb-3">
							<label className="col h2">Name</label>
							<input
								className="col h3"
								type="text"
								name="name"
								value={state.name}
								onChange={handleChange}
								>
							</input>
						</div>
						<div className="row mb-3">
							<label className="col h2">Age</label>
							<input
								className="col h3"
								type="text"
								name="age"
								value={state.age}
								onChange={handleChange}
								>
							</input>
						</div>
						<div className="row mb-3">
							<label className="col h2">Gender</label>
							<input
								className="col h3"
								type="text"
								name="gender"
								value={state.gender}
								onChange={handleChange}
								>
							</input>
						</div>
						<div className="row mb-3">
							<label className="col h2">Movies</label>
							<input
								className="col h3"
								type="text"
								name="movies"
								value={state.movies}
								onChange={handleChange}
								>
							</input>
						</div>
						<button className="btn btn-lg btn-success" onClick={addActor}>
							Submit
						</button>
					</form>
				</div>
			</div>
			);
			}
}

export default ActorAdd
