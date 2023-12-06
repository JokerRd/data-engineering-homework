package ru.dataengineeringhomework.nosqldatabaseproject.task.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;
import ru.dataengineeringhomework.nosqldatabaseproject.writer.JsonFileWriter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.CountData;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.SimpleSalaryDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.task.Task;

import java.util.List;

import static org.springframework.data.domain.Sort.by;


@Component
@RequiredArgsConstructor
public class Task1 implements Task {

    private final SimpleSalaryDataRepository simpleSalaryDataRepository;
    private final JsonFileWriter jsonFileWriter;

    @Override
    public void run() {
        writeToJsonFirstTenRecordsAndSortDescBySalary();
        writeToJsonFirstFifteenRecordsSortedDescBySalaryAndFilteredByAgeLessThirty();
        writeToJsonFirstTenRecordsSortedAscByAgeAndFilteredByEqualsOneCityAndInJobCollections();
        writeToJsonCountByDifficultFilter();
    }

    @Override
    public Integer getNumberTask() {
        return 1;
    }

    private void writeToJsonFirstTenRecordsAndSortDescBySalary() {
        var salaryData = simpleSalaryDataRepository.getAllSortedAndLimited(10, by(Sort.Direction.DESC, "salary"));
        var nameFile = "first10AndSortSalaryDesc.json";
        jsonFileWriter.saveToFile(nameFile, salaryData);
    }

    private void writeToJsonFirstFifteenRecordsSortedDescBySalaryAndFilteredByAgeLessThirty() {
        var salaryData = simpleSalaryDataRepository.getByLessAge(30,15, by(Sort.Direction.DESC, "salary"));
        var nameFile = "first15AndSortSalaryDescAndFilterAgeLess30.json";
        jsonFileWriter.saveToFile(nameFile, salaryData);
    }

    private void writeToJsonFirstTenRecordsSortedAscByAgeAndFilteredByEqualsOneCityAndInJobCollections() {
        var salaryData = simpleSalaryDataRepository.getByEqualsCityAndInJobsCollections(
                "Москва",
                List.of("Врач", "Инженер", "Продавец"),
                10, by(Sort.Direction.ASC, "age"));
        var nameFile = "first10AndSortAscAgeAndFilterEqCityAndFilterInJobs.json";
        jsonFileWriter.saveToFile(nameFile, salaryData);
    }

    private void writeToJsonCountByDifficultFilter() {
        var count = simpleSalaryDataRepository.countByDifficultFilter();
        var nameFile = "countByDifficultFilter.json";
        var countData = new CountData(count);
        jsonFileWriter.saveToFile(nameFile, countData);
    }

}
