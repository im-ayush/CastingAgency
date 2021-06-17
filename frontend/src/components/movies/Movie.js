import React, { useEffect, useState } from "react";
import {Link, Redirect} from 'react-router-dom';
import NavBar from '../NavBar.js';
import Error from '../Error.js';
import {API} from '../../backend.js';

const Movie = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user

	const [error, setError] = useState(false)

	const [items, setItems] = useState('')
	const [isLoaded, setIsLoaded] = useState(false)
	const [isDeleted, setIsDeleted] = useState(false)

	const deleteMovie = () => {
				fetch(`${API}movies/${props.match.params.id}`, {
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${accessToken}`,
					}
				})
				.then(response => response.json())
				.then(json => {
					if (json.success){
						setIsLoaded(true)
						setIsDeleted(true)
					} else{
						setError(json.message)
					}
				}).catch(e => {
					setError(e.message);
				});
	}

	useEffect(() => {
		document.title = "Movie | Details"
				fetch(`${API}movies/${props.match.params.id}`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				})
				.then(response => response.json())
				.then(json => {
					if (json.success){
						setItems(json)
						setIsLoaded(true)
					}
					else{
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

	else if (isDeleted) {
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
	}

	else {
		return (
			<div>
			<NavBar isAuthenticated={isAuthenticated} user={user}/>
			<div className="App bg-light container">
				<div className="">
					<div>
						<h1><b>Title:</b> {items.movie.title}</h1>
						<h1><b>Release Date:</b> {items.movie.release_date}</h1>
						<h1>Total artists: {items.total_actors}</h1>

						<br/><br/><br/>
							<div className="" style={{display:'inline-block', width:'30%'}}>
								{items.actors.map((actor, index) => (
								<div
									className="m-2 col list-group-item list-group-item-action"
									key={index}
									>
									<Link to={{
											pathname:`/actors/${actor.id}`,
											state:{
												isAuthenticated:isAuthenticated,
												accessToken:accessToken,
												user:user
											}
										}}
										>
										<h3>{actor['name']}</h3>
									</Link>
								</div>
							))}
							</div>

					</div>
					<div>
						<Link className="m-3 btn btn-lg btn-primary"
							to={{
									pathname:`/movies/update/${items.movie.id}`,
									state:{
										isAuthenticated:isAuthenticated,
										accessToken:accessToken,
										user:user
									}
								}}
							>
							Edit
						</Link>
						<button className="m-3 btn btn-lg btn-danger" onClick={deleteMovie}>
							 Delete
						 </button>
					</div>
				</div>
			</div>
		</div>
		)
	}
}

export default Movie
