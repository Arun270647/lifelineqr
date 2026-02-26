USE lifelineqr;

DROP TABLE IF EXISTS medical_documents;

CREATE TABLE medical_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_data LONGTEXT NOT NULL,
    description VARCHAR(500) DEFAULT 'Medical Document',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
