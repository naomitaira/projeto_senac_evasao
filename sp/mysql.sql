-- Criação do BD - senac evasao
create database senac_evasao;

-- Use a Database 
use senac_evasao;

-- Criação das tabelas do BD 

CREATE TABLE censo_2022 ( 
     regiao VARCHAR(100) NOT NULL, 
     UF VARCHAR(100) NOT NULL, 
     nome_municipio VARCHAR(100) NOT NULL, 
     acesso_internet VARCHAR(10) NOT NULL,
     qtde_tablets VARCHAR(10) NOT NULL,
     lab_informatica VARCHAR(10) NOT NULL,
     biblioteca VARCHAR(10) NOT NULL,
     alimentacao VARCHAR(10) NOT NULL,
     refeitorio VARCHAR(10) NOT NULL,
     agua_pot VARCHAR(10) NOT NULL,
     energia_elet VARCHAR(10) NOT NULL,
     esgoto VARCHAR(10) NOT NULL,
     banheiro VARCHAR(10) NOT NULL,
     quadra_esp VARCHAR(10) NOT NULL
      
); 

CREATE TABLE censo_2023 ( 
     regiao VARCHAR(100) NOT NULL, 
     UF VARCHAR(100) NOT NULL, 
     nome_municipio VARCHAR(100) NOT NULL, 
     acesso_internet VARCHAR(10) NOT NULL,
     qtde_tablets VARCHAR(10) NOT NULL,
     lab_informatica VARCHAR(10) NOT NULL,
     biblioteca VARCHAR(10) NOT NULL,
     alimentacao VARCHAR(10) NOT NULL,
     refeitorio VARCHAR(10) NOT NULL,
     agua_pot VARCHAR(10) NOT NULL,
     energia_elet VARCHAR(10) NOT NULL,
     esgoto VARCHAR(10) NOT NULL,
     banheiro VARCHAR(10) NOT NULL,
     quadra_esp VARCHAR(10) NOT NULL
     
     );
      

CREATE TABLE censo_2024 ( 
     regiao VARCHAR(100) NOT NULL, 
     UF VARCHAR(100) NOT NULL, 
     nome_municipio VARCHAR(100) NOT NULL, 
     acesso_internet VARCHAR(10) NOT NULL,
     qtde_tablets VARCHAR(10) NOT NULL,
     lab_informatica VARCHAR(10) NOT NULL,
     biblioteca VARCHAR(10) NOT NULL,
     alimentacao VARCHAR(10) NOT NULL,
     refeitorio VARCHAR(10) NOT NULL,
     agua_pot VARCHAR(10) NOT NULL,
     energia_elet VARCHAR(10) NOT NULL,
     esgoto VARCHAR(10) NOT NULL,
     banheiro VARCHAR(10) NOT NULL,
     quadra_esp VARCHAR(10) NOT NULL
     
     );
      

CREATE TABLE fluxo_2022 (
     nome_municipio VARCHAR(100) NOT NULL, 
     abandono_ef_anos_iniciais int NOT NULL,
     abandono_ef_anos_finais int NOT NULL,
     abandono_ensino_medio int NOT NULL,
     total_abandono int NOT NULL
      
); 

CREATE TABLE fluxo_2023 (
     nome_municipio VARCHAR(100) NOT NULL, 
     abandono_ef_anos_iniciais int NOT NULL,
     abandono_ef_anos_finais int NOT NULL,
     abandono_ensino_medio int NOT NULL,
     total_abandono int NOT NULL
      
); 

CREATE TABLE fluxo_2024 (
     nome_municipio VARCHAR(100) NOT NULL, 
     abandono_ef_anos_iniciais int NOT NULL,
     abandono_ef_anos_finais int NOT NULL,
     abandono_ensino_medio int NOT NULL,
     total_abandono int NOT NULL
      
); 
 
