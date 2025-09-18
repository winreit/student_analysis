from typing import List, Dict, Any
from collections import defaultdict
from .base_report import BaseReport


class StudentPerformanceReport(BaseReport):

    def generate(self) -> List[Dict[str, Any]]:
        student_grades = defaultdict(list)

        for row in self.data:
            try:
                student_name = row['student_name']
                grade = int(row['grade'])
                student_grades[student_name].append(grade)
            except (KeyError, ValueError) as e:
                continue

        result = []
        for student, grades in student_grades.items():
            if grades:  # Проверяем, что есть оценки
                average_grade = sum(grades) / len(grades)
                result.append({
                    'student_name': student,
                    'average_grade': round(average_grade, 2)
                })

        result.sort(key=lambda x: x['average_grade'], reverse=True)

        return result