import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import Error from './Error.js';
import {API} from './../backend.js';

const Home = (props) => {
	const isAuthenticated = props.isAuthenticated
	const accessToken = props.accessToken
	const user = props.user

	const [error, setError] = useState(false)

	const [items, setItems] = useState('')
	const [isLoaded, setIsLoaded] = useState(false)

	useEffect(() => {
		document.title = "Home"
			fetch(`${API}`)
			.then(response => response.json())
			.then(json => {
				if (json.success) {
					setItems(json)
					setIsLoaded(true)
				}else{
					console.log(json);
				}
			}).catch(e => {
				setError(e.message);
			});

	},[]);

	if (error) {
			return (
				<div>
					<Error errorMsg={error} />
				</div>
			)
	}

	else if (!isLoaded) {
		return (
			<div className="vertical-center">
				<h1>Loading...</h1>
			</div>
		)
	}

	else if (items.success) {
		return (
			<div>
				<h1 className="p-5">Casting Agency</h1>
					<div className="vertical-center bg-light align-middle">

						<div className="row">
							<div className="col">
								<Link className="btn btn-lg btn-danger"
									to={{
										pathname:"/movies",
										state:{
											isAuthenticated:isAuthenticated,
											accessToken:accessToken,
											user:user
										}
									}}
									>
									Movies
								</Link>
							</div>

							<div className="col">
								<Link className="btn btn-lg btn-danger"
									to={{
										pathname:"/actors",
										state:{
											isAuthenticated:isAuthenticated,
											accessToken:accessToken,
											user:user
										}
									}}
									>
									Actors
								</Link>
							</div>
						</div>

					</div>
					{error && <Error errorMsg={error} />}
			</div>
		)
	}
}

export default Home
