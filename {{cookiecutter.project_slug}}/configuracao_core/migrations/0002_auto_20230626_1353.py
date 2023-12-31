# Generated by Django 3.2.19 on 2023-06-26 16:53

import core.utils
import core.validators.file_max_size
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemGenerica',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=True, verbose_name='Ativo')),
                ('deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('imagem', models.ImageField(upload_to=core.utils.save_file_to, validators=[core.validators.file_max_size.FileMaxSizeValidator(1)], verbose_name='Imagem')),
            ],
            options={
                'verbose_name': 'Imagem Genérica',
                'verbose_name_plural': 'Imagens Genéricas',
                'db_table': 'configuracao_imagem_generica',
            },
        ),
        migrations.CreateModel(
            name='RedeSocial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=True, verbose_name='Ativo')),
                ('deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('link', models.CharField(max_length=100, verbose_name='Link')),
                ('icone', models.CharField(help_text="Ícones aqui: <a href='https://fontawesome.com/v5/search?o=r&m=free' target='_blank'>Font Awesome</a>", max_length=100, verbose_name='Ícone')),
            ],
            options={
                'verbose_name': 'Rede Social',
                'verbose_name_plural': 'Redes Sociais',
                'db_table': 'configuracao_rede_social',
            },
        ),
        migrations.AlterField(
            model_name='gestor',
            name='assinatura',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.save_file_to, validators=[core.validators.file_max_size.FileMaxSizeValidator()], verbose_name='Assinatura'),
        ),
        migrations.AlterField(
            model_name='imagemlogin',
            name='imagem',
            field=models.ImageField(upload_to=core.utils.save_file_to, validators=[core.validators.file_max_size.FileMaxSizeValidator(2)], verbose_name='Imagem de login'),
        ),
        migrations.AlterField(
            model_name='logosistema',
            name='imagem',
            field=models.ImageField(upload_to=core.utils.save_file_to, validators=[core.validators.file_max_size.FileMaxSizeValidator(0.5)], verbose_name='Logo do Sistema'),
        ),
        migrations.CreateModel(
            name='ImagensSistema',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=True, verbose_name='Ativo')),
                ('deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('favicon', models.ImageField(upload_to=core.utils.save_file_to, validators=[core.validators.file_max_size.FileMaxSizeValidator(0.5)], verbose_name='Favicon')),
                ('footer', models.ManyToManyField(related_name='footer', to='configuracao_core.ImagemGenerica', verbose_name='Imagens no Rodapé')),
                ('footer_principal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='footer_principal', to='configuracao_core.imagemgenerica', verbose_name='Imagem Principal no Rodapé')),
                ('login', models.ManyToManyField(related_name='login', to='configuracao_core.ImagemGenerica', verbose_name='Imagens no Login')),
            ],
            options={
                'verbose_name': 'Imagens do Sistema',
                'verbose_name_plural': 'Imagens do Sistema',
                'db_table': 'configuracao_imagens_sistema',
            },
        ),
    ]
