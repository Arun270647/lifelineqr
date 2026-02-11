USE lifelineqr;

DROP TABLE IF EXISTS medical_documents;

CREATE TABLE medical_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_data LONGTEXT NOT NULL,
    description VARCHAR(500) DEFAULT 'Medical Document',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);
