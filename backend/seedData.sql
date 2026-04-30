
INSERT INTO TEACHER (TeacherID, TeacherFullName, TeacherClass) VALUES
('312456789', 'David Levi', 1),
('204567812', 'Miriam Cohen', 2)
ON CONFLICT (TeacherID) DO NOTHING;

INSERT INTO PUPIL (PupilID, PupilFullName, PupilClass) VALUES
('325111001', 'Ariella Amar', 1), ('325111002', 'Benny Akerman', 1), ('325111003', 'Chaim Azoulay', 1), ('325111004', 'Dina Arad', 1), 
('325222011', 'Kobi Baruch', 2), ('325222012', 'Liat Barak', 2), ('325222013', 'Moti Benisty', 2), ('325222014', 'Nava Biton', 2)
ON CONFLICT (PupilID) DO NOTHING;