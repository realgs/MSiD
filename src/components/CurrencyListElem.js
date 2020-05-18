import React, {useState} from 'react';
import EditCurrencyForm from './EditCurrencyForm';

const CurrencyListElem = (props) => {

    const elemView =() => {
        if(props.message==="no data") return props.message;
        else if(props.amount===0) return "amount";
        else return Number(Math.round(props.amount + 'e+2') + 'e-2');
    }

    const [view,setView] = useState(elemView());

    
    if(props.message === "resources"){
        return(
            <div>
                <button onClick={(e) => props.onDeleteItem({id: props.id})}>
                delete
                </button>
                <button onClick={(e) => props.onEditItem({id: props.id, symbol: props.symbol, amount: props.amount, status: "toEdit"})}>
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
            <div>
                <span>{props.symbol}</span>
                <span>{view}
                </span>
            </div>)
    }

};




export default CurrencyListElem; 