from django.db.models.manager import Manager
from ninja.errors import HttpError


class ApplicationManager(Manager):
    def create(self, **kwargs):
        user = kwargs.get('user') or kwargs['user']
        if user.is_deleted:
            raise HttpError(400, "The user has been deleted\nPlease contact the administrator and reactivate your account")
        if user.user_type not in ('company', 'admin'):
            raise HttpError(400, "You don't have permission to create application")
        return super().create(**kwargs)