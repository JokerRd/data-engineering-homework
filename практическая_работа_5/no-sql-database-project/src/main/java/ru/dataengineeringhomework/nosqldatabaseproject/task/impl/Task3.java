package ru.dataengineeringhomework.nosqldatabaseproject.task.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.SimpleSalaryDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.StatSalaryDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.task.Task;
import ru.dataengineeringhomework.nosqldatabaseproject.writer.JsonFileWriter;

import java.util.List;

@Component
@RequiredArgsConstructor
public class Task3 implements Task {

    private final SimpleSalaryDataRepository simpleSalaryDataRepository;
    private final StatSalaryDataRepository statSalaryDataRepository;
    private final JsonFileWriter jsonFileWriter;

    @Override
    public void run() {
        deleteAndWriteSalaryLessThen25000OrGreatThen175000();
        incrementAgeBy1AndWrite();
        upSalaryForJobsByFivePercentAndWrite();
        upSalaryForCitiesBySevenPercentAndWrite();
        upSalaryByTenPercentWithHardFilterAndWrite();
        deleteByRandomQueryAndWrite();
    }

    private void deleteAndWriteSalaryLessThen25000OrGreatThen175000() {
        var deleteResult = simpleSalaryDataRepository.deleteByLessThanOrGreatThen("salary", 25000, 175000);

        var nameFile = "deletedSalaryLessThen25000OrGreatThen175000.json";
        jsonFileWriter.saveToFile(nameFile, deleteResult);
    }

    private void incrementAgeBy1AndWrite() {
        var updatedResult = simpleSalaryDataRepository.incrementByField("age");

        var nameFile = "incrementAgeBy1.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void upSalaryForJobsByFivePercentAndWrite() {
        var updatedResult = statSalaryDataRepository.multiplyFieldByInFilters(
                "salary",
                1.05,
                new InFilter("job", List.of("Инженер", "Врач", "Учитель", "Программист"))
        );

        var nameFile = "upSalaryForJobsByFivePercent.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void upSalaryForCitiesBySevenPercentAndWrite() {
        var updatedResult = statSalaryDataRepository.multiplyFieldByInFilters(
                "salary",
                1.07,
                new InFilter("city", List.of("Валенсия", "Белград", "Москва", "Мадрид"))
        );

        var nameFile = "upSalaryForCitiesBySevenPercent.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void upSalaryByTenPercentWithHardFilterAndWrite() {
        var updatedResult = statSalaryDataRepository.multiplyFieldByInFiltersAndRangeFilters(
                "salary",
                1.1,
                List.of(
                        new InFilter("city", List.of("Валенсия", "Белград", "Москва", "Мадрид")),
                        new InFilter("job", List.of("Инженер", "Врач", "Учитель", "Программист"))
                ),
                List.of(
                        new RangeFilter("age", 18, 25),
                        new RangeFilter("age", 50, 65)
                )
        );

        var nameFile = "upSalaryByTenPercentWithHardFilter.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void deleteByRandomQueryAndWrite() {
        var deleteResult = statSalaryDataRepository.deleteByInFiltersAndRangeFilters(
                List.of(
                        new InFilter("city", List.of("Валенсия", "Белград", "Москва", "Мадрид")),
                        new InFilter("job", List.of("Инженер", "Врач", "Учитель", "Программист"))
                ),
                List.of(
                        new RangeFilter("age", 18, 25),
                        new RangeFilter("age", 50, 65)
                ));

        var nameFile = "deleteByRandomQuery.json";
        jsonFileWriter.saveToFile(nameFile, deleteResult);
    }

    @Override
    public Integer getNumberTask() {
        return 3;
    }
}
