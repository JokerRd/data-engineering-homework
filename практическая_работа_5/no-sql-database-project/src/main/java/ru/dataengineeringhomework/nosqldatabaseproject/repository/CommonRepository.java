package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.SalaryData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;

import java.util.List;

public interface CommonRepository {

    AggData getStatByField(String nameField, String collectionName);

    List<CountByField> countByField(String nameField, String collectionName);

    List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup, String collectionName);

    int getMaxValueByMinField(String maxNameField, String minNameField, String collectionName);

    int getMinValueByMaxField(String minNameField, String maxNameField, String collectionName);

    <T> List<T> deleteByLessThanOrGreatThen(String nameField, Integer lessThen, Integer greatThen, Class<T> dataClass);

    <T> List<T> incrementByField(String name, Class<T> dataClass);

    <T> List<T>  multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter, Class<T> dataClass);

    <T> List<T>  multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier,
                                                             List<InFilter> inFilter, List<RangeFilter> rangeFilters,
                                                         Class<T> dataClass);

    <T> List<T>  deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters,
                                                  Class<T> dataClass);

}
