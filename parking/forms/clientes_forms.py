from django import forms
from ..models import ( 
    Cliente, 
    Vehiculo, 
    EmpresaCorporativa, 
    ContactoAutorizado,
    VehiculoAutorizado,
    ConvenioEmpresa,
    ConvenioVigencia,
    TarifaEspecialConvenio,
    RestriccionHorariaConvenio,
    ConvenioEmpresaLimites,
    TerminoPagoEmpresa,
    TarifaBaseTiempo,
)

#================= CLIENTES ==============
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # OJO: aquí ya NO va "tipo"
        fields = [
            "nombre",
            "apellidos",
            "documento",
            "telefono",
            "email",
            "direccion",
            "ciudad",
            "nombre_empresa",
            "activo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "documento": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "telefono": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "direccion": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "nombre_empresa": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "placa",
            "tipo",
            "activo",
        ]
        widgets = {
            "placa": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "tipo": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class EmpresaCorporativaForm(forms.ModelForm):
    class Meta:
        model = EmpresaCorporativa
        fields = [
            "razon_social",
            "nit",
            "contacto",
            "email",
            "direccion",
            "ciudad",
            "estado",
        ]
        widgets = {
            "razon_social": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "nit": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "contacto": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "telefono": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "direccion": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "estado": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "notas": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 2}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contacto"].required = False

class ContactoAutorizadoForm(forms.ModelForm):
    class Meta:
        model = ContactoAutorizado
        fields = [
            "empresa",
            "nombre",
            "documento",
            "telefono",
            "email",
            "activo",
        ]
        widgets = {
            "empresa": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "nombre": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "documento": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "telefono": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class VehiculoAutorizadoForm(forms.ModelForm):
    class Meta:
        model = VehiculoAutorizado
        fields = ["empresa", "placa", "tipo_vehiculo", "descripcion", "activo"]
        widgets = {
            "empresa": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "placa": forms.TextInput(attrs={
                "class": "form-control form-control-sm placa-input",
                "placeholder": "ABC123",
            }),
            "tipo_vehiculo": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


#================= CONVENIOS ==============
class ConvenioEmpresaForm(forms.ModelForm):
    class Meta:
        model = ConvenioEmpresa
        fields = [
            "empresa",
            "nit",
            "direccion",
            "telefono",
            "email",
            "activo",
        ]
        widgets = {
            "empresa": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Nombre de la empresa aliada",
                }
            ),
            "nit": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "NIT / identificación",
                }
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "activo": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

class ConvenioVigenciaForm(forms.ModelForm):
    class Meta:
        model = ConvenioVigencia
        fields = [
            "empresa_convenio",
            "fecha_inicio",
            "fecha_fin",
            "activo",
            "descripcion",
        ]
        widgets = {
            "empresa_convenio": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "fecha_inicio": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "fecha_fin": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "activo": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "descripcion": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

class TarifaEspecialConvenioForm(forms.ModelForm):
    class Meta:
        model = TarifaEspecialConvenio
        fields = [
            "empresa_convenio",
            "tipo_beneficio",
            "valor_beneficio",
            "consumo_minimo",
            "aplicacion",
            "activo",
        ]
        widgets = {
            "empresa_convenio": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "tipo_beneficio": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "valor_beneficio": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "step": "0.01", "min": "0"}
            ),
            "consumo_minimo": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "step": "0.01", "min": "0"}
            ),
            "aplicacion": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "activo": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

class RestriccionHorariaConvenioForm(forms.ModelForm):
    class Meta:
        model = RestriccionHorariaConvenio
        fields = [
            "empresa_convenio",
            "dia_semana",
            "hora_inicio",
            "hora_fin",
            "activo",
        ]
        widgets = {
            "empresa_convenio": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "dia_semana": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control form-control-sm", "type": "time"}
            ),
            "hora_fin": forms.TimeInput(
                attrs={"class": "form-control form-control-sm", "type": "time"}
            ),
            "activo": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

class ConvenioEmpresaLimitesForm(forms.ModelForm):
    class Meta:
        model = ConvenioEmpresaLimites
        fields = [
            "max_vehiculos_simultaneos",
            "max_ingresos_dia",
            "max_ingresos_mes",
            "max_horas_por_ingreso",
            "permitir_carros",
            "permitir_motos",
            "permitir_bicicletas", 
            "aplica_fines_semana",
            "aplica_festivos",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        number_fields = [
            "max_vehiculos_simultaneos",
            "max_ingresos_dia",
            "max_ingresos_mes",
            "max_horas_por_ingreso",
        ]
        
        for name in number_fields:
            self.fields[name].widget.attrs.update({
                "class": "form-control form-control-sm",
                "min": "0",
            })
            self.fields[name].required = False

        bool_fields = [
            "permitir_carros",
            "permitir_motos",
            "permitir_bicicletas",
            "aplica_fines_semana",
            "aplica_festivos",
        ]
        for name in bool_fields:
            self.fields[name].widget.attrs.update({
                "class": "form-check-input",
            })

class TerminoPagoEmpresaForm(forms.ModelForm):
    class Meta:
        model = TerminoPagoEmpresa
        fields = ["tipo", "dias_credito", "cupo_credito", "dia_corte", "dia_pago", "estado", "notas"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "dias_credito": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 0}),
            "cupo_credito": forms.NumberInput(attrs={"class": "form-control form-control-sm", "step": "0.01"}),
            "dia_corte": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 1, "max": 31}),
            "dia_pago": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 1, "max": 31}),
            "estado": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "notas": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get("tipo")
        dias = cleaned.get("dias_credito") or 0

        if tipo == "CONTADO":
            cleaned["dias_credito"] = 0

        if tipo == "CREDITO" and dias <= 0:
            raise forms.ValidationError("Si es crédito, los días de crédito deben ser mayor a 0.")

        return cleaned