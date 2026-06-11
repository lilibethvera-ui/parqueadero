# Importamos todo lo que está en clientes_forms.py (donde moviste el antiguo forms.py)
from .clientes_forms import (
    ClienteForm,
    VehiculoForm,
    EmpresaCorporativaForm,
    ContactoAutorizadoForm,
    VehiculoAutorizadoForm,
    ConvenioEmpresaForm,
    TerminoPagoEmpresaForm,

    ConvenioVigenciaForm,
    TarifaEspecialConvenioForm,
    RestriccionHorariaConvenioForm,
    ConvenioEmpresaLimitesForm,
    # Agrega aquí cualquier otro que falte de tu lista de la imagen
)

# Importamos lo de tarifas
from .tarifas_forms import *

from .usuarios_forms import *