from django.shortcuts import redirect

# Rutas que NO requieren login
RUTAS_PUBLICAS = [
    '/login/',
    '/registro/',
    '/password-reset/',
    '/password-reset/done/',
    '/password-reset/complete/',
    '/validar-username/',
    '/validar-email/',
    '/admin/',
]

class LoginRequeridoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir rutas públicas y rutas de password reset con token
        es_publica = any(
            request.path.startswith(ruta) for ruta in RUTAS_PUBLICAS
        )

        if not es_publica and not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        return self.get_response(request)