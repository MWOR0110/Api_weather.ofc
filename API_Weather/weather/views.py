# views.py
from datetime import datetime
from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from .forms import WeatherForm
from .repositories import WeatherRepository
from .serializers import WeatherSerializer
from .exceptions import WeatherException

class WeatherView(View):

    authentication_classes = [JWTAuthentication]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
        except Exception as e:
            pass

        # Continua a execução da classe, indo para o método correspondente
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.getAll())
            serializer = WeatherSerializer(data=weathers, many=True)
            if serializer.is_valid():
                modelWeather = serializer.save()
                objectReturn = {"weathers": modelWeather}
            else:
                objectReturn = {"error": serializer.errors}

        except WeatherException as e:
            objectReturn = {"error": e.message}

        if not request.user:
            objectReturn["errorAuth"] = "Usuário Não Autenticado"

        return render(request, "home.html", objectReturn)


class WeatherGenerate(View):
    def get(self, request):
        form = WeatherForm()
        return render(request, "weather_generate.html", {'form': form})

    def post(self, request):
        form = WeatherForm(request.POST)
        if form.is_valid():
            repository = WeatherRepository(collectionName='weathers')
            weather_data = {
                'temperature': form.cleaned_data['temperature'],
                'date': form.cleaned_data['date'],
                'city': form.cleaned_data['city'],
                'atmosphericPressure': form.cleaned_data['atmosphericPressure'],
                'humidity': form.cleaned_data['humidity'],
                'weather': form.cleaned_data['weather'],
            }
            serializer = WeatherSerializer(data=weather_data)
            if serializer.is_valid():
                repository.insert(serializer.validated_data)
                return redirect('Weather View')
            else:
                errors = serializer.errors
                return HttpResponse(f"Erros de validação: {errors}", status=400)
        return render(request, "weather_generate.html", {'form': form})
    
class WeatherReset(View):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authenticate = True
        except Exception as e:
            redirect('Weather View')

        #continua a execução da classe, indo para o método correspondente
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()
    
class WeatherEdit(View):
    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getByID(id)
        weatherForm = WeatherForm(initial=weather)

        return render(request, "weather_edit.html", {"form":weatherForm, "id":id})
    
    def post(self, request, id):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            serializer.id = id
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.update(serializer.data, id)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')


class WeatherDelete(View):
    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteByID(id)
        return redirect('Weather View')
    
class WeatherFilter(View):
    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
    
        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.get(data))
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                objectReturn = {"error":serializer.errors}
            
        except WeatherException as e:
            objectReturn = {"error":e.message}

        return render(request, "home.html", objectReturn)