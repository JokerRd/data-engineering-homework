package ru.dataengineeringhomework.nosqldatabaseproject;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.shell.command.annotation.EnableCommand;
import ru.dataengineeringhomework.nosqldatabaseproject.command.RunCommand;


@SpringBootApplication
@EnableCommand(RunCommand.class)
@EnableMongoRepositories()
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
