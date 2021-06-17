import React, { useEffect, useState } from "react";
import {Redirect} from 'react-router-dom';
import NavBar from '../NavBar.js';
import Error from '../Error.js';
import {API} from '../../backend.js';

const MovieAdd = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user

	const [error, setError] = useState(false)

	const [state, setState] = useState({
		title: '',
		release_date: '',
		actors: ''
	})
	const [isCreated, setIsCreated] = useState(false)

	const	handleChange = (event) => {
		const value = event.target.value;
	  setState({
	    ...state,
	    [event.target.name]: value
	  });
	}

	const addMovie = (event) => {
		event.preventDefault();
			fetch(`${API}movies`, {
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
			document.title = "Movie | New"
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
							pathname:"/movies",
							state:{
								isAuthenticated:isAuthenticated,
								accessToken:accessToken,
								user:user
							}
						}}
						/>
				)
			} else {
				return (
					<div>
					<NavBar isAuthenticated={isAuthenticated} user={user}/>
					<div className="App bg-light container">
						<form className="vertical-center">
							<div className="row mb-3">
								<label className="col h2">Title</label>
								<input
									className="col h3"
									type="text"
									name="title"
									value={state.title}
									onChange={handleChange}
									>
								</input>
							</div>
							<div className="row mb-3">
								<label className="col h2">Release Date</label>
								<input
									className="col h3"
									type="text"
									name="release_date"
									value={state.release_date}
									onChange={handleChange}
									>
								</input>
							</div>
							<div className="row mb-3">
								<label className="col h2">Actors</label>
								<input
									className="col h3"
									type="text"
									name="actors"
									value={state.actors}
									onChange={handleChange}
									>
								</input>
							</div>
							<button className="btn btn-lg btn-success" onClick={addMovie}>
								Submit
							</button>
						</form>
					</div>
				</div>
				)
			}
}

export default MovieAdd
