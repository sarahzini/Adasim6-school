-- Reset everything
DROP TABLE IF EXISTS PUPIL CASCADE;
DROP TABLE IF EXISTS TEACHER CASCADE;
DROP TABLE IF EXISTS PERSON CASCADE;

-- The Mother Table: All IDs are registered here first
CREATE TABLE PERSON (
    ID VARCHAR(10) PRIMARY KEY,
    FullName VARCHAR(30) NOT NULL,
    UserType VARCHAR(10) NOT NULL CHECK (UserType IN ('pupil', 'teacher')),
    
    -- Global constraints to apply both on pupils and teachers
    CONSTRAINT chk_id_format CHECK (
        LENGTH(ID) BETWEEN 8 AND 10 
        AND ID ~ '^[0-9]+$'
    ),
    CONSTRAINT chk_name_letters CHECK (
        FullName ~ '^[a-zA-Z\s]+$'
    )
);

--  The Teacher Table: Inherits ID from PERSON
CREATE TABLE TEACHER (
    TeacherID VARCHAR(10) PRIMARY KEY REFERENCES PERSON(ID) ON DELETE CASCADE,
    TeacherClass INT NOT NULL UNIQUE -- Unique for teachers
);

-- The Pupil Table: Inherits ID from PERSON
CREATE TABLE PUPIL (
    PupilID VARCHAR(10) PRIMARY KEY REFERENCES PERSON(ID) ON DELETE CASCADE,
    PupilClass INT NOT NULL
);
 
-- Person Location Table: Stores the latest location of each person
CREATE TABLE IF NOT EXISTS PERSON_LOCATION (
    ID VARCHAR(10) PRIMARY KEY REFERENCES PERSON(ID),
    Latitude VARCHAR(10) NOT NULL, 
    Longitude VARCHAR(10) NOT NULL, 
    LastUpdate TIMESTAMP NOT NULL
);