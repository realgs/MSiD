import React from 'react';
import EditCurrencyForm from './EditCurrencyForm';

const CurrencyListElem = (props) => {

    const elemView =() => {
        if(props.message==="no data") return props.message;
        else return Number(Math.round(props.amount + 'e+2') + 'e-2');
    }

    const view = elemView();

    
    if(props.message === "resources"){
        return(
            <div className='list__elem'>
                <button className='button-list' onClick={(e) => props.onDeleteItem({id: props.id})}>
                delete
                </button>
                <button className='button-list' onClick={(e) => props.onEditItem({id: props.id, symbol: props.symbol, amount: props.amount, status: "toEdit"})}>
                edit
                </button>
                <span>{props.symbol}</span>
                <span>{view}
                </span>
            </div>)
    } else if (props.message === "toEdit"){
        return(
            <EditCurrencyForm
                id={props.id}
                symbol={props.symbol} 
                amount={props.amount} 
                message = {props.status} 
                onEditItem={props.onEditItem}
            />)
    } else {
        return(
            <div className='list__elem'>
                <span>{props.symbol}</span>
                <span>{view}
                </span>
            </div>)
    }

};




export default CurrencyListElem; 