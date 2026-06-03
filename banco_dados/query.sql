SELECT regiao, AVG(taxa_abandono)
FROM indicadores_completo
GROUP BY regiao;

SELECT localizacao, AVG(taxa_abandono)
FROM indicadores_completo
GROUP BY localizacao;

SELECT dependencia_administrativa, AVG(taxa_abandono)
FROM indicadores_completo
GROUP BY dependencia_administrativa;

SELECT AVG(renda_media), AVG(taxa_abandono)
FROM indicadores_completo;