import React, { useEffect, useState } from "react";
import {Link} from 'react-router-dom';
import NavBar from '../NavBar.js';
import Error from '../Error.js';
import {API} from '../../backend.js';

const MovieList = (props) => {
	const isAuthenticated = props.location.state.isAuthenticated
	const accessToken = props.location.state.accessToken
	const user = props.location.state.user

	const [error, setError] = useState(false)

	const [items, setItems] = useState('')
	const [isLoaded, setIsLoaded] = useState(false)

	const [pageState, setPageState] = useState({
		pageNo:1,
		maxPages:1
	})

	const getMore  = (event) => {
		setPageState({
			...pageState,
			pageNo:pageState.pageNo + 1
		})
	}

	const getLess  = (event) => {
		setPageState({
			...pageState,
			pageNo:pageState.pageNo - 1
		})
	}

	useEffect(() => {
		document.title = "Movies"
			fetch(`${API}movies?page=${pageState.pageNo}`, {
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			})
			.then(response => response.json())
			.then(json => {
				if (json.success) {
						setItems(json)
						setIsLoaded(true)

						setPageState({
							...pageState,
							maxPages: Math.ceil(json.total_movies/10)
						})
				} else{
					setError(json.message)
				}
			}).catch(e => {
				setError(e.message);
			});
	}, [pageState.pageNo]);

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

	else if (items.success) {
		return (
			<div>
			<NavBar isAuthenticated={isAuthenticated} user={user}/>
			<div className="App container bg-light p-2">
				<h1 className="p-2">{items.total_movies} results found.</h1>
				<Link className="p-2 btn btn-lg btn-primary link-light"
					to={{
						pathname:"/movies/new",
						state:{
							isAuthenticated:isAuthenticated,
							accessToken:accessToken,
							user:user
						}
					}}
					>
					Add a new movie
				</Link>
				{items.movies.map((movie, index) => (
				<div key={index}>
					<br/>
					<Link className="list-group-item list-group-item-action w-25 mx-5"
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

			{
				pageState.pageNo<pageState.maxPages &&
				<button className="btn btn-info link-light" onClick={getMore} >
					Next
				</button>
			}
			{
				pageState.pageNo>1 &&
				<button className="btn btn-info link-light" onClick={getLess} >
					Previous
				</button>
			}
			</div>
		</div>
		)
	}

}

export default MovieList;
