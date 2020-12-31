function check_url(){
  let url = document.querySelector("#input-url").value
  url_escaped = encodeURIComponent(url)
  console.log("URL: " + url_escaped)

  if (links.includes(url)){
    existMode()
  }else{
    fetch(`check_url?url=${url_escaped}`, {method: "GET"})
      .then( function(response) {
        if (response.status !== 200)  return errorMode('error');
        response.json().then(function(data) {
          console.log(data)
          uploadMode(data);
          })
        }
      ).catch(err => errorMode(err));
  }
}

function existMode(){
  console.log('exist')

  document.querySelector("#producto-nombre").textContent = "Este producto ya esta en tu lista"
}

function errorMode(error){
  console.error('error: ' + error)

  document.querySelector("#producto-nombre").textContent = "Ocurrio un error, intenta nuevamente"
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

function details(data){

  document.getElementById("modalDetails-delete").hidden = false
  document.getElementById("modalDetails-deleteConfirm").hidden = true
  var not = document.getElementById("modalDetails-deleteNotConfirm")
  not.textContent = "OK"
  not.classList.add('bg-akatsuki')
  not.classList.add('text-white')
  not.classList.remove('btn-outline-secondary')

  document.getElementById("badge-notificaciones-OK").hidden = true
  document.getElementById("badge-notificaciones-NOTOK").hidden = true

  document.getElementById("modalDetails-title").textContent = productos[data].nombre
  document.getElementById("modalDetails-delete").onclick = function(){deleteProduct(productos[data].id)}
  document.getElementById("modalDetails-deleteConfirm").hidden = true
  let check_notificaciones = document.getElementById("check-notificaciones")

  check_notificaciones.setAttribute("onClick", `toggleProductNotification(${productos[data].id})`)

  if (productos[data].notificaciones){
    check_notificaciones.checked = true
  }else{
    check_notificaciones.checked = false
  }

  load_graph();

}

function deleteProduct(id){
  console.log("DELETE: ", id)

  document.getElementById("modalDetails-delete").hidden = true
  confirm = document.getElementById("modalDetails-deleteConfirm")
  confirm.hidden = false
  confirm.href = `/tracker/delete_product/?id=${id}`
  var not = document.getElementById("modalDetails-deleteNotConfirm")
  not.textContent = "Conservar"
  not.classList.remove('bg-akatsuki')
  not.classList.remove('text-white')
  not.classList.add('btn-outline-secondary')
}

function load_graph(data){
  var myLineChart = new Chart(document.getElementById('canvas-chart').getContext('2d'), {
      type: 'line',
       data: {
          datasets: [{
              data: [10, 20, 30, 40, 50, 60]
          }],
          labels: ['January', 'February', 'March', 'April', 'May', 'June']
      },
      options: {}
  });
}

function toggleProductNotification(id){
  console.log(id)

  let formData = new FormData();
  let form = {
    producto: id,
    csrfmiddlewaretoken: csrf
  }

  for (var k in form) formData.append(k, form[k])

  fetch(`/tracker/notif_product`, {method: "POST", body: formData})
  .then( function(response) {
    if (response.status !== 200)  return console.error('error');
    response.json().then(function(data) {
      document.getElementById("badge-notificaciones-OK").hidden = false
      document.getElementById("badge-notificaciones-NOTOK").hidden = true

      productos[id].notificaciones = !productos[id].notificaciones
      })
    }
  ).catch( function(err) {
    console.error(err)
    document.getElementById("badge-notificaciones-OK").hidden = true
    document.getElementById("badge-notificaciones-NOTOK").hidden = false
  });

}
