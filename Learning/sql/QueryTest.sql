SELECT			P.Year, 
                SUM(P.Economics) AS Opex_MUSD
FROM			UCube.Economics P
INNER JOIN		UCube.Asset A ON A.Id = P.FK_Asset
INNER JOIN		UCube.Geography G ON G.Id = A.FK_Geography
INNER JOIN		UCube.OilAndGas OG ON OG.Id = P.FK_OilAndGas
INNER JOIN		UCube.EconomicsType ET ON ET.Id = P.FK_EconomicsType
WHERE			G.Country = 'Denmark'
AND				OG.[Oil And Gas Group] = 'Liquids'
AND				ET.[Economics Group] = 'Opex'
AND				P.Year BETWEEN 2000 AND 2030
GROUP BY		P.Year;