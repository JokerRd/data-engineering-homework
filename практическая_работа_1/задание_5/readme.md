Входные данные подкладываются в папку resources.

Варианты запуска:  
- для запуска программы надо собрать maven проект из дериктории exercise-one с помощью
команды mvn clean install(можно не собирать, jar уже лежит рядом с проектом, название app.jar)
- далее с помощью команды java -jar имя_jar_файла_из_папки_target(илл app.jar если берется готовый jar-ник) можно запустить программу
- при запуске можно передать аргумент с путем куда сохранять данные, пример:
java -jar .\target\exercise-five-1.0.jar C:\test\result.csv, если аргумент не передать, то по умолчанию
будет создаваться файл result.csv в директории из которой запустили программу