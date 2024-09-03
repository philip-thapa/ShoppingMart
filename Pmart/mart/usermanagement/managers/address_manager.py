from django.core.exceptions import ValidationError

from usermanagement.models import Address
from usermanagement.user_exceptions import AddressException


class AddressManager:

    def __init__(self, address_id=None):
        if address_id:
            self.address = Address.objects.get(id=address_id)
        else:
            self.address = Address()

    def _update_address_fields(self, data):
        fields = ['full_name', 'phone_number', 'pincode', 'state', 'city', 'address', 'landmark', 'address_type']
        for field in fields:
            setattr(self.address, field, data.get(field, '').strip())

    def add_new_address(self, request):
        data = request.data
        self._update_address_fields(data)
        self.address.user = request.user
        self._save_address()

    def edit_address(self, data):
        self._update_address_fields(data)
        self._save_address()

    def _save_address(self):
        try:
            self.address.save()
        except ValidationError as e:
            raise AddressException(str(e))

    def remove_address(self):
        self.address.isDeleted = True
        self.address.save()

    @staticmethod
    def get_all_address(user):
        addresses = list(Address.objects.filter(user_id=user).values())
        return addresses


