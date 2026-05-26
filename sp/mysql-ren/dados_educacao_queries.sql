SELECT regiao, AVG(taxa_abandono)
FROM indicadores_completos
GROUP BY regiao;

SELECT localizacao, AVG(taxa_abandono)
FROM indicadores_completos
GROUP BY localizacao;

SELECT dependencia_administrativa, AVG(taxa_abandono)
FROM indicadores_completos
GROUP BY dependencia_administrativa;

SELECT AVG(renda_media), AVG(taxa_abandono)
FROM indicadores_completos;

