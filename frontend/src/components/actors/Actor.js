import React, { useEffect, useState } from "react";
import {Link, Redirect} from 'react-router-dom';
import Error from '../Error.js';
import NavBar from '../NavBar.js';
import {API} from '../../backend.js';


const Actor = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user

	const [error, setError] = useState(false)

	const [items, setItems] = useState('')
	const [isLoaded, setIsLoaded] = useState(false)
	const [isDeleted, setIsDeleted] = useState(false)

	const deleteActor = () => {
		fetch(`${API}actors/${props.match.params.id}`, {
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
		document.title = "Actor | Details"
				fetch(`${API}actors/${props.match.params.id}`, {
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
			<div className=" App bg-light container">
				<div className="">
					<div>
						<h1><b>Name:</b> {items.actor.name}</h1>
						<h2><b>Gender:</b> {items.actor.gender}</h2>
						<h2><b>Age:</b> {items.actor.age}</h2>

					<br/><br/><br/>
						<h3>Worked in {items.total_movies} movies.</h3><br/>
							<div className="" style={{display:'inline-block', width:'30%'}} >
								{items.movies.map((movie, index) => (
								<div
									className="m-2 col list-group-item list-group-item-action"
									key={index}
									>
									<Link className=""
										to={{
												pathname:`/movies/${movie.id}`,
												state:{
													isAuthenticated:isAuthenticated,
													accessToken:accessToken,
													user:user
												}
											}}
										>
										<h3>{movie['title']}</h3>
									</Link>
								</div>
							))}
					</div>
					</div>

					<div className="">
						<Link className="m-3 btn btn-lg btn-primary"
							to={{
									pathname:`/actors/update/${items.actor.id}`,
									state:{
										isAuthenticated:isAuthenticated,
										accessToken:accessToken,
										user:user
									}
								}}
							>
							Edit
						</Link>
						<button className="m-3 btn btn-lg btn-danger" onClick={deleteActor}>
							Delete
						</button>
					</div>

				</div>
			</div>
		</div>
		)
	}
}

export default Actor
