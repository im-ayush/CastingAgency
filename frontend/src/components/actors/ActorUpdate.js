import React, { useEffect, useState } from "react";
import { Redirect} from 'react-router-dom';
import NavBar from '../NavBar.js';
import Error from '../Error.js';
import {API} from '../../backend.js';

const ActorUpdate = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user

	const [error, setError] = useState(false)

	const [state, setState] = useState({
		id: '',
		name: '',
		age: '',
		gender: '',
		movies: ''
	})

	const [isLoaded, setIsLoaded] = useState(false)
	const [isUpdated, setIsUpdated] = useState(false)

	const	handleChange = (event) => {
		const value = event.target.value;
	  setState({
	    ...state,
	    [event.target.name]: value
	  });
	}

	const updateActor = (event) => {
		event.preventDefault();
			fetch(`${API}actors/${props.match.params.id}`, {
        method: 'PATCH',
        headers: {
					Authorization: `Bearer ${accessToken}`,
					'Content-Type': 'application/json'
				},
        body: JSON.stringify(state)
	    })
        .then(response => response.json())
        .then(json => {
					if (json.success){
						setIsUpdated(true)
					}
					else {
						setError(json.message)
					}
					}).catch(e => {
						setError(e.message);
					});
	}

	useEffect(() => {
		document.title = "Actor | Update"
			fetch(`${API}actors/${props.match.params.id}`, {
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			})
			.then(response => response.json())
			.then(json => {
				if (json.success) {
					let movies = "";
					json.movies.map((movie) => (
						movies += movie.id +','
					))

					setState({
						id: json.actor.id,
						name: json.actor.name,
						age: json.actor.age,
						gender: json.actor.gender,
						movies: movies,
					})
					setIsLoaded(true)
			} else{
				setError(json.message)
			}
			}).catch(e => {
				setError(e.message);
			});
}, []);

if (error) {
		return (
			<div>
				<Error errorMsg={error} />
			</div>
		)
}

else if (!isLoaded) {
		return (
			<div>
				<h1>Loading...</h1>
			</div>
		)
	}

	else if (isUpdated) {
		return (
			<Redirect to={{
					pathname:`/actors/${state.id}`,
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
					<button className="btn btn-lg btn-success" onClick={updateActor}>
						Submit
					</button>
				</form>
			</div>
		</div>
		)
	}
}

export default ActorUpdate
