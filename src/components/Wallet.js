import React from 'react';
import CurrencyListElem from './CurrencyListElem';
import currencyArray from '../wallet';
import Options from './Options';
import symbolsArray from '../symbols.json'
import ListButton from './ListButton';

const Wallet = (props) => {

    return(
        <div className="block-exchange">
            <Options/>
            <div>
                <label>Currency:</label>
                <select>
                    {symbolsArray.symbols.map((elem)=>
                        <option value={elem}>{elem}</option>)
                    }
                </select>
            </div>
            <div className="block-lists-converter">
                <ul className="list-currency">
                    {currencyArray.currency.map((elem)=>
                        <li className="list__elem">
                            <ListButton text="delete"/>
                            <ListButton text="edit"/>
                            <CurrencyListElem symbol={elem.symbol} amount={elem.amount}/>
                        </li>)
                    }
                </ul> 
                <ul className="list-currency">
                    {currencyArray.currency.map((elem)=>
                        <li className="list__elem">
                            <CurrencyListElem symbol={elem.symbol} amount={elem.amount}/>
                        </li>)
                    }
                </ul> 
            </div>
            
        </div>
    )
};




export default Wallet; 