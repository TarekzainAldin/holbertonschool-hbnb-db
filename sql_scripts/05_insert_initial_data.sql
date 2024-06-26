INSERT INTO State (id, name) VALUES ('1', 'California');
INSERT INTO City (id, name, state_id) VALUES ('1', 'San Francisco', '1');
INSERT INTO User (id, email, password, is_admin) VALUES ('1', 'admin@example.com', 'hashed_password', TRUE);
