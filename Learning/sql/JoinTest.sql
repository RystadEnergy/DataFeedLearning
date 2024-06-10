SELECT			TOP 10 *
FROM			UCube.Economics P
INNER JOIN		UCube.Asset A ON A.Id = P.FK_Asset;