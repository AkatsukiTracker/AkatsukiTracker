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
  document.getElementById("modalDetails-link").href = productos[data].link
  document.getElementById("modalDetails-delete").onclick = function(){deleteProduct(productos[data].id)}
  document.getElementById("modalDetails-deleteConfirm").hidden = true
  let check_notificaciones = document.getElementById("check-notificaciones")

  check_notificaciones.setAttribute("onClick", `toggleProductNotification(${productos[data].id})`)

  if (productos[data].notificaciones){
    check_notificaciones.checked = true
  }else{
    check_notificaciones.checked = false
  }

  load_graph(productos[data].id);

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

  historiales = {}
  fetch(`/tracker/check_product_info?id=${data}`, {method: "GET"})
  .then( function(response) {
    if (response.status !== 200)  return console.error('error');
    response.json().then(function(data) {
        render_graph(data['historiales'])
      })
    }
  ).catch( function(err) {
    console.error(err)
  });


}
function render_graph(data){
  console.log(data)

  chart = {}
  chart.labels = [];
  chart.datasets = [];

  //Suciedad maxima
  let flag = true

  colores = ['rgba(250,0,0,0.1)', 'rgba(0,0,250,0.1)', 'rgba(0,250,0,0.1)', 'rgba(250,250,0,0.1)']

  for (precio_tipo in data){
    precios = []
    console.log(precio_tipo.replace('_', ' '))
    i = chart.datasets.push({})-1
    dataset = chart.datasets[i]
    dataset.label = capitalizeFirstLetter(precio_tipo.replace('_', ' '))
    dataset.backgroundColor = colores[i]
    console.log(data[precio_tipo])
    for (precio of data[precio_tipo]){
      precios.push(precio[0]);
      if (flag) chart.labels.push(precio[1].split('T')[0])
    }
    flag = false

    dataset.data = precios
  }

  var elem =  document.getElementById('canvas-chart')
  elem.parentNode.removeChild(elem);

  document.getElementById("col-chart").innerHTML = `<canvas id="canvas-chart" width="400" height="200"></canvas>`

  if (chart.labels.length >= 2){
    myLineChart = new Chart(document.getElementById('canvas-chart').getContext('2d'), {
      type: 'line',
      data: chart,
    });
    document.querySelector("#row-sinDatos").hidden = true
    document.querySelector("#row-chart").hidden = false
  }else{
    document.querySelector("#row-sinDatos").hidden = false
    document.querySelector("#row-chart").hidden = true
  }

}
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
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
