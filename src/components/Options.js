import React from 'react';
import OptionButton from './OptionButton';

const Options = (props) => {

    return(
        <div className="block-options">
            <OptionButton text="Add new"/>
            <OptionButton text="Refresh"/>
            <OptionButton text="Clear"/>
            <OptionButton text="Save"/>
        </div>
    )
};




export default Options; 