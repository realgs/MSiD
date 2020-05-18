function save(list) {
    
	localStorage.setItem(
		"currency",JSON.stringify(list)
    );
}

function read() {	
    const list = localStorage.getItem("currency");
    
    return JSON.parse(list);
}

export {save, read}