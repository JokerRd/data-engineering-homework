package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.AggWithSortRequest;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.SalaryData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.CommonRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.SalarySpringDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.StatSalaryDataRepository;

import java.util.List;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;

@Repository
@RequiredArgsConstructor
public class StatSalaryDataMongoRepository implements StatSalaryDataRepository {

    private final SalarySpringDataRepository salarySpringDataRepository;
    private final MongoTemplate mongoTemplate;
    private final CommonRepository commonRepository;


    @Override
    public AggData getStatByField(String nameField) {
        return commonRepository.getStatByField(nameField, "salary_data");
    }

    @Override
    public List<CountByField> countByField(String nameField) {
        return commonRepository.countByField(nameField, "salary_data");
    }

    @Override
    public List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup) {
        return commonRepository.getStatByFieldAndGroupByValue(nameField, nameFieldForGroup, "salary_data");
    }

    @Override
    public int getMaxValueByMinField(String maxNameField, String minNameField) {
        return commonRepository.getMaxValueByMinField(maxNameField, minNameField, "salary_data");
    }

    @Override
    public int getMinValueByMaxField(String minNameField, String maxNameField) {
        return commonRepository.getMinValueByMaxField(minNameField, maxNameField, "salary_data");
    }

    @Override
    public List<AggDataByField> getStatWithGreatThenFilterBySalaryAndGroupByFieldAndSort(Integer salary,
                                                                                         AggWithSortRequest aggWithSortRequest) {
        var matchOperation = match(Criteria.where("salary").gt(salary));
        var aggOperation = group(aggWithSortRequest.groupNameField())
                .min(aggWithSortRequest.aggNameField()).as("min")
                .max(aggWithSortRequest.aggNameField()).as("max")
                .avg(aggWithSortRequest.aggNameField()).as("avg");
        var sortOperation = sort(aggWithSortRequest.direction(), aggWithSortRequest.sortNameField());
        var projectionOperation = project()
                .andExpression("_id").as("value")
                .andExpression("max").as("max")
                .andExpression("min").as("min")
                .andExpression("avg").as("avg");
        var aggregation = newAggregation(matchOperation, aggOperation, sortOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, AggDataByField.class);
        return result.getMappedResults();
    }

    @Override
    public AggData getStatWithInFiltersAndRangeFilters(String aggNameField, List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        var matchOperator = match(prepareCriteriaForInFiltersAndRangeFilters(inFilters, rangeFilters));

        var aggOperation = group()
                .min(aggNameField).as("min")
                .max(aggNameField).as("max")
                .avg(aggNameField).as("avg");
        var aggregation = newAggregation(matchOperator, aggOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, AggData.class);
        return result.getUniqueMappedResult();
    }


    @Override
    public List<SalaryData> multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter) {
        return commonRepository.multiplyFieldByInFilters(multiplyNameField, multiplier, inFilter, SalaryData.class);
    }

    @Override
    public List<SalaryData> multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier,
                                                                    List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        return commonRepository.multiplyFieldByInFiltersAndRangeFilters(multiplyNameField, multiplier,
                inFilters, rangeFilters, SalaryData.class);
    }

    @Override
    public List<SalaryData> deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        return commonRepository.deleteByInFiltersAndRangeFilters(inFilters, rangeFilters, SalaryData.class);
    }

    private Criteria prepareCriteriaForInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        var criteria = inFilters.stream()
                .map(inFilter -> Criteria.where(inFilter.nameField()).in(inFilter.values()))
                .reduce(Criteria::andOperator).get();

        var rangeList = rangeFilters.stream()
                .map(rangeFilter -> Criteria.where(rangeFilter.name()).gt(rangeFilter.from()).lt(rangeFilter.to()))
                .toList();

        criteria.orOperator(rangeList);
        return criteria;
    }
}
