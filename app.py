import streamlit as st
import nbformat
import matplotlib.pyplot as plt
import io
import sys
import os

# streamlit run app.py / para executar

# Função para executar o notebook e capturar o gráfico
def execute_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    local_vars = {}
    fig = None

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            try:
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                exec(cell.source, globals(), local_vars)
                sys.stdout = old_stdout

                for var in local_vars.values():
                    if isinstance(var, plt.Figure):
                        fig = var
                        break
                    elif isinstance(var, plt.Axes):
                        fig = var.figure
                        break
                if fig:
                    return fig
            except Exception as e:
                st.error(f'Erro na execução da célula: {e}')
                return None
    return None

st.title('Visualizador de Gráficos de Notebooks')

opcao = st.radio('Escolha uma opção:', ['Venda de Carros', 'Venda de Motos', 'Venda de Caminhonetes'])

arquivoEscolhido = {
    "Venda de Carros": 'Untitled3.ipynb',
    "Venda de Motos": 'Untitled4.ipynb',
    "Venda de Caminhonetes": 'Untitled5.ipynb',
}

if st.button('Gerar gráfico'):
    caminhoArquivo = arquivoEscolhido[opcao]

    if os.path.exists(caminhoArquivo):
        fig = execute_notebook(caminhoArquivo)
        if fig:
            st.pyplot(fig)
        else:
            st.warning('Nenhum gráfico foi gerado no notebook.')
    else:
        st.error(f'Arquivo não encontrado: {caminhoArquivo}')
