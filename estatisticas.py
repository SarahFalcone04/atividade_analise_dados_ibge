import numpy as np
import pandas as pd

def calcular_estatisticas(valores):
    """
    Calcula estatísticas descritivas para uma série de valores numéricos.

    Parâmetros:
    valores (pd.Series): Série de valores numéricos.

    Retorna:
    dict: Dicionário contendo as estatísticas calculadas.
    """
    valores = np.asarray(valores, dtype=float)  # Converte a série para um array NumPy de float, ignorando valores não numéricos
    valores = valores[~np.isnan(valores)]  # Remove valores NaN do array
    estatisticas = {
        'media': np.mean(valores),
        'mediana': np.median(valores),
        'desvio_padrao': np.std(valores, ddof=1),  # ddof=1 para amostra
        'minimo': np.min(valores),
        'maximo': np.max(valores),
        'amplitude': np.max(valores) - np.min(valores),
        #calcular percentis e iqr
        'q1': np.percentile(valores, 25),
        'q3': np.percentile(valores, 75),
        'iqr': np.percentile(valores, 75) - np.percentile(valores, 25)
    }
    
    return estatisticas