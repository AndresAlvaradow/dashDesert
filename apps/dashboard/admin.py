from django.contrib import admin
from . import models

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class MachineCategoria(resources.ModelResource):
    class Meta:
        model = models.MachineData
        import_id_fields =('idMachien',)

class DataMachine(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['idMachien']
    list_display =('precision', 'recall', 'accuracy', 'title')
    resource_class = MachineCategoria


class DeepCategoria(resources.ModelResource):
    class Meta:
        model = models.DeepData
        import_id_fields =('idDeep',)

class DataDeep(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['idDeep']
    list_display =('precision', 'accuracy', 'title')
    resource_class = DeepCategoria
# para la data del estudiante 
    
class StudentCategoria(resources.ModelResource):
    class Meta:
        model = models.student
        import_id_fields =('identification',)

class DataStudent(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['identification']
    list_display =('identification', 'school_years_display')
    resource_class = StudentCategoria
    def school_years_display(self, obj):
        return ", ".join([str(year) for year in obj.school_year.all()])
    school_years_display.short_description = 'School Years'


# Data del periodo
class YearCategoria(resources.ModelResource):
    class Meta:
        model = models.schoolYear
        import_id_fields =('idScholYear',)

class DataYear(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['idScholYear']
    list_display =('idScholYear', 'nameYear', 'id_year')
    resource_class = YearCategoria

# data de la tabla intermedia entre yearschol y student 
class StudentSchoolYearResource(resources.ModelResource):
    class Meta:
        model = models.StudentSchoolYear
        import_id_fields =('id',)

class DataStudentResource(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['id']
    list_display =('id','student', 'school_year', 'status')
    resource_class = StudentSchoolYearResource

# data geberal del estudiante
class StudentGeneralResource(resources.ModelResource):
    class Meta:
        model = models.DataStudent
        import_id_fields =('idDataStudent',)

class DataStudentgeneralResource(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['idDataStudent']
    list_display =('idDataStudent', 'identification', 'names', 'modality', 'cycle', 'qualification', 'courseName', 'program','nameYear', 'region', 'zone', 'centerSchool','studentType' )
    resource_class = StudentGeneralResource

# data de resultados
    
class ResultStudentResource(resources.ModelResource):
    class Meta:
        model = models.ResultDataStudent
        import_id_fields =('idDataStudentResult',)

class DataResultStudentResource(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['idDataStudentResult']
    list_display =('idDataStudentResult','identification', 'deserta', 'lstm', 'cnn', )
    resource_class = ResultStudentResource

#Metricas 
#modelos
class ModelsResource(resources.ModelResource):
    class Meta:
        model = models.Models
        import_id_fields =('idModels',)

class DataModelsResource(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['name']
    list_display =('idModels','name' )
    resource_class = ModelsResource


#Metricas para modelos de deep learning
class MachineLearningMetricsResource(resources.ModelResource):
    class Meta:
        model = models.MachineLearningMetrics
        import_id_fields =('idMachineLearningMetrics',)

class DataMachineLearningMetricsResource(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields =['idMachineLearningMetrics']
    list_display =('idMachineLearningMetrics','nameYear','idModels','precision','recall','accuracy' )
    resource_class = MachineLearningMetricsResource

admin.site.register(models.MachineData, DataMachine)
admin.site.register(models.DeepData, DataDeep)
admin.site.register(models.student, DataStudent)
admin.site.register(models.schoolYear, DataYear)
admin.site.register(models.StudentSchoolYear, DataStudentResource)
admin.site.register(models.DataStudent, DataStudentgeneralResource)
admin.site.register(models.ResultDataStudent, DataResultStudentResource)
admin.site.register(models.Models, DataModelsResource)
admin.site.register(models.MachineLearningMetrics, DataMachineLearningMetricsResource)

