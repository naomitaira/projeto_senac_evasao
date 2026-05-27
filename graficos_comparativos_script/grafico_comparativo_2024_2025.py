import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV_2024 = BASE / 'censo_escolar_2024_limpo.csv'
CSV_2025 = BASE / 'censo_escolar_2025_limpo.csv'

COLUMNS = [
    'NO_REGIAO',
    'IN_INTERNET_ALUNOS',
    'QT_TABLET_ALUNO',
    'IN_LABORATORIO_INFORMATICA',
    'IN_BIBLIOTECA',
    'IN_ALIMENTACAO',
    'IN_REFEITORIO',
    'IN_AGUA_POTAVEL',
    'IN_ENERGIA_REDE_PUBLICA',
    'IN_ESGOTO_REDE_PUBLICA',
    'IN_BANHEIRO',
    'IN_QUADRA_ESPORTES',
]

BOOLEAN_COLS = [
    'IN_INTERNET_ALUNOS',
    'IN_LABORATORIO_INFORMATICA',
    'IN_BIBLIOTECA',
    'IN_ALIMENTACAO',
    'IN_REFEITORIO',
    'IN_AGUA_POTAVEL',
    'IN_ENERGIA_REDE_PUBLICA',
    'IN_ESGOTO_REDE_PUBLICA',
    'IN_BANHEIRO',
    'IN_QUADRA_ESPORTES',
]


def read_and_prepare(path: Path):
    # Read only required columns; keep boolean columns as strings ('Sim'/'Não') for counting
    df = pd.read_csv(path, usecols=lambda c: c in COLUMNS)
    # Ensure numeric for QT_TABLET_ALUNO
    if 'QT_TABLET_ALUNO' in df.columns:
        df['QT_TABLET_ALUNO'] = pd.to_numeric(df['QT_TABLET_ALUNO'], errors='coerce').fillna(0)
    return df


def aggregate_by_region(df: pd.DataFrame):
    # Aggregate numeric columns (currently only QT_TABLET_ALUNO) by mean per region
    agg_cols = {}
    if 'QT_TABLET_ALUNO' in df.columns:
        agg_cols['QT_TABLET_ALUNO'] = 'mean'
    if not agg_cols:
        return df.groupby('NO_REGIAO').size().reset_index(name='count')
    grouped = df.groupby('NO_REGIAO').agg(agg_cols).reset_index()
    return grouped


