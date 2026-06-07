import os
import pandas as pd

def carregar_excel(path, ano):
    """Carrega um arquivo Excel e adiciona a coluna 'Ano'."""
    df = pd.read_excel(path)
    df['Ano'] = ano
    df['Total Abandono Escolar'] = pd.to_numeric(df['Total Abandono Escolar'], errors='coerce')
    return df

def carregar_dados(base_dir):
    """Carrega todos os arquivos de evasão escolar disponíveis."""
    frames = []
    for ano in [2022, 2023, 2024]:
        path = os.path.join(base_dir, f"relacao_evasao_infraestrutura_{ano}.xlsx")
        if os.path.exists(path):
            frames.append(carregar_excel(path, ano))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
