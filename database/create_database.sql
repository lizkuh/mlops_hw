CREATE DATABASE model_db;

-- CREATE TABLE model_db.model_signature
-- (
--     "model_type"            TEXT PRIMARY KEY,
--     "fit_params_json"       TEXT,
--     "python_library_path"   TEXT
-- );

-- CREATE TABLE model_db.model_instance
-- (
--     "model_name"            TEXT PRIMARY KEY,
--     "model_type"       TEXT,
--     "fit_params_json"   TEXT,
--     "python_library_path" TEXT,
--     "model_bin"  BYTEA,
--     "features"   TEXT,
--     "target_column" TEXT PRIMARY KEY,
-- );
-- CREATE TABLE model_db.model_instance
-- (
--     "model_name"            TEXT PRIMARY KEY,
--     "model_type"       TEXT,
--     "fit_params_json"   TEXT,
--     "python_library_path" TEXT,
--     "model_bin"  BYTEA,
--     "features"   TEXT,
--     "target_column" TEXT PRIMARY KEY,
-- );