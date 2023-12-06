package ru.dataengineeringhomework.nosqldatabaseproject.command;

import lombok.RequiredArgsConstructor;
import org.springframework.shell.command.annotation.Command;
import org.springframework.shell.command.annotation.Option;
import ru.dataengineeringhomework.nosqldatabaseproject.task.Task;

import java.util.Map;

@Command
@RequiredArgsConstructor
public class RunCommand {

    private final Map<Integer, Task> tasksByNumber;
    @Command(command = "run")
    public String run(@Option Integer numberTask) {
        var taskForRun = tasksByNumber.get(numberTask);
        if (taskForRun == null) {
            return "Bad number task";
        } else {
            taskForRun.run();
            return "Complete task with number " + numberTask;
        }
    }
}
