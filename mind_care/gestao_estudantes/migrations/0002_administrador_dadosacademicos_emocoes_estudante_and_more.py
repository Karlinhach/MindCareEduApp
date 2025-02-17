# Generated by Django 5.1.3 on 2024-11-27 03:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_estudantes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id_adm', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('contatos', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('sexo', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='DadosAcademicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.CharField(max_length=50)),
                ('turma', models.CharField(max_length=100)),
                ('notas', models.FloatField()),
                ('media', models.FloatField()),
                ('ira', models.FloatField()),
                ('faltas', models.IntegerField()),
                ('presenca', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Emocoes',
            fields=[
                ('id_emocao', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.TextField()),
                ('emocao_detectada', models.CharField(max_length=100)),
                ('data_hora', models.DateTimeField()),
                ('confianca', models.DecimalField(decimal_places=2, max_digits=5)),
                ('foto', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Estudante',
            fields=[
                ('matricula', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('contatos', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('sexo', models.CharField(max_length=20)),
                ('foto', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Relatorios',
            fields=[
                ('id_relatorio', models.AutoField(primary_key=True, serialize=False)),
                ('emocao_detectada', models.CharField(max_length=100)),
                ('relatorio', models.TextField()),
                ('data_hora', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Alunos',
        ),
        migrations.AddField(
            model_name='emocoes',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_estudantes.estudante'),
        ),
        migrations.AddField(
            model_name='dadosacademicos',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_estudantes.estudante'),
        ),
        migrations.AddField(
            model_name='relatorios',
            name='id_emocao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_estudantes.emocoes'),
        ),
        migrations.AddField(
            model_name='relatorios',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_estudantes.estudante'),
        ),
    ]
