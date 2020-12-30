function add_product(producto,url) {
  let url_escaped = encodeURIComponent(url)
  let producto_enabled = document.querySelector(`#btn-product-${producto}-enabled`)
  let producto_disabled = document.querySelector(`#btn-product-${producto}-disabled`)
  let producto_loading = document.querySelector(`#btn-product-${producto}-loading`)

  console.log("URL: " + url_escaped)

  producto_enabled.hidden = true
  producto_loading.hidden = false
  producto_disabled.hidden = true

  fetch(`/tracker/check_url?url=${url_escaped}`, {method: "GET"})
    .then( function(response) {
      if (response.status !== 200)  return console.error('OKNT');
      response.json().then(function(data) {
        console.log(data)
        var formData = new FormData();
        let form = {
          datos: JSON.stringify(data['data']),
          url: url,
          csrfmiddlewaretoken: csrf
        }

        for (var k in form) formData.append(k, form[k])

        fetch(`/tracker/add_product/`, {method: "POST", body: formData})
          .then( function(response) {
            if (response.status !== 200)  return console.error('OKNT');
            console.log('OK')

            producto_enabled.hidden = true
            producto_loading.hidden = true
            producto_disabled.hidden = false

          })

        })
      }
    ).catch(err => errorMode(err));

}
