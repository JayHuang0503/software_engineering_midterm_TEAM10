chcp 65001
echo "當main.py執行後, ctrl+c來中斷(但不結束批次工作), 接著就會把資料加入資料庫(記得先刪除原先的資料庫)"
python .\main.py
python .\util\add_students.py
python .\util\add_courses.py
python .\util\auto_add_major.py