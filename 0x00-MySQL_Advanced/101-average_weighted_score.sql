-- Create a stored procedure ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all students
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE current_user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_weighted_score FLOAT;

    -- Cursor to iterate through each user
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Declare handler for when the cursor finishes
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through all users
    read_loop: LOOP
        -- Fetch the current user id
        FETCH user_cursor INTO current_user_id;

        -- Exit the loop if no more rows are found
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Initialize total score and total weight
        SET total_score = 0;
        SET total_weight = 0;

        -- Calculate the total score and total weight for the current user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = current_user_id;

        -- Handle cases where total_weight might be NULL or zero
        IF total_weight IS NULL OR total_weight = 0 THEN
            SET avg_weighted_score = 0;
        ELSE
            SET avg_weighted_score = total_score / total_weight;
        END IF;

        -- Update the average_score in the users table
        UPDATE users SET average_score = avg_weighted_score WHERE id = current_user_id;

    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;
