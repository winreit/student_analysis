1. Создайте виртуальное окружение и активируйте его:
  
   Для macOS/Linux
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```
   Для Windows
   ```bash
   python -m venv myenv
   myenv\Scripts\activate
   ```
   
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запуск проекта:
   ```bash
   student_analysis % python main.py --files csv-files/students1.csv csv-files/students2.csv --report student-performance
   ```

4. Запуск тестов:
   ```bash
   pytest -v
   ```

   Скриншоты с примерами запуска тестов и запуска приложения в директории 'screenshots'
