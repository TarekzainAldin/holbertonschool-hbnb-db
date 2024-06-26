-- Example initial data
INSERT INTO states (id, name) VALUES ('1', 'California');
INSERT INTO cities (id, name, state_id) VALUES ('1', 'San Francisco', '1');
INSERT INTO users (id, email, password, is_admin) VALUES ('1', 'admin@example.com', 'hashed_password', TRUE);
INSERT INTO amenities (id, name) VALUES ('1', 'Wi-Fi'), ('2', 'Pool'), ('3', 'Parking');
