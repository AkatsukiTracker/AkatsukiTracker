from django.apps import AppConfig

class TrackerConfig(AppConfig):
    name = 'apps.tracker'

    def ready(self):

        from .models import Tienda

        tiendasTxt = open('apps/tracker/tiendas.txt', 'r')
        for linea in tiendasTxt:
            idT, tienda, url = linea.strip().split(';')

            if not Tienda.objects.filter(nombre=tienda):
                instancia_tienda = Tienda(idT, tienda, url)
                instancia_tienda.save()
        tiendasTxt.close()

        print("\nTiendas iniciales cargadas correctamente\n")
        


