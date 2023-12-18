from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import pandas as pd
import plotly.express as px
import os

def index(request):
    return render(request, 'index.html')

def plot(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        df = pd.read_csv(file_path)
        columns = list(df.columns)
        conditions = [df.nunique().index[i] for i in range(len(df.nunique())) if df.nunique()[i]<=3]
        subsets = []
        for cond in conditions:
            subsets.extend([cond + ":" + i for i in list(df[cond].unique())])
        response = render(request, 'plot.html', {'columns': columns, 'subsets': subsets, 'file': file_path})
    else:
        response = render(request, 'index.html', {'error': 'No file uploaded'})
    #os.remove(file_path)
    return(response)

def plot_result(request):
    if request.method == 'POST':
        selected_columns = request.POST.getlist('selected_columns')
        selected_subsets = request.POST.getlist('selected_subsets')
        file_path = request.POST['file']
        df = pd.read_csv(file_path)
        for pair in selected_subsets:
            df = df[df[pair.split(":")[0]] == pair.split(":")[1]]
        df_selected = df[selected_columns]
        fig = px.box(df_selected,
                 title = "Columns: {}<br>Condition: {} N = {}".format(selected_columns, selected_subsets, len(df_selected)),
                 height = 800,
                 width = 1000,)
        fig.update_layout(
        # title='<b></b>',
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
