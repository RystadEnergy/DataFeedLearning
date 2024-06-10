/*
CUBESCRIPT(UCube) Report
S(TabName:[Data Values], Year;)
F(Year:"2010 - 2023";Greenfield-Brownfield:Greenfield;Economics Group:Capex)
C(Data Values)
R(Country[Sorting:Alpha])
V(Economics:MUSD;Production:Million bbl."Base unit bbl";Economics pr bbl:USD/bbl."Base unit nom")
*/

SELECT  AUXECO.Country,
        SUM([Economics]) AS [Economics],
        SUM([Production]) AS [Production],
        SUM(iif([Production]>0.000100, [Economics]/[Production], 0))
FROM(
    SELECT  G.Country, 
            SUM(R.[Economics]) AS Economics
    FROM UCube.Economics R
    INNER JOIN Ucube.EconomicsType ET ON ET.Id = R.Fk_EconomicsType
    INNER JOIN UCube.Asset A ON A.Id = R.FK_Asset
    INNER JOIN UCube.Geography G ON G.Id = A.Fk_Geography
    INNER JOIN UCube.OtherParameter OP ON OP.Id = R.Fk_OtherParameter
    WHERE   ET.[Economics Group] = 'Capex'
    	    AND OP.[Green Brown Field] = 'Greenfield'
    	    AND R.Year >= 2010 AND R.Year <= 2023
    GROUP BY G.Country) AS AUXECO
LEFT JOIN (
    SELECT  G.Country, 
            SUM(P.[Production]) AS Production
    FROM UCube.Production P
    INNER JOIN UCube.Asset A ON A.Id = P.FK_Asset
    INNER JOIN UCube.Geography G ON G.Id = A.Fk_Geography
    INNER JOIN UCube.OtherParameter OP ON OP.Id = P.Fk_OtherParameter
    WHERE   P.Year >= 2010 AND P.Year <= 2023
    GROUP BY G.Country) AS AUXPROD
ON AUXPROD.Country = AUXECO.Country
GROUP BY AUXECO.Country
ORDER BY AUXECO.Country;