package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
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
import ru.dataengineeringhomework.nosqldatabaseproject.repository.SalarySpringDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.StatSalaryDataRepository;

import java.util.List;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;

@Repository
@RequiredArgsConstructor
public class StatSalaryDataMongoRepository implements StatSalaryDataRepository {

    private final SalarySpringDataRepository salarySpringDataRepository;
    private final MongoTemplate mongoTemplate;


    @Override
    public AggData getStatByField(String nameField) {
        var aggOperation = group().min(nameField).as("min")
                .max(nameField).as("max")
                .avg(nameField).as("avg");
        var aggregation = newAggregation(aggOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, AggData.class);
        return result.getUniqueMappedResult();
    }

    @Override
    public List<CountByField> countByField(String nameField) {
        var countOperation = group(nameField).count().as("count");
        var projectionOperation = project()
                .andExpression("_id").as("value")
                .andExpression("count").as("count");

        var aggregation = newAggregation(countOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, CountByField.class);
        return result.getMappedResults();
    }

    @Override
    public List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup) {
        var aggOperation = group(nameFieldForGroup)
                .min(nameField).as("min")
                .max(nameField).as("max")
                .avg(nameField).as("avg");
        var projectionOperation = project()
                .andExpression("_id").as("value")
                .andExpression("max").as("max")
                .andExpression("min").as("min")
                .andExpression("avg").as("avg");

        var aggregation = newAggregation(aggOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, AggDataByField.class);
        return result.getMappedResults();
    }

    @Override
    public int getMaxValueByMinField(String maxNameField, String minNameField) {
        var sortOperation = sort(Sort.Direction.ASC, minNameField).and(Sort.Direction.DESC, maxNameField);
        var limitOperation = limit(1);
        var projectionOperation = project()
                .andExpression(maxNameField).as("max");
        var aggregation = newAggregation(sortOperation, limitOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, AggData.class);
        return result.getUniqueMappedResult().max();
    }

    @Override
    public int getMinValueByMaxField(String minNameField, String maxNameField) {
        var sortOperation = sort(Sort.Direction.DESC, maxNameField).and(Sort.Direction.ASC, minNameField);
        var limitOperation = limit(1);
        var projectionOperation = project()
                .andExpression(minNameField).as("min");
        var aggregation = newAggregation(sortOperation, limitOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, SalaryData.class, AggData.class);
        return result.getUniqueMappedResult().min();
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

    @Override
    public List<SalaryData> multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter) {
        var query = Query.query(Criteria.where(inFilter.nameField()).in(inFilter.values()));
        mongoTemplate
                .update(SalaryData.class)
                .matching(query)
                .apply(new Update().multiply(multiplyNameField, multiplier))
                .all();

        return mongoTemplate.find(query, SalaryData.class);
    }

    @Override
    public List<SalaryData> multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier,
                                                                    List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        var criteria = prepareCriteriaForInFiltersAndRangeFilters(inFilters, rangeFilters);
        var query = Query.query(criteria);
        mongoTemplate
                .update(SalaryData.class)
                .matching(query)
                .apply(new Update().multiply(multiplyNameField, multiplier))
                .all();

        return mongoTemplate.find(query, SalaryData.class);
    }

    @Override
    public List<SalaryData> deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        var criteria = prepareCriteriaForInFiltersAndRangeFilters(inFilters, rangeFilters);
        var query = Query.query(criteria);
        return mongoTemplate.findAllAndRemove(query, SalaryData.class);
    }
}
