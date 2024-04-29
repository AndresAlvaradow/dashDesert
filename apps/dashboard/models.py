from django.db import models

# Create your models here.
class MachineData(models.Model):
    idMachien = models.AutoField(primary_key=True)
    precision = models.FloatField()
    recall = models.FloatField()
    accuracy = models.FloatField()
    title = models.CharField(max_length=255)

class DeepData(models.Model):
    idDeep = models.AutoField(primary_key=True)
    precision = models.FloatField()
    accuracy = models.FloatField()
    title = models.CharField(max_length=255)

class schoolYear(models.Model):
    idScholYear = models.AutoField(primary_key=True)
    nameYear = models.CharField(max_length=100, null=True, blank=True)
    id_year = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nameYear


class student(models.Model):
    identification = models.CharField(max_length=255, primary_key=True, unique=True)
    school_year = models.ManyToManyField(schoolYear, through='StudentSchoolYear', related_name='students')
    
    def __str__(self):
        return self.identification

class StudentSchoolYear(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    school_year = models.ForeignKey(schoolYear, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True)

class DataStudent(models.Model):
    idDataStudent = models.AutoField(primary_key=True)
    identification = models.ForeignKey(student, on_delete=models.CASCADE)
    names = models.CharField(max_length=300)
    modality = models.CharField(max_length=300)
    cycle = models.IntegerField(null=True, blank=True)
    qualification = models.DecimalField(max_digits=5, decimal_places=2)
    courseName = models.CharField(max_length=300)
    program = models.CharField(max_length=300)
    nameYear = models.ForeignKey(schoolYear, on_delete=models.CASCADE)
    region = models.CharField(max_length=300)
    zone = models.CharField(max_length=300)
    centerSchool = models.CharField(max_length=300)
    studentType = models.CharField(max_length=300)

class ResultDataStudent(models.Model):
    idDataStudentResult = models.AutoField(primary_key=True)
    identification = models.ForeignKey(student, on_delete=models.CASCADE)
    deserta = models.CharField(max_length=300, null=True, blank=True)
    lstm = models.DecimalField(max_digits=5, decimal_places=2)
    cnn = models.DecimalField(max_digits=5, decimal_places=2)

class Models(models.Model):
    idModels = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class MachineLearningMetrics(models.Model):
    idMachineLearningMetrics = models.AutoField(primary_key=True)
    nameYear = models.ForeignKey(schoolYear, on_delete=models.CASCADE)
    idModels = models.ForeignKey(Models, on_delete=models.CASCADE)
    precision = models.DecimalField(max_digits=5, decimal_places=2)
    recall = models.DecimalField(max_digits=5, decimal_places=2)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    # Agrega más campos de medida según sea necesario


    def __str__(self):
        return f"{self.nameYear} - {self.idModels}"
    
class DeepLearningMetrics(models.Model):
    idDeepLearningMetrics = models.AutoField(primary_key=True)
    nameYear = models.ForeignKey(schoolYear, on_delete=models.CASCADE)
    idModels = models.ForeignKey(Models, on_delete=models.CASCADE)
    precision = models.DecimalField(max_digits=5, decimal_places=2)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    # Agrega más campos de medida según sea necesario

    def __str__(self):
        return f"{self.nameYear} - {self.idModels}"