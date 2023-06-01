function handleDelete(url, term) {
    $.ajax(url+term, {
        type: "DELETE"
    })
    .then((response) => {
        console.log(response);
        if (url==='') {
            window.location.replace('http://localhost:3000/terms');
        } else {
            window.location.reload();
        }
    })
}

function handleChange(direction) {
    if (direction === 'index') {
        direction = document.getElementById("indexInput").value;
    }

    $.ajax("terms/change/"+direction, {
        type: "GET"
    })
    .then((response) => {
        console.log(response);
        window.location.reload();
    })
}