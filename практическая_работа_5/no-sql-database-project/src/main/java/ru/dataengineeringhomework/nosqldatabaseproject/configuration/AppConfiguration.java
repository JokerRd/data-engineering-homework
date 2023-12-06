package ru.dataengineeringhomework.nosqldatabaseproject.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.ListableBeanFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import ru.dataengineeringhomework.nosqldatabaseproject.task.Task;

import java.util.Map;
import java.util.stream.Collectors;

@Configuration
public class AppConfiguration {

    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }

    @Bean
    public Map<Integer, Task> tasksByNumber(ListableBeanFactory beanFactory) {
        var tasks = beanFactory.getBeansOfType(Task.class);
        return tasks.values().stream()
                .collect(Collectors.toMap(
                        Task::getNumberTask,
                        forValue -> forValue
                ));
    }

}
