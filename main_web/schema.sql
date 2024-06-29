DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS Store; 
DROP TABLE IF EXISTS Product; 
DROP TABLE IF EXISTS ProductImages;    
DROP TABLE IF EXISTS CHATT;    
DROP TABLE IF EXISTS CHATTMESSAGES;
DROP TABLE IF EXISTS RECOMMENDATIONS;  
DROP TABLE IF EXISTS MODELS; 

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed password
    email VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),               
    last_name VARCHAR(50),                 
    date_of_birth DATE,                  
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    last_login TIMESTAMP,                 
    is_active BOOLEAN DEFAULT TRUE        
);     

CREATE TABLE Store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(50) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    website VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL, -- Increased length for better descriptions
    rating INTEGER NOT NULL CHECK (rating >= 0 AND rating <= 5), -- Rating constraint
    logo_path VARCHAR(255) 
);   

CREATE TABLE Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255) NOT NULL, -- Increased length for better descriptions
    price INTEGER NOT NULL CHECK (price >= 0), -- Price constraint
    rating INTEGER NOT NULL CHECK (rating >= 0 AND rating <= 5), -- Rating constraint
    store_id INTEGER NOT NULL,
    FOREIGN KEY (store_id) REFERENCES Store(id)
);  

CREATE TABLE ProductImages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(id)
);   

CREATE TABLE CHATT (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (store_id) REFERENCES Store(id)
);    

CREATE TABLE CHATTMESSAGES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    message VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES CHATT(id)
);

CREATE TABLE RECOMMENDATIONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);  

CREATE TABLE MODELS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT NOT NULL,   
    model_path VARCHAR(255) NOT NULL
);
