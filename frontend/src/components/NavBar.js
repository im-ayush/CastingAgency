import React from 'react'
import {Link} from 'react-router-dom'
import LoginButton from './LoginButton.js';
import LogoutButton from './LogoutButton.js';

const NavBar = (props) => {
	return (
			<div style={{margin:'50px', marginTop:'10px'}}>
				<div style={{display:'inline-block'}}>
					<Link className="btn btn-outline-primary" to="/">Home</Link>
				</div>

				<div style={{
						display:'inline-block',
						float:'right',
						textAlign:'-webkit-right'
					}}
					>
					{!props.isAuthenticated && <LoginButton/>}
					{props.isAuthenticated && (
						<div>
							<h4>{props.user.nickname}</h4>
							<LogoutButton />
						</div>
					)}
				</div>
			</div>
	)
}

export default NavBar
