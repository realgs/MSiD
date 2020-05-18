import React from 'react';

const OptionButton = (props) => {
    return(
        <button onClick = {(e) => props.onClick(props)}>
            {props.text}
        </button>
    )
};




export default OptionButton; 