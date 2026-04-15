from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from crm.models import Client, Order


class Command(BaseCommand):
    help = 'Fill the database with sample clients and orders.'

    def handle(self, *args, **options):
        if Client.objects.exists() or Order.objects.exists():
            self.stdout.write(self.style.WARNING('Database already contains clients or orders. Seed aborted.'))
            return

        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "admin" does not exist. Create it first.'))
            return

        clients = [
            Client(user=user, name='Иван Иванов', phone='+7 912 345-67-89', email='ivan@example.com'),
            Client(user=user, name='Мария Петрова', phone='+7 900 123-45-67', email='maria@example.com'),
            Client(user=user, name='Сергей Кузнецов', phone='+7 905 987-65-43', email='sergey@example.com'),
        ]
        Client.objects.bulk_create(clients)

        created_clients = list(Client.objects.filter(user=user))

        orders = [
            Order(user=user, client=created_clients[0], total_price=12000.00, status=Order.STATUS_NEW),
            Order(user=user, client=created_clients[0], total_price=4500.50, status=Order.STATUS_IN_PROGRESS),
            Order(user=user, client=created_clients[1], total_price=7800.00, status=Order.STATUS_DONE),
            Order(user=user, client=created_clients[2], total_price=3200.75, status=Order.STATUS_CANCELED),
        ]
        Order.objects.bulk_create(orders)

        self.stdout.write(self.style.SUCCESS('Sample clients and orders created successfully.'))
