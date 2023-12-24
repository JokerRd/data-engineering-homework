package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.CommonRepository;

import java.util.List;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;

@Repository
@RequiredArgsConstructor
public class CommonRepositoryImpl implements CommonRepository {

    private final MongoTemplate mongoTemplate;

    @Override
    public AggData getStatByField(String nameField, String collectionName) {
        var aggOperation = group().min(nameField).as("min")
                .max(nameField).as("max")
                .avg(nameField).as("avg");
        var aggregation = newAggregation(aggOperation);
        var result = mongoTemplate.aggregate(aggregation, collectionName, AggData.class);
        return result.getUniqueMappedResult();
    }

    @Override
    public List<CountByField> countByField(String nameField, String collectionName) {
        var countOperation = group(nameField).count().as("count");
        var projectionOperation = project()
                .andExpression("_id").as("value")
                .andExpression("count").as("count");

        var aggregation = newAggregation(countOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, collectionName, CountByField.class);
        return result.getMappedResults();
    }

    @Override
    public List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup, String collectionName) {
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
        var result = mongoTemplate.aggregate(aggregation, collectionName, AggDataByField.class);
        return result.getMappedResults();
    }

    @Override
    public int getMaxValueByMinField(String maxNameField, String minNameField, String collectionName) {
        var sortOperation = sort(Sort.Direction.ASC, minNameField).and(Sort.Direction.DESC, maxNameField);
        var limitOperation = limit(1);
        var projectionOperation = project()
                .andExpression(maxNameField).as("max");
        var aggregation = newAggregation(sortOperation, limitOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, collectionName, AggData.class);
        return result.getUniqueMappedResult().max();
    }

    @Override
    public int getMinValueByMaxField(String minNameField, String maxNameField, String collectionName) {
        var sortOperation = sort(Sort.Direction.DESC, maxNameField).and(Sort.Direction.ASC, minNameField);
        var limitOperation = limit(1);
        var projectionOperation = project()
                .andExpression(minNameField).as("min");
        var aggregation = newAggregation(sortOperation, limitOperation, projectionOperation);
        var result = mongoTemplate.aggregate(aggregation, collectionName, AggData.class);
        return result.getUniqueMappedResult().min();
    }

    @Override
    public <T> List<T> deleteByLessThanOrGreatThen(String nameField, Integer lessThen, Integer greatThen, Class<T> dataClass) {
        var query = Query.query(
                new Criteria().orOperator(
                        Criteria.where(nameField).lt(lessThen),
                        Criteria.where(nameField).gt(greatThen)
                )
        );
        return mongoTemplate.findAllAndRemove(query, dataClass);
    }

    @Override
    public <T> List<T> incrementByField(String name, Class<T> dataClass) {
        var updateResult = mongoTemplate
                .update(dataClass)
                .apply(new Update().inc(name, 1))
                .all();

        return mongoTemplate.findAll(dataClass);
    }

    @Override
    public <T> List<T> multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter, Class<T> dataClass) {
        var query = Query.query(Criteria.where(inFilter.nameField()).in(inFilter.values()));
        mongoTemplate
                .update(dataClass)
                .matching(query)
                .apply(new Update().multiply(multiplyNameField, multiplier))
                .all();

        return mongoTemplate.find(query, dataClass);
    }

    @Override
    public <T> List<T> multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier,
                                                               List<InFilter> inFilters, List<RangeFilter> rangeFilters,
                                                               Class<T> dataClass) {
        var criteria = prepareCriteriaForInFiltersAndRangeFilters(inFilters, rangeFilters);
        var query = Query.query(criteria);
        mongoTemplate
                .update(dataClass)
                .matching(query)
                .apply(new Update().multiply(multiplyNameField, multiplier))
                .all();

        return mongoTemplate.find(query, dataClass);
    }

    @Override
    public <T> List<T> deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters,
                                                        Class<T> dataClass) {
        var criteria = prepareCriteriaForInFiltersAndRangeFilters(inFilters, rangeFilters);
        var query = Query.query(criteria);
        return mongoTemplate.findAllAndRemove(query, dataClass);
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
