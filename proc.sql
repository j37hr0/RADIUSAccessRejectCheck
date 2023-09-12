CREATE DEFINER=`radiusmain`@`%` PROCEDURE `rts_CheckAccessRejects`()
BEGIN
	SELECT * FROM radius.radpostauth
	WHERE authdate >= NOW() - INTERVAL 15 MINUTE
	ORDER BY ID DESC;
END$$
DELIMITER ;
