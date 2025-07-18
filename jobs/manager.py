from ninja.errors import HttpError
from django.db.models import Manager

class JobManager(Manager):

    def create(self, **kwargs):
        user = kwargs.get('user') or kwargs['user']
        
        if user.user_type not in ('company', 'admin'):
            raise HttpError(400, "You don't have permission to create job")
        
        if user.is_deleted:
            raise HttpError(400, "The user has been deleted\nPlease contact the administrator and reactivate your account")
        
        return super().create(**kwargs)

    

class JobCategoryManager(Manager):
    def create(self, **kwargs):
        user = kwargs.get('user') or kwargs['user']
        if user.user_type != 'admin':
            raise HttpError(400, "You don't have permission to create job category")
        if user.is_deleted:
            raise HttpError(400, "The user has been deleted\nPlease contact the administrator and reactivate your account")
        return super().create(**kwargs)