CREATE TABLE t_p60900679_quantum_data_analysi.leads (
    id SERIAL PRIMARY KEY,
    contact TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);