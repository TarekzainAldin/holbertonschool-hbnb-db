CREATE TABLE City (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    state_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES State(id)
);