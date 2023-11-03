from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email or self.username

    def __str__(self):
        return f'{self.full_name} ({self.pk})'

