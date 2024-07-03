CREATE TABLE User (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Role (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE UserRole (
    user_id VARCHAR(36),
    role_id VARCHAR(36),
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (role_id) REFERENCES Role(id)
);

-- Insérer des données initiales
INSERT INTO Role (id, name, description) VALUES ('1', 'admin', 'Administrator role');
INSERT INTO Role (id, name, description) VALUES ('2', 'user', 'Standard user role');


 Place table
CREATE TABLE Place (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    city_id VARCHAR(36),
    country_id VARCHAR(36),
    owner_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES City(id),
    FOREIGN KEY (country_id) REFERENCES Country(id),
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

-- Amenity table
CREATE TABLE Amenity (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Place-Amenity relationship table
CREATE TABLE PlaceAmenity (
    id VARCHAR(36) PRIMARY KEY,
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

-- City table
CREATE TABLE City (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id VARCHAR(36),
    FOREIGN KEY (country_id) REFERENCES Country(id)
);

-- Country table
CREATE TABLE Country (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
INSERT INTO Amenity (id, name)
VALUES 
    ('1', 'Wi-Fi'),
    ('2', 'Pool'),
    ('3', 'Gym'),
    ('4', 'Parking'),
    ('5', 'Air Conditioning');

-- Insert initial data into Country table
INSERT INTO Country (id, name)
VALUES 
    ('1', 'United States'),
    ('2', 'France'),
    ('3', 'Spain');

-- Insert initial data into City table
INSERT INTO City (id, name, country_id)
VALUES 
    ('1', 'New York', '1'),
    ('2', 'Paris', '2'),
    ('3', 'Barcelona', '3');

-- Insert initial data into Place table
INSERT INTO Place (id, title, description, price, city_id, country_id, owner_id)
VALUES 
    ('1', 'Luxury Apartment in Manhattan', 'Central location with stunning views', 250.00, '1', '1', '2'),
    ('2', 'Charming Studio in Montmartre', 'Historic neighborhood close to attractions', 120.00, '2', '2', '1');

-- Insert initial data into PlaceAmenity table (example data)
INSERT INTO PlaceAmenity (id, place_id, amenity_id)
VALUES 
    ('1', '1', '1'),
    ('2', '1', '2'),
    ('3', '1', '4'),
    ('4', '2', '1'),
    ('5', '2', '5');