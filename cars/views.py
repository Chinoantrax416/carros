from django.shortcuts import render,redirect
from cars.models import Car
from cars.forms import CarModelForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

def cars_view(request):# Antiga função antes da classe
    cars= Car.objects.all().order_by('model') # Buscar tudo que estiver na tabela 
    search = request.GET.get('search') # Busca oque o usuário quer procurar 
    
    #Esse __contains serve para não precisar digitar o nome todo do que vai buscar 
    if search:
        cars = Car.objects.filter(model__icontains= search) #Filtra pelos modelos

    

    return render(request,
                  'cars.html',
                  {'cars': cars}
                  )


class CarsView(View): # Noca classe que fica no lugar da função

    def get(self,request):
        cars= Car.objects.all().order_by('model') 
        search = request.GET.get('search') 
    
        if search:
            cars = Car.objects.filter(model__icontains= search) 

    

        return render(request,
                  'cars.html',
                  {'cars': cars}
                  )
    


class CarListView(ListView): # Django já entende que é get, só precisa colocar os parametros que quer usar 
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search)
        return cars



def new_car_view(request):# Antiga Função antes da classe basedview
    if request.method == 'POST':# Se o usúario clicar em cadastar cai aqui
        new_car_form = CarModelForm(request.POST, request.FILES )#recebe os dados que o usúario digitou 
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')
    
    else:
        new_car_form = CarModelForm()
    return render (request, 'new_car.html', {'new_car_form': new_car_form})




class NewCarView(View): # Nova class para inserir carros

    def get(self,request):
         new_car_form = CarModelForm()
         return render (request, 'new_car.html', {'new_car_form': new_car_form})

    def post(self,request):
         new_car_form = CarModelForm(request.POST, request.FILES )
         if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')
         return render (request, 'new_car.html', {'new_car_form': new_car_form})
    

@method_decorator(login_required(login_url='login'), name='dispatch') # Não consegue acessar enquanto não estiver logado, volta para a pagina de login por conta do (login_url)
class NewCarCreateView(CreateView): # Nova view 
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'


# Detail view (Serve para ver detalhes das fotos dos carros)

class CarDetailView(DetailView): 
    model = Car
    template_name = 'car_detail.html'



# UpdateView (Serve para editar ou fazer atualizações)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk' : self.object.pk}) # Serve para poder depois de fazer alguma alteração voltar para os "Detalhes"

# DeleteView (Serve para deletar )
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'
    