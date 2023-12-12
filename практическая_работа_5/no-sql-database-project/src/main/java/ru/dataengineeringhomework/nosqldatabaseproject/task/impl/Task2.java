package ru.dataengineeringhomework.nosqldatabaseproject.task.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;
import ru.dataengineeringhomework.nosqldatabaseproject.model.AggWithSortRequest;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.StatSalaryDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.writer.JsonFileWriter;
import ru.dataengineeringhomework.nosqldatabaseproject.task.Task;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Component
@RequiredArgsConstructor
public class Task2 implements Task {

    private final StatSalaryDataRepository statSalaryDataRepository;
    private final JsonFileWriter jsonFileWriter;

    @Override
    public void run() {
        writeMaxMinAvgBySalary();
        writeCountByJob();
        writeMaxMinAvgBySalaryGroupByCity();
        writeMaxMinAvgBySalaryGroupByJob();
        writeMaxMinAvgByAgeGroupByCity();
        writeMaxMinAvgByAgeGroupByJob();
        writeMaxSalaryForMinAge();
        writeMinSalaryForMaxAge();
        writeMaxMinAvgByAgeGroupByCityFilterBySalaryGreatThen50000SortAscByMin();
        writeMaxMinAvgInFilterByCityAndJobRangeFiltersByAge();
        writeRandomQuery();
    }

    private void writeMaxMinAvgBySalary() {
        var aggData = statSalaryDataRepository.getStatByField("salary");
        var nameFile = "maxMinAvgBySalary.json";
        jsonFileWriter.saveToFile(nameFile, aggData);
    }

    private void writeCountByJob() {
        var countByFieldList = statSalaryDataRepository.countByField("job");

        var countByJob = countByFieldList.stream().collect(Collectors.toMap(
                CountByField::value,
                CountByField::count
        ));

        var nameFile = "countByJob.json";
        jsonFileWriter.saveToFile(nameFile, countByJob);
    }

    private void writeMaxMinAvgBySalaryGroupByCity() {
        var aggDataByField = statSalaryDataRepository.getStatByFieldAndGroupByValue("salary", "city");

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "maxMinAvgBySalaryGroupByCity.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxMinAvgBySalaryGroupByJob() {
        var aggDataByField = statSalaryDataRepository.getStatByFieldAndGroupByValue("salary", "job");

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "maxMinAvgBySalaryGroupByJob.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxMinAvgByAgeGroupByCity() {
        var aggDataByField = statSalaryDataRepository.getStatByFieldAndGroupByValue("age", "city");

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "maxMinAvgByAgeGroupByCity.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxMinAvgByAgeGroupByJob() {
        var aggDataByField = statSalaryDataRepository.getStatByFieldAndGroupByValue("age", "job");

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "maxMinAvgByAgeGroupByJob.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxSalaryForMinAge() {
        var maxSalary = statSalaryDataRepository.getMaxValueByMinField("salary", "age");

        var result = Map.of("maxSalary", maxSalary);

        var nameFile = "maxSalaryForMinAge.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMinSalaryForMaxAge() {
        var minSalary = statSalaryDataRepository.getMinValueByMaxField("salary", "age");

        var result = Map.of("minSalary", minSalary);

        var nameFile = "minSalaryForMaxAge.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxMinAvgByAgeGroupByCityFilterBySalaryGreatThen50000SortAscByMin() {
        var aggDataByField = statSalaryDataRepository.getStatWithGreatThenFilterBySalaryAndGroupByFieldAndSort(
                50000,
                new AggWithSortRequest(
                        "age", "city", "min", Sort.Direction.ASC
                ));

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "maxMinAvgByAgeGroupByCityFilterBySalaryGreatThen50000SortAscByMin.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxMinAvgInFilterByCityAndJobRangeFiltersByAge() {
        var aggData = statSalaryDataRepository.getStatWithInFiltersAndRangeFilters(
                "salary",
                List.of(
                        new InFilter("city", List.of("Валенсия", "Белград", "Москва", "Мадрид")),
                        new InFilter("job", List.of("Инженер", "Врач", "Учитель", "Программист"))
                ),
                List.of(
                        new RangeFilter("age", 18, 25),
                        new RangeFilter("age", 50, 65)
                )
        );

        var nameFile = "maxMinAvgInFilterByCityAndJobRangeFiltersByAge.json";
        jsonFileWriter.saveToFile(nameFile, aggData);
    }

    private void writeRandomQuery() {
        var aggDataByField = statSalaryDataRepository.getStatWithGreatThenFilterBySalaryAndGroupByFieldAndSort(
                40000,
                new AggWithSortRequest(
                        "salary", "job", "max", Sort.Direction.DESC
                ));

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "randomQuery.json";
        jsonFileWriter.saveToFile(nameFile, result);

    }

    private Map<String, AggData> convertAggDataByFieldToMap(List<AggDataByField> aggDataByFields) {
        return aggDataByFields.stream()
                .collect(Collectors.toMap(
                        AggDataByField::value,
                        forValue -> new AggData(forValue.max(), forValue.min(), forValue.avg()),
                        (o1, o2) -> o1,
                        LinkedHashMap::new
                ));
    }

    @Override
    public Integer getNumberTask() {
        return 2;
    }
}
