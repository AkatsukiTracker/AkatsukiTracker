window.addEventListener('load', function() {
  var forms = document.getElementsByClassName('needs-validation');

  var validation = Array.prototype.filter.call(forms, function(form) {
    form.addEventListener('submit', function(event) {
      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
}, false);


check_trending = document.getElementById("check-trending")
check_trending.addEventListener('change', function (e) {
  let formData = new FormData();
  let form = {
    csrfmiddlewaretoken: csrf
  }

  for (var k in form) formData.append(k, form[k])

  fetch(`/tracker/notif_trending`, {method: "POST", body: formData})
  .then( function(response) {
    if (response.status !== 200)  return console.error('error');
    response.json().then(function(data) {
      document.getElementById("badge-notificaciones-OK").hidden = false
      document.getElementById("badge-notificaciones-NOTOK").hidden = true

      })
    }
  ).catch( function(err) {
    console.error(err)
    document.getElementById("badge-notificaciones-OK").hidden = true
    document.getElementById("badge-notificaciones-NOTOK").hidden = false
  });
})

check_oferta = document.getElementById("check-oferta")
check_oferta.addEventListener('change', function (e) {
  let formData = new FormData();
  let form = {
    csrfmiddlewaretoken: csrf
  }

  for (var k in form) formData.append(k, form[k])

  fetch(`/tracker/notif_product_all`, {method: "POST", body: formData})
  .then( function(response) {
    if (response.status !== 200)  return console.error('error');
    response.json().then(function(data) {
      document.getElementById("badge-notificaciones-OK").hidden = false
      document.getElementById("badge-notificaciones-NOTOK").hidden = true

      })
    }
  ).catch( function(err) {
    console.error(err)
    document.getElementById("badge-notificaciones-OK").hidden = true
    document.getElementById("badge-notificaciones-NOTOK").hidden = false
  });
})

