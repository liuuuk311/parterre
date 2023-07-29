import requests
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Sets up initial project data & users. Also in production!"""

    help = "Sets up initial project data & users. Also in production!"
    number_of_tenants = 3
    number_of_users_per_tenant = 6
    number_of_customers = 5
    number_of_suppliers = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0
        self.uid = 1

    def setup_development(self):
        self._create_superuser()
        self._setup_tenants()
        self._setup_users()
        self._setup_customers()
        self._setup_suppliers()

    def handle(self, *args, **options):
        """entry point"""
        self.verbosity = options["verbosity"]
        if not settings.DEBUG:
            raise RuntimeError("Command can not be run in production.")

        if self.verbosity > 0:
            self.stdout.write("Setting up sensible development defaults...")
        self.setup_development()

    def _make_user_request(self):
        self.stdout.write(f"Requesting user {self.uid} fake data")
        resp = requests.get(f"https://dummyjson.com/users/{self.uid}")
        if resp.status_code != 200:
            raise RuntimeError(resp.json())

        self.uid += 1
        return resp.json()

    @staticmethod
    def _create_user(data, tenant_id, role):
        User.objects.create_user(
            username=data.get("username"),
            email=data.get("email"),
            password="1234",
            role=role,
            email_verified=True,
            tenant_id=tenant_id,
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
        )

    def _create_tenant(self, data):
        Tenant = apps.get_model("tenants.Tenant")  # noqa
        company = data.get("company", {})
        _tenant, _ = Tenant.objects.get_or_create(
            name=company.get("name"),
            defaults={
                "address": company.get("address", {}).get("address"),
                "city": company.get("address", {}).get("city"),
                "state": company.get("address", {}).get("state"),
                "zip_code": company.get("address", {}).get("postalCode"),
                "phone_number": data.get("phone"),
                "email": data.get("email"),
            },
        )
        self._create_user(data, _tenant.id, User.Role.OWNER)

    def _setup_tenants(self):
        for i in range(self.number_of_tenants):
            user = self._make_user_request()
            self._create_tenant(user)

    def _setup_users(self):
        Tenant = apps.get_model("tenants.Tenant")  # noqa
        for tenant in Tenant.objects.all():
            for i in range(self.number_of_users_per_tenant):
                user = self._make_user_request()
                role = (
                    User.Role.OPERATOR
                    if i / self.number_of_users_per_tenant < 0.7
                    else User.Role.ADMIN
                )
                self._create_user(user, tenant.id, role)

    def _setup_customers(self):
        Tenant = apps.get_model("tenants.Tenant")  # noqa
        for tenant in Tenant.objects.all():
            for i in range(self.number_of_customers):
                data = self._make_user_request()
                Customer = apps.get_model("customers.Customer")  # noqa
                company = data.get("company", {})
                obj = Customer(
                    name=company.get("name"),
                    address=company.get("address", {}).get("address"),
                    city=company.get("address", {}).get("city"),
                    state=company.get("address", {}).get("state"),
                    zip_code=company.get("address", {}).get("postalCode"),
                    phone_number=data.get("phone"),
                    email=data.get("email"),
                    tenant_id=tenant.id,
                )
                obj.save()

    def _setup_suppliers(self):
        Tenant = apps.get_model("tenants.Tenant")  # noqa
        for tenant in Tenant.objects.all():
            for i in range(self.number_of_customers):
                data = self._make_user_request()
                Supplier = apps.get_model("suppliers.Supplier")  # noqa
                company = data.get("company", {})
                obj = Supplier(
                    name=company.get("name"),
                    address=company.get("address", {}).get("address"),
                    city=company.get("address", {}).get("city"),
                    state=company.get("address", {}).get("state"),
                    zip_code=company.get("address", {}).get("postalCode"),
                    phone_number=data.get("phone"),
                    email=data.get("email"),
                    tenant_id=tenant.id,
                )
                obj.save()

    @staticmethod
    def _create_superuser():
        User.objects.create_superuser(
            username="SA_user",
            email="admin@django.com",
            password="1234",
            role=User.Role.OWNER,
            email_verified=True,
        )
