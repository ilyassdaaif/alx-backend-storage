DELIMITER //

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
    
    -- If no rows were affected (item doesn't exist), insert a new item with negative quantity
    IF ROW_COUNT() = 0 THEN
	INSERT INTO items (name, quantity)
	VALUES (NEW.item_name, -NEW.number);
    END IF;
END//

DELIMITER ;
