from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import pandas as pd
import plotly.express as px

def index(request):
    return render(request, 'index.html')

from django.core.files.storage import FileSystemStorage

def plot(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        df = pd.read_csv(file_path)
        columns = list(df.columns)
        return render(request, 'plot.html', {'columns': columns, 'file': file_path})
    else:
        return render(request, 'index.html', {'error': 'No file uploaded'})

def plot_result(request):
    selected_columns = request.POST.getlist('columns')
    file_path = request.POST['file']
    df = pd.read_csv(file_path)
    df_selected = df[selected_columns]


def plot_result(request):
    selected_columns = request.POST.getlist('columns')
    file_path = request.POST['file']
    df = pd.read_csv(file_path)
    df_selected = df[selected_columns]
    fig = px.box(df_selected,
             title = str(selected_columns),
             height = 800,
             width = 1000,)

    fig.update_layout(
        font=dict(
            size=20,  # Set the font size
        )
    )
    graph = fig.to_html(full_html=False)
    return render(request, 'plot_result.html', {'graph': graph})


# def display_data(request):
#     if request.method == 'POST' and request.FILES['file']:
#         selected_columns = request.POST.getlist('columns')
#         uploaded_file = request.FILES['file']
#         df = pd.read_csv(uploaded_file)
#         df_selected = df[selected_columns]
#         return render(request, 'display_data.html', {'data': df_selected})
#     else:
#         return render(request, 'index.html', {'error': 'No file uploaded'})
