from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives


# Класс для сохранения зарегистрированных пользователей в группу common_users
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        common_users = Group.objects.get(name="common_users")
        user.groups.add(common_users)

        # subject - тема письма
        subject = "Добро пожаловать!",
        # текст письма
        text = f"<b>{user.username}вы успешно зарегистрировались на нашем новостном портале, поздравляем!"
        html = (
            f'<b>{user.username}</b> вы успешно зарегистрировались на '
            f'<a href=http://127.0.0.1:8000/posts/>нашем новостном портале</a>, поздравляем!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user
