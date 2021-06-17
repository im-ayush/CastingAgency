import React from 'react'

const Error = (props) => {
	return (
		<div style={{
				height:'auto', minWidth:'250px', background:'#ff0000', color:'white',
				display:'inline-block', padding:'2px', border:'double', textAlign:'center'
			}}>
			<h4>{props.errorMsg}</h4>
		</div>
	)
}

export default Error
