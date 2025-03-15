import random
import faker
from blog.models import Car, DriverLicence, CarOwner, Ownership, User

def add_models(n, m):
    brands = ['brand1', 'brand2', 'brand3', 'brand4', 'brand5', 'brand6']
    models = ['model1', 'model2', 'model3', 'model4', 'model5', 'model6']
    colors = ['red', 'blue', 'brown', 'black', 'white', 'grey']
    fnames = ['oleg', 'sergey', 'dima', 'lyoha', 'vitek']
    lnames = ['l_name1', 'l_name2', 'l_name3', 'l_name4', 'l_name5', 'l_name6']

    id = int(Car.objects.last().id)
    owners = []
    cars = []
    for _ in range(n):
        id += 1
        brand = random.choice(brands)
        model = random.choice(models)
        color = random.choice(colors)
        number = random.randint(10**8, 10**9 - 1)
        car = Car.objects.create(gov_number=str(number), brand=brand, model=model, color=color)
        cars.append(car)
    id = int(CarOwner.objects.last().id)
    for _ in range(m):
        id += 1
        date = f'{random.randint(1990, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}'
        f_name = random.choice(fnames)
        l_name = random.choice(lnames)
        
        user = User.objects.create(name=f'{id}', passport_number=id, address='address', username=f'{id}')
        owner = CarOwner.objects.create(first_name=f_name, last_name=l_name, user=user)
        license = DriverLicence.objects.create(owner_id=owner, licence_number=f'{id}', type='ABC', date_of_issue=date)
        owners.append(owner)
    
    for owner in owners:
        ownership_count = random.randint(1, 3)
        for _ in range(ownership_count):
            car = random.choice(cars)
            date = f'{random.randint(2006, 2020)}-{random.randint(1, 12)}-{random.randint(1, 28)}'
            ownership = Ownership.objects.create(owner=owner, car=car, date_of_start=date)
    