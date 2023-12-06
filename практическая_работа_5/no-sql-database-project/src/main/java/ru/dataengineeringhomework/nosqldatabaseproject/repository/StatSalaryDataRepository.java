package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;

import java.util.List;

public interface StatSalaryDataRepository {

    AggData getStatByField(String nameField);

    List<CountByField> countByField(String nameField);

    List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup);

    int getMaxValueByMinField(String maxNameField, String minNameField);

}
