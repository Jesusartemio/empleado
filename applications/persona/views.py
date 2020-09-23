from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
    )
    # Models
from .models import Empleado
# Forms
from .forms import EmpleadoForm


class InicioView(TemplateView):
    template_name = "inicio.html"


class ListAllEmpleados(ListView):
    template_name = "persona/list_all.html"
    paginate_by = 10
    ordering = 'first_name'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword",'')
        lista = Empleado.objects.filter(
            full_name__icontains=palabra_clave
        )
        return lista


class ListaEmpleadosAdmin(ListView):
    template_name = "persona/lista_empleados.html"
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'
    model = Empleado


class ListByAreaEmpleado(ListView):
    template_name = "persona/list_by_area.html"
    context_object_name = "empleados"

    def get_queryset(self):
        area = self.kwargs['shortname']
        lista = Empleado.objects.filter(
            departamento__short_name=area
        )
        return lista
    

class ListEmpleadosByKword(ListView):
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('********************')
        palabra_clave = self.request.GET.get("kword",'')
        print('=========', palabra_clave)
        lista = Empleado.objects.filter(
            first_name=palabra_clave
        )
        print('lista resultado:', lista)
        return lista

class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        empleado = Empleado.objects.get(id=2)
        print(empleado.habilidades.all())
        return empleado.habilidades.all()


class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/detail_empleado.html"

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        context["titulo"] = 'empleado del mes'
        return context



class SuccessView(TemplateView):
    template_name = "persona/success.html"


class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = "persona/add.html"
    # fields = ( '__all__' )
    # fields = [
    #     'first_name', 
    #     'last_name', 
    #     'job',
    #     'departamento',
    #     'habilidades',
    #     'avatar',
    # ]
    form_class = EmpleadoForm
    # success_url = '.'
    # success_url = '/success'
    success_url = reverse_lazy('persona_app:empleados_admin')

    def form_valid(self, form):
        # Logica de proceso
        empleado = form.save(commit=False)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = "persona/update.html"
    fields = [
        'first_name', 
        'last_name', 
        'job',
        'departamento',
        'habilidades',
    ]
    success_url = reverse_lazy('persona_app:empleados_admin')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('******* Metodo POST **********')
        print('============ request.POST ===============')
        print(request.POST)
        print('============ request.POST[last_name] ===============')
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Logica de proceso
        print('******* Metodo Form Valid **********')
        print('====================================')
        return super(EmpleadoUpdateView, self).form_valid(form)



class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "persona/delete.html"
    success_url = reverse_lazy('persona_app:empleados_admin')