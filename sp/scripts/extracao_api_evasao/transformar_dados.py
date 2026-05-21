import pandas as pd
import os

##################### FUNÇÕES AUXILIARES #####################

def renomear_colunas_censo(df):

    colunas = {
        'NO_REGIAO': 'Região',
        'NO_UF': 'UF',
        'NO_MUNICIPIO': 'Municipio',
        'IN_INTERNET_ALUNOS': 'Acesso à internet para alunos',
        'QT_TABLET_ALUNO': 'Quantidade de tablets para alunos',
        'IN_LABORATORIO_INFORMATICA': 'Acesso ao Laboratório de informática',
        'IN_BIBLIOTECA': 'Acesso à Biblioteca',
        'IN_ALIMENTACAO': 'Acesso à Alimentação',
        'IN_REFEITORIO': 'Acesso ao Refeitório',
        'IN_AGUA_POTAVEL': 'Acesso à Água potável',
        'IN_ENERGIA_REDE_PUBLICA': 'Acesso à Energia elétrica da rede pública',
        'IN_ESGOTO_REDE_PUBLICA': 'Acesso à Esgoto da rede pública',
        'IN_BANHEIRO': 'Acesso ao Banheiro',
        'IN_QUADRA_ESPORTES': 'Acesso à Quadra de esportes'
    }

    return df.rename(columns=colunas)


def selecionar_colunas_existentes(df, colunas):

    colunas_existentes = [col for col in colunas if col in df.columns]

    return (
        df[colunas_existentes]
        .replace('', pd.NA)
        .dropna(how='any')
        .copy()
    )


def transformar_booleanos(df, colunas_booleanas):

    mapeamento = {
        1: 'Sim',
        0: 'Não',
        1.0: 'Sim',
        0.0: 'Não'
    }

    df[colunas_booleanas] = df[colunas_booleanas].replace(mapeamento)

    return df


def calcular_total_abandono(df, colunas_abandono):

    for coluna in colunas_abandono:

        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(',', '.', regex=False)
        )

        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    df['Total Abandono Escolar'] = df[colunas_abandono].sum(axis=1)

    total_abandono = (
        df.groupby('Municipio')['Total Abandono Escolar']
        .mean()
        .round(2)
        .reset_index()
    )

    return total_abandono


##################### FUNÇÃO PRINCIPAL #####################

def transformar_dados():

    os.makedirs(r'sp/dados_limpos', exist_ok=True)

    ##################### CENSO ESCOLAR #####################

    anos = [2022, 2023, 2024]

    colunas_relevantes = [
        'Região',
        'UF',
        'Municipio',
        'Acesso à internet para alunos',
        'Quantidade de tablets para alunos',
        'Acesso ao Laboratório de informática',
        'Acesso à Biblioteca',
        'Acesso à Alimentação',
        'Acesso ao Refeitório',
        'Acesso à Água potável',
        'Acesso à Energia elétrica da rede pública',
        'Acesso à Esgoto da rede pública',
        'Acesso ao Banheiro',
        'Acesso à Quadra de esportes'
    ]

    colunas_booleanas = [
        'Acesso à internet para alunos',
        'Acesso ao Laboratório de informática',
        'Acesso à Biblioteca',
        'Acesso à Alimentação',
        'Acesso ao Refeitório',
        'Acesso à Água potável',
        'Acesso à Energia elétrica da rede pública',
        'Acesso à Esgoto da rede pública',
        'Acesso ao Banheiro',
        'Acesso à Quadra de esportes'
    ]

    for ano in anos:

        print(f'Carregando Censo {ano}...')

        caminho = rf'sp\{ano}\microdados_ed_basica_{ano}.csv'

        df = pd.read_csv(
            caminho,
            sep=';',
            encoding='latin-1',
            on_bad_lines='skip',
            low_memory=False
        )

        df = renomear_colunas_censo(df)

        df = selecionar_colunas_existentes(df, colunas_relevantes)

        df = transformar_booleanos(df, colunas_booleanas)

        df.to_csv(
            rf'sp/dados_limpos/censo_escolar_{ano}_limpo.csv',
            index=False,
            encoding='utf-8'
        )

        print(f'Censo {ano} tratado com sucesso!')


    ##################### FLUXO ESCOLAR #####################

    renomear_fluxo = {
        'NM_MUNICIPIO': 'Municipio',
        'NM_COMPLETO_ESCOLA': 'Escola',
        'ABA_1': 'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
        'ABA_2': 'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'ABA_3': 'Porcentagem de abandono - Ensino Médio'
    }

    colunas_fluxo = [
        'Municipio',
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio'
    ]

    for ano in anos:

        print(f'Carregando Fluxo Escolar {ano}...')

        caminho_fluxo = rf'sp\{ano}\Fluxo Escolar {ano} - por municipio.csv'

        df_fluxo = pd.read_csv(
            caminho_fluxo,
            sep=';',
            encoding='latin-1',
            on_bad_lines='skip',
            engine='python'
        )

        df_fluxo = df_fluxo.rename(columns=renomear_fluxo)

        df_fluxo = df_fluxo[colunas_fluxo]

        df_fluxo = df_fluxo.dropna(how='any')

        colunas_abandono = [
            'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
            'Porcentagem de abandono - Ensino fundamental - Anos Finais',
            'Porcentagem de abandono - Ensino Médio'
        ]

        abandono = calcular_total_abandono(
            df_fluxo,
            colunas_abandono
        )

        df_fluxo.to_csv(
            rf'sp/dados_limpos/fluxo_escolar_municipio_{ano}_limpo.csv',
            sep=';',
            decimal=',',
            index=False,
            encoding='utf-8'
        )

        abandono.to_csv(
            rf'sp/dados_limpos/abandono_escolar_{ano}.csv',
            sep=';',
            decimal=',',
            index=False,
            encoding='utf-8'
        )

        print(f'Fluxo Escolar {ano} tratado com sucesso!')

    print('Todos os arquivos foram transformados com sucesso!')


##################### EXECUTAR #####################

transformar_dados()