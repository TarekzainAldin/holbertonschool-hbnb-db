CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    address VARCHAR(255),
    latitude FLOAT DEFAULT 0.0,
    longitude FLOAT DEFAULT 0.0,
    host_id VARCHAR(36) NOT NULL,
    city_id VARCHAR(36) NOT NULL,
    price_per_night INTEGER DEFAULT 0,
    number_of_rooms INTEGER DEFAULT 0,
    number_of_bathrooms INTEGER DEFAULT 0,
    max_guests INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (host_id) REFERENCES users(id)
);

