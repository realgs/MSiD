import React from 'react';
import '../App.css'

const OptionButton = (props) => {
    return(
        <button className="button-option" onClick = {(e) => props.onClick(props)}>
            {props.text}
        </button>
    )
};




export default OptionButton; 