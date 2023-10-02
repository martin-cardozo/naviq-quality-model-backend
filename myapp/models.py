from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from io import BytesIO
import json


class Evaluative_Entity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    weight = models.FloatField()

    class Meta:
        abstract = True  # clase abstracta para que no tener que instanciar directamente

    @classmethod
    def createEntity(cls, name, description, weight):
        entity = cls(name=name, description=description, weight=weight)
        entity.save()
        return entity

    @classmethod
    def getEntity(cls, entity_id):
        try:
            return cls.objects.get(id=entity_id)
        except cls.DoesNotExist:
            return None

    def updateEntity(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight
        self.save()

    def deleteEntity(self):
        self.delete()

    @classmethod
    def listAllEntities(cls):
        return cls.objects.all()
    

class Answer_Option(models.Model):
    id_answer_option = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    value = models.FloatField()

    def getDescription(self):
        return self.description

    def getValue(self):
        return self.value

    def __str__(self):
        return self.description  #  devuelve la descripción 




class Application(Evaluative_Entity):
    answer_option_list = models.ManyToManyField(Answer_Option, blank=True)

    def addAnswerOption(self, answer_option):
        self.answer_option_list.add(answer_option)

    def removeAnswerOption(self, answer_option):
        self.answer_option_list.remove(answer_option)

    def listAllAnswerOptions(self):
        return self.answer_option_list.all()

    def calculateScore(self):
        return sum(option.value for option in self.answer_option_list.all())

    def __str__(self):
        return f'Application {self.id}'



class Property(Evaluative_Entity):
    application_list = models.ManyToManyField(Application, blank=True)

    def addApplication(self, application):
        self.application_list.add(application)

    def removeApplication(self, application):
        self.application_list.remove(application)

    def listAllApplications(self):
        return self.application_list.all()

    def calculateScore(self):
        return sum(application.calculateScore() for application in self.application_list.all())

    def __str__(self):
        return f'Property {self.id}'



class Criterion(Evaluative_Entity):
    property_list = models.ManyToManyField(Property, blank=True)

    def addProperty(self, property):
        self.property_list.add(property)

    def removeProperty(self, property):
        self.property_list.remove(property)

    def listAllProperties(self):
        return self.property_list.all()

    def calculateScore(self):
        return sum(property.calculateScore() for property in self.property_list.all())

    def __str__(self):
        return f'Criterion {self.id}'


class Quality_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    custom = models.BooleanField(default=False)
    criteriaList = models.ManyToManyField(Criterion, blank=True)

    @classmethod
    def createProfile(cls, name, description, custom):
        profile = cls(name=name, description=description, custom=custom)
        profile.save()
        return profile

    @classmethod
    def getProfile(cls, profile_id):
        try:
            return cls.objects.get(id=profile_id)
        except cls.DoesNotExist:
            return None

    def updateProfile(self, name, description, custom):
        self.name = name
        self.description = description
        self.custom = custom
        self.save()

    def deleteProfile(self):
        self.delete()

    @classmethod
    def listAllProfiles(cls):
        return cls.objects.all()

    def __str__(self):
        return self.name
    


class CustomUserManager(BaseUserManager):
    def createUser(self, name, email, password=None):
        if not email:
            raise ValueError('El campo Email es obligatorio')
        email = self.normalizeEmail(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def getUser(self, user_id):
        try:
            return self.get(pk=user_id)
        except self.model.DoesNotExist:
            return None

    def updateUser(self, user_id, **kwargs):
        user = self.getUser(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save(using=self._db)
            return user
        return None

    def deleteUser(self, user_id):
        user = self.getUser(user_id)
        if user:
            user.delete()

    def listAllUsers(self):
        return self.all()

class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    customProfile = models.ManyToManyField(Quality_Profile, blank=True)

    evaluations = models.ManyToManyField('Evaluation', related_name='users_evaluated', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(self.id_user)

    def login(self, request):
        user = authenticate(request, username=self.email, password=self.password)
        if user is not None:
            login(request, user)
            return True
        return False

    def logout(self, request):
        logout(request)



class Evaluation_Answer(models.Model):
    evaluation = models.ForeignKey('Evaluation', on_delete=models.CASCADE, related_name='answers')
    answerOption = models.ForeignKey('Answer_Option', on_delete=models.CASCADE)

    def __str__(self):
        return f'Evaluation_Answer {self.id}'



class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    file = models.FileField(upload_to='evaluations/', default='nombre_de_archivo_default.pdf')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    result = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quality_profile = models.OneToOneField(Quality_Profile, on_delete=models.CASCADE, default=1)
    evaluationAnswers = models.ManyToManyField(Evaluation_Answer, blank=True, related_name='evaluations')

    @classmethod
    def createEvaluation(cls, date, file, score, result, user, quality_profile):
        evaluation = cls(
            date=date,
            file=file,
            score=score,
            result=result,
            user=user,
            quality_profile=quality_profile,
        )
        evaluation.save()
        return evaluation

    def calculateFinalScore(self):
        pass

    def __str__(self):
        return f'Evaluation {self.id}'
    
    




