import React, { useEffect, useState } from "react";
import {Redirect} from 'react-router-dom';
import NavBar from '../NavBar.js';
import Error from '../Error.js';
import {API} from '../../backend.js';

const MovieUpdate = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user

	const [error, setError] = useState(false)

	const [state, setState] = useState({
		id: '',
		title: '',
		release_date: '',
		actors: ''
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

	const updateMovie = (event) => {
		event.preventDefault();
			fetch(`${API}movies/${props.match.params.id}`, {
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
		document.title = "Movie | Update"
			fetch(`${API}movies/${props.match.params.id}`,{
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			})
			.then(response => response.json())
			.then(json => {
				if (json.success) {
					let actors = "";
					json.actors.map((actor) => (
						actors += actor.id +','
					))

					setState({
						id: json.movie.id,
						title: json.movie.title,
						release_date: json.movie.release_date,
						actors: actors,
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
						pathname:`/movies/${state.id}`,
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
						<button className="btn btn-lg btn-success" onClick={updateMovie}>
							Submit
						</button>
					</form>
				</div>
			</div>
			)
		}
}

export default MovieUpdate
