-- Drop tables if they already exist to allow for easy resetting
DROP TABLE IF EXISTS PUPIL CASCADE;
DROP TABLE IF EXISTS TEACHER CASCADE;

-- Create the TEACHER table first
CREATE TABLE IF NOT EXISTS TEACHER (
    TeacherID VARCHAR(10) NOT NULL,
    TeacherFullName VARCHAR(30),
    TeacherClass INT NOT NULL UNIQUE, -- UNIQUE belongs here so two teachers can't have the same class
    PRIMARY KEY (TeacherID),
    CONSTRAINT chk_teacher_id_format CHECK (
        LENGTH(TeacherID) BETWEEN 8 AND 10 
        AND TeacherID ~ '^[0-9]+$'
    ),
    CONSTRAINT chk_teacher_name_letters CHECK (
        TeacherFullName ~ '^[a-zA-Z\s]+$'
    )
);

-- Then create the PUPIL table
CREATE TABLE IF NOT EXISTS PUPIL (
    PupilID VARCHAR(10) NOT NULL,
    PupilFullName VARCHAR(30),
    PupilClass INT NOT NULL, 
    PRIMARY KEY (PupilID),
    CONSTRAINT chk_pupil_id_format CHECK (
        LENGTH(PupilID) BETWEEN 8 AND 10 
        AND PupilID ~ '^[0-9]+$'
    ),
    CONSTRAINT chk_pupil_name_letters CHECK (
        PupilFullName ~ '^[a-zA-Z\s]+$'
    )
);