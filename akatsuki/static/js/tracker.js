function check_url(){
  var url = document.querySelector("#input-url").value
  fetch(`check_url?url=${url}`, {method: "GET"})
    .then( function(response) {
      if (response.status !== 200)  return false;
      response.json().then(function(data) {
        console.log(data)
        uploadMode(data);
        })
      }
    ).catch(err => false);
}

function editMode(){
  console.log('edit')
  btn_checkUrl = document.querySelector("#btn-checkUrl")
  btn_submitUrl = document.querySelector("#btn-submitUrl")

  btn_checkUrl.textContent = "Comprobar";
  btn_checkUrl.classList.remove("mdi-pencil");
  btn_checkUrl.classList.add("mdi-check");
  btn_checkUrl.onclick = check_url;

  btn_submitUrl.disabled = true

  document.querySelector("#input-datos").value = ""
  document.querySelector("#producto-nombre").textContent = ""

  document.querySelector("#input-url").disabled = false

}
function uploadMode(data){
  console.log('upload')
  btn_checkUrl = document.querySelector("#btn-checkUrl")
  btn_submitUrl = document.querySelector("#btn-submitUrl")

  btn_checkUrl.textContent = "Editar"
  btn_checkUrl.classList.remove("mdi-check")
  btn_checkUrl.classList.add("mdi-pencil")
  btn_checkUrl.onclick = editMode;

  btn_submitUrl.disabled = false

  document.querySelector("#input-datos").value = JSON.stringify(data['data'])
  document.querySelector("#producto-nombre").textContent = data['data']['nombre']

  document.querySelector("#input-url").disabled = true

}
