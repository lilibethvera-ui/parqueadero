# parking/forms_tarifas.py
from django import forms
from ..models import (
    TarifaBaseTiempo,
    TarifaBaseDiaria,
    TarifaBaseNocturna,
)

class TarifaBaseTiempoForm(forms.ModelForm):
    class Meta:
        model = TarifaBaseTiempo
        fields = [
            "nombre", "modo", "minimo_minutos", "redondeo",
            "precio_hora", "tamano_fraccion_min", "precio_fraccion",
            "activo", "tipo_vehiculo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "modo": forms.Select(attrs={"class": "form-select", "id": "id_modo"}),
            "minimo_minutos": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "redondeo": forms.Select(attrs={"class": "form-select"}),
            "precio_hora": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "tamano_fraccion_min": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "precio_fraccion": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "tipo_vehiculo": forms.Select(attrs={"class":"form-select"}),
        }

    def clean(self):
        cleaned = super().clean()
        modo = cleaned.get("modo")

        precio_hora = cleaned.get("precio_hora")
        tam = cleaned.get("tamano_fraccion_min")
        precio_frac = cleaned.get("precio_fraccion")

        if modo == TarifaBaseTiempo.Modo.HORA:
            if precio_hora is None:
                self.add_error("precio_hora", "Requerido en modo Hora.")
            cleaned["tamano_fraccion_min"] = None
            cleaned["precio_fraccion"] = None

        elif modo == TarifaBaseTiempo.Modo.FRACCION:
            if tam is None:
                self.add_error("tamano_fraccion_min", "Requerido en modo Fracción.")
            if precio_frac is None:
                self.add_error("precio_fraccion", "Requerido en modo Fracción.")
            cleaned["precio_hora"] = None

        return cleaned

class TarifaBaseDiariaForm(forms.ModelForm):
    class Meta:
        model = TarifaBaseDiaria
        fields = [ "tipo_vehiculo", "modo_diaria", "hora_corte", "precio_dia", "activo"]
        widgets = {
            #"nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_vehiculo": forms.Select(attrs={"class": "form-select"}),
            "modo_diaria": forms.Select(attrs={"class": "form-select"}),
            "hora_corte": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "precio_dia": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

class TarifaBaseNocturnaForm(forms.ModelForm):
    class Meta:
        model = TarifaBaseNocturna
        fields = [
            "nombre", "tipo_vehiculo",
            "hora_inicio", "hora_fin",
            "modo", "minimo_minutos", "redondeo",
            "precio_hora", "tamano_fraccion_min", "precio_fraccion",
            "activo"
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_vehiculo": forms.Select(attrs={"class": "form-select"}),
            "hora_inicio": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "hora_fin": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),

            "modo": forms.Select(attrs={"class": "form-select"}),
            #"minimo_minutos": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            #"redondeo": forms.Select(attrs={"class": "form-select"}),

            "precio_hora": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            #"tamano_fraccion_min": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "precio_fraccion": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }