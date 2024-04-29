import matplotlib
matplotlib.use("Agg")  # Cambia el backend a no interactivo
from apps.dashboard.models import MachineData, DeepData, DataStudent, ResultDataStudent, StudentSchoolYear, schoolYear
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import matplotlib.pyplot as plt
import io
import base64
from django.template.loader import render_to_string
from django.db.models import Sum, Avg
from django.db.models.functions import Cast
from django.db.models import Max, Subquery
import random  # Importa la biblioteca random para generar colores aleatorios
class Home(LoginRequiredMixin, TemplateView):
    template_name = 'tables.html'
    login_url = 'dashboard:login'

# @login_required(login_url="/login/")
# def main(LoginRequiredMixin, ListView):
#     model = DataStudent
#     template_name = 'tables.html'
#     context_object_name = 'datastudents'
#     login_url = 'dashboard:login'
#     #return render(request, 'tables.html')
class main(LoginRequiredMixin, ListView):
    model = DataStudent
    template_name = 'tables.html'
    context_object_name = 'datastudents'
    login_url = 'dashboard:login'
    #return render(request, 'tables.html')
    def get_queryset(self):
        # queryset = super().get_queryset()

    # Subconsulta para seleccionar registros únicos basados en 'identification' y 'nameYear'
        unique_records_subquery = DataStudent.objects.values('identification', 'nameYear').annotate(
            max_id=Max('idDataStudent')
        ).values('max_id')

        # Filtrar registros usando la subconsulta
        queryset = DataStudent.objects.filter(idDataStudent__in=Subquery(unique_records_subquery))
        # Obtener parámetros de filtro
        year_filter = self.request.GET.get('anio', '')
        zone_filter = self.request.GET.get('zona', '')
        region_filter = self.request.GET.get('region', '')
        center_filter = self.request.GET.get('centro', '')
        program_filter = self.request.GET.get('programa', '')
        student_type_filter = self.request.GET.get('student_type', '')
        modality_filter = self.request.GET.get('modality', '')

        # Aplicar filtros a la queryset
        if year_filter:
            queryset = queryset.filter(nameYear=year_filter)
        if zone_filter:
            queryset = queryset.filter(zone=zone_filter)
        if region_filter:
            queryset = queryset.filter(region=region_filter)
        if center_filter:
            queryset = queryset.filter(centerSchool=center_filter)
        if program_filter:
            queryset = queryset.filter(program=program_filter)
        if student_type_filter:
            queryset = queryset.filter(studentType=student_type_filter)
        if modality_filter:
            queryset = queryset.filter(modality=modality_filter)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agregar valores de otro modelo al contexto
        context['schoolYear'] = schoolYear.objects.all()
        unique_zones = DataStudent.objects.values('zone').distinct()
        context['zones'] = unique_zones
        unique_region = DataStudent.objects.values('region').distinct()
        context['regiones'] = unique_region
        unique_centro = DataStudent.objects.values('centerSchool').distinct()
        context['centerSchool'] = unique_centro
        unique_program = DataStudent.objects.values('program').distinct()
        context['programs'] = unique_program
        unique_studentType = DataStudent.objects.values('studentType').distinct()
        context['studentTypes'] = unique_studentType
        unique_modality = DataStudent.objects.values('modality').distinct()
        context['modalitys'] = unique_modality
        # Calcular el promedio de calificaciones por estudiante y año lectivo
      
        student_averages = DataStudent.objects.values('identification', 'nameYear').annotate(
            average_qualification=Avg('qualification')
        ).order_by('identification', 'nameYear')

        # Convertir student_averages en un diccionario para facilitar el acceso
        averages_dict = {(obj['identification'], obj['nameYear']): obj['average_qualification'] for obj in student_averages}

        # Añadir los promedios a los objetos DataStudent
        datastudents_with_averages = []
        for student in context['datastudents']:
            identification = student.identification_id  # Ajusta según tu modelo
            nameYear = student.nameYear_id  # Ajusta según tu modelo
            # Añadir el promedio al objeto estudiante como un nuevo atributo
            average = averages_dict.get((identification, nameYear), None)
            student.average_qualification = average  # Añadir directamente al objeto puede no ser lo ideal, pero funciona para este propósito
            datastudents_with_averages.append(student)

        # Reemplazar datastudents en el contexto con la nueva lista que incluye los promedios
        context['datastudents'] = datastudents_with_averages

        return context


def generar_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Genera un color hexadecimal aleatorio

def generar_grafico(labels, data, title):
    # Crea el gráfico de barras con colores aleatorios
    fig, ax = plt.subplots()
    for label, value in zip(labels, data):
        color = generar_color()
        ax.bar(label, value, color=color)

    ax.set(xlabel='Resultados', ylabel='Valores', title=title)

    # Guarda la imagen en un objeto de bytes
    image_stream = io.BytesIO()
    fig.savefig(image_stream, format='png')
    plt.close(fig)

    # Convierte la imagen a base64 para incrustarla en la plantilla
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def statisticsMachine(request):
    # Datos de ejemplo (puedes obtener estos datos de tu base de datos u otras fuentes)
    conjuntos_de_datos = [
        {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [0.97, 0.94, 0.93,], 'title': 'SVM'},
        {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [0.96, 0.98, 0.88,], 'title': 'KNN'},
        {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [0.97, 0.97, 0.95,], 'title': 'Regresión logistrica'},
        {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [0.96, 0.96, 0.93,], 'title': 'Forest'},
        {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [0.96, 0.90, 0.88,], 'title': 'Arboles de decisión'},
        # Puedes agregar más conjuntos de datos según sea necesario
    ]

    imagenes_base64 = []

    for conjunto in conjuntos_de_datos:
        labels = conjunto['labels']
        data = conjunto['data']
        title = conjunto['title']
        imagen_base64 = generar_grafico(labels, data, title)
        imagenes_base64.append(imagen_base64)

    context = {'imagenes_base64': imagenes_base64}
    html_content = render_to_string('machine.html', context)

    return HttpResponse(html_content)

@login_required(login_url="/login/")
def statistics_machine(request):
    machine_data = MachineData.objects.all()
    conjuntos_de_datos =[]
    for objMachine in machine_data:
        dataTemp = {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':"{:.2f}".format(objMachine.precision)}, {'x':'Recall', 'rec':"{:.2f}".format(objMachine.recall)}, {'x':'Accuracy', 'acc': "{:.2f}".format(objMachine.accuracy)}], 'title': [objMachine.title,]}
        conjuntos_de_datos.append(dataTemp)
    # conjuntos_de_datos = [
    #      {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.97}, {'x':'Recall', 'rec':0.94}, {'x':'Accuracy', 'acc':0.93}], 'title': ['SVM',]},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.96}, {'x':'Recall', 'rec':0.98}, {'x':'Accuracy', 'acc':0.88}], 'title': ['KNN',]},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.97}, {'x':'Recall', 'rec':0.97}, {'x':'Accuracy', 'acc':0.95}], 'title': ['Regresión logistrica']},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.96}, {'x':'Recall', 'rec':0.96}, {'x':'Accuracy', 'acc':0.93}], 'title': ['Forest']},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.96}, {'x':'Recall', 'rec':0.90}, {'x':'Accuracy', 'acc':0.88}], 'title': ['Arboles de decisión']},
    #     # Agrega más conjuntos de datos según sea necesario
    # ]

    context = {'conjuntos_de_datos': conjuntos_de_datos}
    return render(request, 'machine.html', context)

@login_required(login_url="/login/")
def statistics_deep(request):
    deep_data = DeepData.objects.all()
    conjuntos_de_datos =[]
    for objMachine in deep_data:
        dataTemp = {'labels': ['Precisión', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':"{:.2f}".format(objMachine.precision)}, {'x':'Accuracy', 'acc': "{:.2f}".format(objMachine.accuracy)}], 'title': [objMachine.title,]}
        conjuntos_de_datos.append(dataTemp)
    # conjuntos_de_datos = [
    #      {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.97}, {'x':'Recall', 'rec':0.94}, {'x':'Accuracy', 'acc':0.93}], 'title': ['SVM',]},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.96}, {'x':'Recall', 'rec':0.98}, {'x':'Accuracy', 'acc':0.88}], 'title': ['KNN',]},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.97}, {'x':'Recall', 'rec':0.97}, {'x':'Accuracy', 'acc':0.95}], 'title': ['Regresión logistrica']},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.96}, {'x':'Recall', 'rec':0.96}, {'x':'Accuracy', 'acc':0.93}], 'title': ['Forest']},
    #     {'labels': ['Precisión', 'Recall', 'Accuracy'], 'data': [{'x':'Precisión', 'pre':0.96}, {'x':'Recall', 'rec':0.90}, {'x':'Accuracy', 'acc':0.88}], 'title': ['Arboles de decisión']},
    #     # Agrega más conjuntos de datos según sea necesario
    # ]

    context = {'conjuntos_de_datos': conjuntos_de_datos}
    return render(request, 'deep.html', context)

@login_required(login_url="/login/")
def detail_views(request, identification, idScholYear):
    
    dataGraf = ResultDataStudent.objects.get(identification=identification)
    dataTempGraf = [{'labels': ['lstm', 'cnn'], 'data': [{'x':'lstm', 'lstm':"{:.2f}".format(dataGraf.lstm)}, {'x':'cnn', 'cnn': "{:.2f}".format(dataGraf.cnn)}], 'title': ["Pocerntaje de deserción"]}]
    
    student_school_years = StudentSchoolYear.objects.filter(student=identification)
    
    dataStudent = DataStudent.objects.filter(identification=identification, nameYear__idScholYear=idScholYear)
    
    # course_names = [data['courseName'] for data in DataStudent]
    # qualifications = [data['qualification'] for data in DataStudent]
    course_names = []
    qualifications = []
    for data in dataStudent:
        course_names.append(data.courseName)
        qualifications.append(float(data.qualification)) 
   
    data_object = {
    'courseNames': course_names,
    'qualifications': qualifications
    }
    print(data_object)
    return render(request, 'grafs.html', {'dataGraf': dataTempGraf, 'ResultDataStudent': student_school_years, 'DataStudent':dataStudent, 'DataSubjects':data_object})


@login_required(login_url="/login/")
def statistics_academic(request):
    school_years = schoolYear.objects.all()
    year_filter = request.GET.get('anio', '')
    zone_filter = request.GET.get('zona', '')
    region_filter = request.GET.get('region', '')
    center_filter = request.GET.get('centro', '')
    program_filter = request.GET.get('programa', '')
    student_type_filter = request.GET.get('student_type', '')
    modality_filter = request.GET.get('modality', '')

    # Filtrar los datos basados en los parámetros de filtro
    queryset = DataStudent.objects.all()
    if year_filter:
        queryset = queryset.filter(nameYear=year_filter)
    if zone_filter:
        queryset = queryset.filter(zone=zone_filter)
    if region_filter:
        queryset = queryset.filter(region=region_filter)
    if center_filter:
        queryset = queryset.filter(centerSchool=center_filter)
    if program_filter:
        queryset = queryset.filter(program=program_filter)
    if student_type_filter:
        queryset = queryset.filter(studentType=student_type_filter)
    if modality_filter:
        queryset = queryset.filter(modality=modality_filter)

    # Calcular los datos estadísticos
    grouped_data = queryset.values('courseName').annotate(
        total_qualification=Sum('qualification'),
        average_qualification=Avg('qualification'),
    )

    conjuntos_de_datos = []
    for group in grouped_data:
        course_name = group['courseName']
        total_qualification = group['total_qualification']
        average_qualification = group['average_qualification']

        data_temp = {
            'courseName': course_name,
            'total_qualification': total_qualification,
            'average_qualification': average_qualification,
        }

        conjuntos_de_datos.append(data_temp)

    # Preparar datos para el gráfico
    course_names = [course['courseName'] for course in conjuntos_de_datos]
    dataProm = [float(course['average_qualification']) for course in conjuntos_de_datos]
    data_graf = [{'labels': course_names, 'data': dataProm}]
    context = {'data': dataProm, 'labels': course_names,'schoolYear': school_years,}
    unique_zones = DataStudent.objects.values('zone').distinct()
    context['zones'] = unique_zones
    unique_region = DataStudent.objects.values('region').distinct()
    context['regiones'] = unique_region
    unique_centro = DataStudent.objects.values('centerSchool').distinct()
    context['centerSchool'] = unique_centro
    unique_program = DataStudent.objects.values('program').distinct()
    context['programs'] = unique_program
    unique_studentType = DataStudent.objects.values('studentType').distinct()
    context['studentTypes'] = unique_studentType
    unique_modality = DataStudent.objects.values('modality').distinct()
    context['modalitys'] = unique_modality
    
    return render(request, 'criticalm.html', context)