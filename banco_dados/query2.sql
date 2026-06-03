SELECT ano, uf, municipio, instituicao
FROM censo_escolar;  

SELECT *
FROM censo_escolar
WHERE ano = 2024; 

SELECT *
FROM censo_escolar
WHERE uf = 'RO'; 

SELECT *
FROM censo_escolar
WHERE uf = 'RO' AND ano = 2024;
----------------------------------------------------------------------- 
SELECT ano, regiao, taxa_abandono, renda_media
FROM indicadores_completos; 

SELECT *
FROM indicadores_completos
WHERE regiao = 'Nordeste'; 

SELECT *
FROM indicadores_completos
ORDER BY taxa_abandono DESC;
