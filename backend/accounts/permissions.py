from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.role in self.allowed_roles
        )

class IsManager(HasRole):
    allowed_roles = ('MANAGER',)

class IsServer(HasRole):
    allowed_roles = ('SERVER', 'MANAGER')

class IsKitchen(HasRole):
    allowed_roles = ('KITCHEN', 'MANAGER')

class IsDriver(HasRole):
    allowed_roles = ('DRIVER', 'MANAGER')

class IsCustomer(HasRole):
    allowed_roles = ('CUSTOMER',)