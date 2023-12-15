from django.shortcuts import render

# Create your views here.
import pandas as pd
import plotly.express as px


def index(request):
    return render(request, 'index.html')

from django.core.files.storage import FileSystemStorage
import tempfile
from django.core.files.uploadhandler import TemporaryFileUploadHandler

import io
import os

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
    if request.method == 'POST':
        selected_columns = request.POST.getlist('selected_columns')
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
        response = render(request, 'plot_result.html', {'graph': graph})
    else:
        response = render(request, 'index.html', {'error': 'Invalid request or action'})
    os.remove(file_path)
    return(response)

def display_data(request):
    if request.method == 'POST':
        selected_columns = request.POST.getlist('selected_columns')
        file_path = request.POST['file']
        df = pd.read_csv(file_path)
        df_selected = df[["sub"] + selected_columns]
        response = render(request, 'display_data.html', {'data': df_selected})
    else:
        response = render(request, 'index.html', {'error': 'Invalid request or action'})
    os.remove(file_path)
    return(response)
