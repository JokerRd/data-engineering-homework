package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Repository;
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
        return 0;
    }
}
