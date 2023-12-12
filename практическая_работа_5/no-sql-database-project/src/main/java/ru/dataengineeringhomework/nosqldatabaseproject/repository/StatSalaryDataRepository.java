package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import ru.dataengineeringhomework.nosqldatabaseproject.model.AggWithSortRequest;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.SalaryData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;

import java.util.List;

public interface StatSalaryDataRepository {

    AggData getStatByField(String nameField);

    List<CountByField> countByField(String nameField);

    List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup);

    int getMaxValueByMinField(String maxNameField, String minNameField);

    int getMinValueByMaxField(String minNameField, String maxNameField);

    List<AggDataByField> getStatWithGreatThenFilterBySalaryAndGroupByFieldAndSort(Integer salary,
                                                                                  AggWithSortRequest aggWithSortRequest);

    AggData getStatWithInFiltersAndRangeFilters(String aggNameField, List<InFilter> inFilters, List<RangeFilter> rangeFilters);

    List<SalaryData> multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter);

    List<SalaryData> multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier,
                                                             List<InFilter> inFilter, List<RangeFilter> rangeFilters);

    List<SalaryData> deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters);
}
