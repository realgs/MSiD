import React from 'react';

const CurrencyListElem = (props) => {
    return(
        <div>
            <span>{props.symbol}</span>
            <span>{props.amount}</span>
        </div>
    )
};




export default CurrencyListElem; 