def plot_comparison(df24_raw, df25_raw, df24, df25, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    regions = sorted(set(df24_raw['NO_REGIAO']).union(df25_raw['NO_REGIAO']),
                     key=lambda r: ['Norte','Nordeste','Centro-Oeste','Sudeste','Sul'].index(r) if r in ['Norte','Nordeste','Centro-Oeste','Sudeste','Sul'] else r)

    # df24 and df25 here are aggregated numeric dfs (may contain QT_TABLET_ALUNO)
    df24_num = df24.set_index('NO_REGIAO').reindex(regions).fillna(0)
    df25_num = df25.set_index('NO_REGIAO').reindex(regions).fillna(0)

    sns.set(style='whitegrid')

    # One bar chart per column (excluding NO_REGIAO)
    # For each column requested, create appropriate chart. Boolean columns: counts of 'Sim'/'Não' per region (stacked, grouped by year).
    cols_to_plot = [c for c in COLUMNS if c != 'NO_REGIAO']
    for col in cols_to_plot:

        plt.figure(figsize=(10,6))
        x = np.arange(len(regions))
        width = 0.35

        if col in BOOLEAN_COLS:
            # compute counts per region for each year
            counts24 = df24_raw.groupby(['NO_REGIAO', col]).size().unstack(fill_value=0).reindex(regions).fillna(0)
            counts25 = df25_raw.groupby(['NO_REGIAO', col]).size().unstack(fill_value=0).reindex(regions).fillna(0)

            sim24 = counts24.get('Sim', pd.Series(0, index=regions)).values
            nao24 = counts24.get('Não', pd.Series(0, index=regions)).values
            sim25 = counts25.get('Sim', pd.Series(0, index=regions)).values
            nao25 = counts25.get('Não', pd.Series(0, index=regions)).values

            # 2024 bars (left)
            p1 = plt.bar(x - width/2, sim24, width, label='2024 - Sim', color='#4c72b0')
            p2 = plt.bar(x - width/2, nao24, width, bottom=sim24, label='2024 - Não', color='#55a868')
            # 2025 bars (right)
            p3 = plt.bar(x + width/2, sim25, width, label='2025 - Sim', color='#c44e52')
            p4 = plt.bar(x + width/2, nao25, width, bottom=sim25, label='2025 - Não', color='#8172b2')

            plt.ylabel('Contagem')
            plt.title(f'Contagem Sim/Não por região — {col}')
            plt.xticks(x, regions, rotation=45)
            # custom legend (avoid duplicate labels)
            plt.legend()

        else:
            # numeric column (QT_TABLET_ALUNO)
            y24 = df24_num.get(col, pd.Series(0, index=regions)).values
            y25 = df25_num.get(col, pd.Series(0, index=regions)).values
            plt.bar(x - width/2, y24, width, label='2024')
            plt.bar(x + width/2, y25, width, label='2025')
            plt.ylabel(col)
            plt.title(f'Comparação por região — {col}')
            plt.xticks(x, regions, rotation=45)
            plt.legend()

        plt.xlabel('Região')
        plt.tight_layout()
        out_file = out_dir / f'comparativo_{col.lower()}.png'
        plt.savefig(out_file)
        plt.close()

    # Also create a combined plot with multiple subplots
    n = len(cols_to_plot)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*3.5), squeeze=False)
    axes = axes.flatten()
    for i, col in enumerate(cols_to_plot):
        ax = axes[i]
        x = np.arange(len(regions))
        width = 0.3
        if col in BOOLEAN_COLS:
            counts24 = df24_raw.groupby(['NO_REGIAO', col]).size().unstack(fill_value=0).reindex(regions).fillna(0)
            counts25 = df25_raw.groupby(['NO_REGIAO', col]).size().unstack(fill_value=0).reindex(regions).fillna(0)
            sim24 = counts24.get('Sim', pd.Series(0, index=regions)).values
            nao24 = counts24.get('Não', pd.Series(0, index=regions)).values
            sim25 = counts25.get('Sim', pd.Series(0, index=regions)).values
            nao25 = counts25.get('Não', pd.Series(0, index=regions)).values
            ax.bar(x - width/2, sim24, width, label='2024 - Sim', color='#4c72b0')
            ax.bar(x - width/2, nao24, width, bottom=sim24, label='2024 - Não', color='#55a868')
            ax.bar(x + width/2, sim25, width, label='2025 - Sim', color='#c44e52')
            ax.bar(x + width/2, nao25, width, bottom=sim25, label='2025 - Não', color='#8172b2')
            ax.set_ylabel('Contagem')
        else:
            y24 = df24_num.get(col, pd.Series(0, index=regions)).values
            y25 = df25_num.get(col, pd.Series(0, index=regions)).values
            ax.bar(x - width/2, y24, width, label='2024')
            ax.bar(x + width/2, y25, width, label='2025')
            ax.set_ylabel(col)
        ax.set_title(col)
        ax.set_xticks(x)
        ax.set_xticklabels(regions, rotation=45)
        ax.legend()

    # hide unused axes
    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])

    fig.tight_layout()
    fig.savefig(out_dir / 'comparativo_todas_colunas.png')
    plt.close(fig)


def main():
    df24_raw = read_and_prepare(CSV_2024)
    df25_raw = read_and_prepare(CSV_2025)

    agg24 = aggregate_by_region(df24_raw)
    agg25 = aggregate_by_region(df25_raw)

    out_dir = BASE / 'graficos_comparativos_2024_2025'
    plot_comparison(df24_raw, df25_raw, agg24, agg25, out_dir)
    print('Gráficos gerados em:', out_dir)


if __name__ == '__main__':
    main()
