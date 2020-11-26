function check_url(){

  var url = document.querySelector("#input-url").value
  fetch(`check_url?url=${url}`, {method: "GET"})
    .then( function(response) {
      if (response.status !== 200)  return false;
        response.json().then(function(data) {
          console.log(data)
          document.querySelector("#input-nombre").value = data['data']['nombre']
          document.querySelector("#input-nombreTienda").value = data['data']['tienda']
        }
      );
    })
    .catch(err => false);
}
