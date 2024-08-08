-- Create trigger to decrease item quantity after adding a new order
-- This trigger will activate after an INSERT operation on the orders table
-- It updates the quantity in the items table, reducing it by the number of items ordered
-- The quantity in the items table can become negative

DELIMITER //

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END//

DELIMITER ;
