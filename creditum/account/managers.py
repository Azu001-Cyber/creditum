
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        #ensure email is provided
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        # create user object but not saved
        user = self.model( email=email, **extra_fields)

        user.set_password(password) #hash password
        user.save()
        return user
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Add default admin privileges
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')


        # Call create_user() to reuse logic
        return self.create_user(email, password, **extra_fields)