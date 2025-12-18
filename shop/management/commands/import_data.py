import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Profile, Category, Manufacturer, Supplier, Product, PickupPoint, Order, OrderItem

class Command(BaseCommand):
    help = 'Imports data from CSV files'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importing data...'))

        with open('Users.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                role_str, full_name, login, password = row
                if role_str == 'Администратор':
                    role = 'admin'
                elif role_str == 'Менеджер':
                    role = 'manager'
                else:
                    role = 'client'
                
                user, created = User.objects.get_or_create(username=login)
                if created:
                    user.set_password(password)
                    user.save()
                
                Profile.objects.get_or_create(user=user, defaults={'full_name': full_name, 'role': role})

        with open('Pickup_poitnts.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                PickupPoint.objects.get_or_create(address=row[0])

        with open('Products.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                sku, name, unit, price, supplier_name, manufacturer_name, category_name, discount, stock, description, photo = row
                
                category, _ = Category.objects.get_or_create(name=category_name)
                manufacturer, _ = Manufacturer.objects.get_or_create(name=manufacturer_name)
                supplier, _ = Supplier.objects.get_or_create(name=supplier_name)

                Product.objects.get_or_create(
                    sku=sku,
                    defaults={
                        'name': name,
                        'unit': unit,
                        'price': price,
                        'supplier': supplier,
                        'manufacturer': manufacturer,
                        'category': category,
                        'discount': discount,
                        'stock': stock,
                        'description': description,
                        'photo': photo,
                    }
                )

        with open('Orders.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                order_number, ordered_items_str, order_date_str, delivery_date_str, pickup_point_id, user_full_name, pickup_code, status_str = row
                
                try:
                    profile = Profile.objects.get(full_name=user_full_name)
                    user = profile.user
                except Profile.DoesNotExist:
                    username = user_full_name.replace(' ', '').lower()
                    user, created = User.objects.get_or_create(username=username)
                    if created:
                        user.set_password('password')
                        user.save()
                    profile, _ = Profile.objects.get_or_create(user=user, defaults={'full_name': user_full_name, 'role': 'client'})

                pickup_point = PickupPoint.objects.get(id=pickup_point_id)
                
                if status_str == 'Завершен':
                    status = 'completed'
                else:
                    status = 'new'
                    
                order_date_parts = order_date_str.split(' ')[0].split('/')
                order_date = f'{order_date_parts[2]}-{order_date_parts[0].zfill(2)}-{order_date_parts[1].zfill(2)}'

                delivery_date_parts = delivery_date_str.split(' ')[0].split('/')
                delivery_date = f'{delivery_date_parts[2]}-{delivery_date_parts[0].zfill(2)}-{delivery_date_parts[1].zfill(2)}'


                order, created = Order.objects.get_or_create(
                    order_number=order_number,
                    defaults={
                        'order_date': order_date,
                        'delivery_date': delivery_date,
                        'pickup_point': pickup_point,
                        'user': user,
                        'pickup_code': pickup_code,
                        'status': status,
                    }
                )

                if created:
                    ordered_items = ordered_items_str.split(', ')
                    i = 0
                    while i < len(ordered_items):
                        sku = ordered_items[i]
                        quantity = ordered_items[i+1]
                        try:
                            product = Product.objects.get(sku=sku)
                            OrderItem.objects.create(order=order, product=product, quantity=quantity)
                        except Product.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Product with SKU {sku} not found.'))
                        i += 2

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
