-- Create a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average
-- weighted score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the total weighted score and the sum of the weights
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_weighted_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Calculate the average weighted score
    IF total_weight > 0 THEN
        SET total_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET total_weighted_score = 0;
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = total_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;
