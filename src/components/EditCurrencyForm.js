import React, {useState} from 'react';
import symbolsArray from '../symbols.json'

const EditCurrencyForm = (props) => {

    const elemView =() => {
        if(props.amount===0) return "amount";
        else return Number(Math.round(props.amount + 'e+2') + 'e-2');
    }

    const [amount,setAmount] = useState(elemView());
    const [symbol,setSymbol] = useState(symbolsArray.symbols[0]);

    
    return(
        <div>
            <button onClick={(e) => props.onEditItem({id: props.id, symbol: symbol, amount: amount, status: "resources"})}>
                submit
            </button>
            <form>
                <select onChange={(e) => setSymbol(e.currentTarget.value)}>
                    {symbolsArray.symbols.map((elem)=>
                        <option key={elem} value={elem}>{elem}</option>)
                    }
                </select>
                <input 
                    type="text" 
                    defaultValue={amount}
                    onChange={(e) => setAmount(e.currentTarget.value)}
                />
            </form>
        </div>)

};




export default EditCurrencyForm; 