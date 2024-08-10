-- Create a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE current_user_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
	FETCH cur INTO current_user_id;

	IF done THEN
	    LEAVE read_loop;
	END IF;

	-- Call the procedure to compute the average score for the current user
	CALL ComputeAverageWeightedScoreForUser(current_user_id);
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
