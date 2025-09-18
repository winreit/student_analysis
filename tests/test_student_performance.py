import os
import sys
import pytest
import tempfile
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_reader import read_csv_files
from reports.student_performance_report import StudentPerformanceReport


@pytest.fixture
def sample_csv_data() -> str:
    return """student_name,subject,teacher_name,date,grade
Семенова Елена,Английский язык,Ковалева Анна,2023-10-10,5
Титов Владислав,География,Орлов Сергей,2023-10-12,4
Власова Алина,Биология,Ткаченко Наталья,2023-10-15,5
Семенова Елена,Математика,Иванов Петр,2023-10-16,4
Титов Владислав,Физика,Сидоров Иван,2023-10-17,3"""


@pytest.fixture
def empty_csv_data() -> str:
    return "student_name,subject,teacher_name,date,grade"


@pytest.fixture
def invalid_grade_csv_data() -> str:
    return """student_name,subject,teacher_name,date,grade
Семенова Елена,Английский язык,Ковалева Анна,2023-10-10,5
Титов Владислав,География,Орлов Сергей,2023-10-12,invalid
Власова Алина,Биология,Ткаченко Наталья,2023-10-15,5"""


@pytest.fixture
def multiple_files_data() -> tuple[str, str]:
    file1 = """student_name,subject,teacher_name,date,grade
Семенова Елена,Английский язык,Ковалева Анна,2023-10-10,5
Титов Владислав,География,Орлов Сергей,2023-10-12,4"""

    file2 = """student_name,subject,teacher_name,date,grade
Власова Алина,Биология,Ткаченко Наталья,2023-10-15,5
Семенова Елена,Математика,Иванов Петр,2023-10-16,4"""

    return file1, file2


@pytest.fixture
def create_temp_csv():
    def _create_temp_csv(content: str) -> str:
        fd, path = tempfile.mkstemp(suffix='.csv')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
            return path
        except:
            os.unlink(path)
            raise

    return _create_temp_csv


@pytest.fixture
def student_performance_report(sample_csv_data, create_temp_csv):
    file_path = create_temp_csv(sample_csv_data)
    data = read_csv_files([file_path])
    report = StudentPerformanceReport(data)

    yield report

    # Cleanup
    os.unlink(file_path)


class TestStudentPerformanceReport:

    def test_report_generation(self, student_performance_report):
        result = student_performance_report.generate()

        assert len(result) == 3
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    def test_report_sorting(self, student_performance_report):
        result = student_performance_report.generate()

        assert result[0]['student_name'] == 'Власова Алина'
        assert result[0]['average_grade'] == 5.0

        assert result[1]['student_name'] == 'Семенова Елена'
        assert result[1]['average_grade'] == 4.5

        assert result[2]['student_name'] == 'Титов Владислав'
        assert result[2]['average_grade'] == 3.5

    def test_empty_data(self):
        report = StudentPerformanceReport([])
        result = report.generate()
        assert result == []

    @pytest.mark.parametrize("csv_content,expected_students", [
        ("""student_name,subject,teacher_name,date,grade
Семенова Елена,Английский язык,Ковалева Анна,2023-10-10,5
Титов Владислав,География,Орлов Сергей,2023-10-12,4""",
         ['Семенова Елена', 'Титов Владислав']),

        ("""student_name,subject,teacher_name,date,grade
Власова Алина,Биология,Ткаченко Наталья,2023-10-15,5""",
         ['Власова Алина']),

        ("""student_name,subject,teacher_name,date,grade
Петров Иван,Химия,Смирнова Ольга,2023-10-18,5
Сидорова Мария,Физика,Кузнецов Дмитрий,2023-10-19,4""",
         ['Петров Иван', 'Сидорова Мария'])
    ])
    def test_different_data_scenarios(self, create_temp_csv, csv_content, expected_students):
        file_path = create_temp_csv(csv_content)

        try:
            data = read_csv_files([file_path])
            report = StudentPerformanceReport(data)
            result = report.generate()

            assert len(result) == len(expected_students)
            student_names = [student['student_name'] for student in result]
            assert set(student_names) == set(expected_students)

        finally:
            os.unlink(file_path)

    @pytest.mark.parametrize("grades,expected_average", [
        ([5, 5], 5.0),
        ([4, 5], 4.5),
        ([3, 4, 5], 4.0),
        ([2, 3, 4], 3.0),
        ([5], 5.0)
    ])
    def test_average_calculation(self, create_temp_csv, grades, expected_average):
        csv_content = "student_name,subject,teacher_name,date,grade\n"
        for i, grade in enumerate(grades):
            csv_content += f"Тестовый Студент,Предмет {i},Учитель {i},2023-10-{10 + i},{grade}\n"

        file_path = create_temp_csv(csv_content)

        try:
            data = read_csv_files([file_path])
            report = StudentPerformanceReport(data)
            result = report.generate()

            assert len(result) == 1
            assert result[0]['average_grade'] == expected_average

        finally:
            os.unlink(file_path)


class TestFileReader:

    def test_read_single_file(self, sample_csv_data, create_temp_csv):
        file_path = create_temp_csv(sample_csv_data)

        try:
            data = read_csv_files([file_path])

            assert len(data) == 5
            assert all('student_name' in row for row in data)
            assert all('grade' in row for row in data)

        finally:
            os.unlink(file_path)

    def test_read_multiple_files(self, multiple_files_data, create_temp_csv):
        file1_content, file2_content = multiple_files_data
        file_path1 = create_temp_csv(file1_content)
        file_path2 = create_temp_csv(file2_content)

        try:
            data = read_csv_files([file_path1, file_path2])

            assert len(data) == 4
            student_names = [row['student_name'] for row in data]
            assert 'Семенова Елена' in student_names
            assert 'Титов Владислав' in student_names
            assert 'Власова Алина' in student_names

        finally:
            os.unlink(file_path1)
            os.unlink(file_path2)

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            read_csv_files(["nonexistent_file.csv"])



if __name__ == '__main__':
    pytest.main([__file__, '-v'])