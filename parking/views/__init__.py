#parking/views/__init__.py

# IMPORTANTE: Importamos todo lo de dashboard_views para que urls.py lo encuentre
from .dashboard_views import *

# Importamos el resto de módulos
# (Asegúrate de que estos archivos existan en la carpeta views)
from .usuarios_views import *
from .clientes_views import *
from .tarifas_views import *
from .convenios_views import *
