from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from usuario.models import Usuario


@receiver(post_save, sender=Usuario)
def signal_save_usuario_django(sender, instance, created, **kwargs):
    # Cria e atrela o Django User
    """
    The signal_save_usuario_django function is a receiver that listens for the post_save signal from the Usuario model.
    When it receives this signal, it checks to see if a Django User object exists with the same email address as the Usuario
    object's email field. If not, then it creates one and saves its token in an instance of Token associated with that user.
    If there is already a Django User object with that email address, then we just save its token in an instance of Token
    associated with that user.

    Parameters
    ----------
        sender
            Specify the model class
        instance
            Pass the instance of the model that is being saved
        created
            Check if the object is being created or updated
        **kwargs
            Pass a keyworded, variable-length argument list to the function

    Returns
    -------

        The following:

    Doc Author
    ----------
        Trelent
    """
    if created or not instance.django_user:
        try:
            with transaction.atomic():
                if not User.objects.filter(username=instance.email).exists():
                    django_user = User.objects.create_user(
                        instance.email,
                        instance.email,
                        User.objects.make_random_password(length=8),
                    )
                    instance.token = str(Token.objects.create(user=django_user))
                    instance.django_user = django_user
                else:
                    instance.django_user = User.objects.get(username=instance.email)
                instance.save()
        except Exception as error:
            print(f"Erro ao Criar/Atrelar o DjangoUser: {error}")

    # Deleta o Django User
    elif instance.deleted:
        try:
            with transaction.atomic():
                if django_user := User.objects.get(username=instance.email):
                    django_user.is_active = False
                    django_user.save()

        except Exception as error:
            print(f"Erro ao Inativar o DjangoUser: {error}")

    if instance.email and not User.objects.filter(username=instance.email).exists():
            try:
                with transaction.atomic():
                    if django_user := User.objects.filter(pk=instance.django_user.pk).first():
                        django_user.username = instance.email
                        django_user.email = instance.email
                        django_user.save()

            except Exception as error:
                # TODO: SALVAR ERRO NO SENTRY
                print(f"Erro ao atribuir/alterar o username e o email: {error}")
@receiver(post_delete, sender=Usuario)
def signal_delete_usuario_django(sender, instance, **kwargs):
    # Deleta o Django User quando o usuário for deletado
    # apenas se o USE_DEFAULT_MANAGER for True
    try:
        with transaction.atomic():
            if django_user := User.objects.get(username=instance.email):
                django_user.delete()

    except Exception as error:
        print(f"Erro ao Deletar o DjangoUser: {error}")
