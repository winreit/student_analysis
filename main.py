import argparse
from reports.student_performance_report import StudentPerformanceReport
from utils.file_reader import read_csv_files


def main():
    parser = argparse.ArgumentParser(description='Анализ успеваемости студентов')
    parser.add_argument('--files', nargs='+', required=True,
                        help='Пути к CSV файлам с данными')
    parser.add_argument('--report', required=True,
                        help='Название отчета (student-performance)')

    args = parser.parse_args()

    data = read_csv_files(args.files)

    if args.report == 'student-performance':
        report = StudentPerformanceReport(data)
        result = report.generate()
        report.display(result)
    else:
        raise ValueError(f"Неизвестный тип отчета: {args.report}")


if __name__ == '__main__':
    main()