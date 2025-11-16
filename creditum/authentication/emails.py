from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={'uidb64': uid, 'token': token})
    )
    
    send_mail( 
    subject = 'Activate your account',
    message = f'Hi {user.email}, please activate your account by clicking this link: {activation_link}',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False
    )
