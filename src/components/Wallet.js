import React, {useState} from 'react';
import CurrencyListElem from './CurrencyListElem';
import symbolsArray from '../symbols.json'
import {getMarkets} from '../Api/bittrex'
import {convertList} from '../controllers/currency';
import OptionButton from './OptionButton';
import {save, read} from '../controllers/storage'

const Wallet =  (props) => {

    const [baseCurrency,setBaseCurrency] = useState("BTC");
    const [convertedList,setConvertedList] = useState([]);
    const [resources,setResources] = useState([]);

    const onCovert = async (e) => {
        Promise.all(convertList(resources,await getMarkets(), baseCurrency))
        .then((res) => {
            setConvertedList(res);
          });
    }

    const onAddItem = () => {
        setResources([...resources, {id:resources.length, symbol: "", amount: 0, status: "toEdit"}]);
    }

    const onEditItem = (e) => {
        setResources(
            resources.map(elem => {
              if (elem.id === e.id) {
                if(isNaN(e.amount)) return {...e, amount:0}
                return e;
              } else {
                return elem;
              }
            }))
    }
    const onDeleteItem = (e) => {
        let i=0;
        const arr = resources.filter(elem => elem.id !== e.id);
        setResources(
            arr.map(elem => {
              i++;
            return {...elem, id:i};
              
            }))
    }

    const onClear = () => {
        setResources([]);
        setConvertedList([]);
    }

    const onRefresh = () => {
        const arr = read();
        setResources(arr);
        setConvertedList([]);
    }

    const onSave = () => {
        save(resources);
    }

    const listResources = resources.map((elem)=>
        <li key={elem.id+" "+elem.status} className="list__elem">
            <CurrencyListElem 
                id = {elem.id}
                symbol={elem.symbol} 
                amount={elem.amount} 
                message = {elem.status} 
                onEditItem={(e) => onEditItem(e)}
                onDeleteItem={(e) => onDeleteItem(e)}/>
        </li>)
    
    return(
        <div className="block-exchange">
            <div className="block-options">
                <OptionButton text="Add new" onClick = {(e) => onAddItem(e)}/>
                <OptionButton text="Last saved" onClick =  {(e) => onRefresh(e)}/>
                <OptionButton text="Clear" onClick =  {(e) => onClear(e)}/>
                <OptionButton text="Save" onClick =  {(e) => onSave(e)}/>
            </div>
            <div>
                <label>Currency:</label>
                <select onChange={(e) => setBaseCurrency(e.currentTarget.value)}>
                    {symbolsArray.symbols.map((elem)=>
                        <option key={elem} value={elem}>{elem}</option>)
                    }
                </select>
                <button className="button-convert" onClick={(e) => onCovert(e)}>convert</button>
            </div>
            <div className="block-lists-converter">
                <ul className="list-currency">
                    {listResources}
                </ul> 
                <ul className="list-currency">
                    {convertedList.map((elem)=>
                        <li key={elem.id +"_"+elem.amount} className="list__elem">
                            <CurrencyListElem amount={elem.amount} message={elem.status}/>
                        </li>)
                    }
                </ul> 
            </div>
            
        </div>
    )
};




export default Wallet; 