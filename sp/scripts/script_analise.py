import pandas as pd


##################### FUNÇÃO PARA PADRONIZAR MUNICÍPIOS #####################

def padronizar_municipios(df):

    df['Municipio'] = (
        df['Municipio']
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


##################### FUNÇÃO PARA PROCESSAR CADA ANO #####################

def processar_ano(ano):

    print(f'\nProcessando {ano}...')


    ##################### EVASÃO #####################

    abandono = pd.read_csv(
        fr'sp/dados_limpos/total_abandono_escolar_{ano}.csv',
        sep=';',
        decimal=',',
        encoding='utf-8'
    )

    abandono = padronizar_municipios(abandono)


    ##################### INFRAESTRUTURA #####################

    infra = pd.read_csv(
        fr'sp/dados_limpos/censo_escolar_{ano}_limpo.csv',
        encoding='utf-8'
    )

    infra = padronizar_municipios(infra)


    ##################### CONVERTER SIM/NÃO #####################

    mapeamento = {
        'Sim': 1,
        'Não': 0
    }

    colunas_infra = [
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

    for coluna in colunas_infra:

        infra[coluna] = infra[coluna].replace(mapeamento)


    ##################### AGRUPAR POR MUNICÍPIO #####################

    infra_agrupada = (
        infra
        .groupby('Municipio')[colunas_infra]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )


    ##################### JUNTAR TABELAS #####################

    relacao = abandono.merge(
        infra_agrupada,
        on='Municipio',
        how='inner'
    )


    ##################### MOSTRAR RESULTADOS #####################

    print('\nQuantidade de linhas:')

    print(relacao.shape)

    print('\nPrimeiras linhas:')

    print(relacao.head())


    ##################### CORRELAÇÃO #####################

    print('\nCorrelação entre evasão e internet:')

    print(
        relacao[
            [
                'Total Abandono Escolar',
                'Acesso à internet para alunos'
            ]
        ].corr()
    )
    print('\nCorrelação entre evasão e internet:')

    print('\nCorrelação entre evasão e alimentação:')
    
    print(
        relacao[
            [
                'Total Abandono Escolar',
                'Acesso à Alimentação'
            ]
        ].corr()
    )
    print('\nCorrelação entre evasão e acesso à água potável:')
    
    print(
        relacao[
            [
                'Total Abandono Escolar',
                'Acesso à Água potável'
            ]
        ].corr()
    )
    print('\nCorrelação entre evasão e acesso à energia elétrica:')
    
    
    print(
        relacao[
            [
                'Total Abandono Escolar',
                'Acesso à Energia elétrica da rede pública'
            ]
        ].corr()
    )
    print('\nCorrelação entre evasão e acesso ao esgoto:')
    
    print(
        relacao[
            [
                'Total Abandono Escolar',
                'Acesso à Esgoto da rede pública'
            ]
        ].corr()
    )

    ##################### MAIOR EVASÃO #####################

    print('\nTop 5 municípios com maior evasão:')

    print(
        relacao.sort_values(
            by='Total Abandono Escolar',
            ascending=False
        ).head(5)
    )


    ##################### SALVAR #####################

    # relacao.to_csv(
    #     fr'sp/dados_limpos/relacao_evasao_infraestrutura_{ano}.csv',
    #     sep=';',
    #     decimal=',',
    #     index=False,
    #     encoding='utf-8'
    # )
    
    relacao.to_excel(
        fr'sp/dados_limpos/relacao_evasao_infraestrutura_{ano}.xlsx',
        index=False
    )

    print(f'\nArquivo {ano} salvo com sucesso!')


##################### EXECUTAR #####################

processar_ano(2022)
processar_ano(2023)
processar_ano(2024)