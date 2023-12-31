# Generated by Django 4.2.5 on 2023-09-22 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_evaluation_vis_file'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnswerOption',
            new_name='Answer_Option',
        ),
        migrations.RenameModel(
            old_name='CriteriaProperties',
            new_name='Criteria_Properties',
        ),
        migrations.RenameModel(
            old_name='Criteria',
            new_name='Criterion',
        ),
        migrations.RenameModel(
            old_name='EvaluationAnswerOption',
            new_name='Evaluation_Answer_Option',
        ),
        migrations.RenameModel(
            old_name='PropertiesApplications',
            new_name='Properties_Applications',
        ),
        migrations.RenameModel(
            old_name='QualityProfile',
            new_name='Quality_Profile',
        ),
        migrations.RenameModel(
            old_name='QualityProfileCriteria',
            new_name='Quality_Profiles_Criteria',
        ),
        migrations.RenameField(
            model_name='answer_option',
            old_name='id_answerOption',
            new_name='id_answer_option',
        ),
        migrations.RenameField(
            model_name='criteria_properties',
            old_name='criteria',
            new_name='criterion',
        ),
        migrations.RenameField(
            model_name='criterion',
            old_name='id_criteria',
            new_name='id_criterion',
        ),
        migrations.RenameField(
            model_name='quality_profile',
            old_name='id_qualityProfile',
            new_name='id_quality_profile',
        ),
        migrations.RenameField(
            model_name='quality_profiles_criteria',
            old_name='criteria',
            new_name='criterion',
        ),
    ]
