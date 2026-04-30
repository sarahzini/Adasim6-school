-- This table prevents duplicates between roles
INSERT INTO PERSON (ID, FullName, UserType) VALUES
-- Teachers
('312456789', 'David Levi', 'teacher'),
('204567812', 'Miriam Cohen', 'teacher'),
-- Pupils
('325111001', 'Ariella Amar', 'pupil'),
('325111002', 'Benny Akerman', 'pupil'),
('325111003', 'Chaim Azoulay', 'pupil'),
('325111004', 'Dina Arad', 'pupil'),
('325222011', 'Kobi Baruch', 'pupil'),
('325222012', 'Liat Barak', 'pupil'),
('325222013', 'Moti Benisty', 'pupil'),
('325222014', 'Nava Biton', 'pupil')
ON CONFLICT (ID) DO NOTHING;

-- The ID must already exist in the PERSON and TEACHER table (foreign key)

INSERT INTO TEACHER (TeacherID, TeacherClass) VALUES
('312456789', 1),
('204567812', 2)
ON CONFLICT (TeacherID) DO NOTHING;

INSERT INTO PUPIL (PupilID, PupilClass) VALUES
('325111001', 1), ('325111002', 1), ('325111003', 1), ('325111004', 1),
('325222011', 2), ('325222012', 2), ('325222013', 2), ('325222014', 2)
ON CONFLICT (PupilID) DO NOTHING;

INSERT INTO PERSON_LOCATION (ID, Latitude, Longitude, LastUpdate) VALUES
('312456789', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('204567812', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325111001', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325111002', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325111003', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325111004', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325222011', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325222012', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325222013', '32 05 23', '34 46 44', '2026-04-30 14:50:00'),
('325222014', '32 05 23', '34 46 44', '2026-04-30 14:50:00');