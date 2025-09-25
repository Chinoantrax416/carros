from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver 
from cars.models import Car, CarInventory


def car_inventory_update():

    cars_count = Car.objects.all().count() # Vai mostrar todos os carros que está no banco e o count pega conta só os números
    cars_value = Car.objects.aggregate(
        total_value=Sum('value') # O Sum serve para somar os valores totais dos carros que estão no banco de dados 
    )['total_value']
    CarInventory.objects.create( # Criar e registrar no banco de dados os valores da contagem e dos valores dos carros
        cars_count = cars_count,
        cars_value = cars_value
    )

@receiver(pre_save, sender=Car)
def car_pre_save(sender,instance, **kwargs):
    if not instance.bio:
        instance.bio = ' Bio gerada automaticamente!'

   
@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    car_inventory_update()



@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()