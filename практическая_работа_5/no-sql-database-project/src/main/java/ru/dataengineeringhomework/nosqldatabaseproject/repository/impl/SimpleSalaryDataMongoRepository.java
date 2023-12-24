package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import com.mongodb.client.result.UpdateResult;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.SalaryData;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.CommonRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.SimpleSalaryDataRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.SalarySpringDataRepository;

import java.util.List;

import static org.springframework.data.domain.PageRequest.of;

@Repository
@RequiredArgsConstructor
public class SimpleSalaryDataMongoRepository implements SimpleSalaryDataRepository {

    private final SalarySpringDataRepository salarySpringDataRepository;
    private final MongoTemplate mongoTemplate;
    private final CommonRepository commonRepository;

    @Override
    public List<SalaryData> getAllSortedAndLimited(int limit, Sort sort) {
        var pageRequest = of(0, limit, sort);
        return salarySpringDataRepository.findAll(pageRequest).getContent();
    }

    public List<SalaryData> getByLessAge(int age, int limit, Sort sort) {
        var pageRequest = of(0, limit, sort);
        var query = Query.query(
                Criteria.where("age").lt(age)
        ).with(pageRequest);
        return mongoTemplate.find(query, SalaryData.class);
    }

    public List<SalaryData> getByEqualsCityAndInJobsCollections(String city, List<String> jobs, int limit, Sort sort) {
        var pageRequest = of(0, limit, sort);
        var query = Query.query(
                Criteria.where("city").is(city)
                        .and("value").in(jobs)
        ).with(pageRequest);
        return mongoTemplate.find(query, SalaryData.class);
    }

    @Override
    public long countByDifficultFilter() {
        var firstSalaryCriteria = Criteria.where("salary").gt(50000).lte(75000);
        var secondSalaryCriteria = Criteria.where("salary").gt(125000).lte(150000);

        var query = Query.query(
                Criteria.where("age").gte(20).lte(30)
                        .and("year").gte(2019).lte(2022)
                        .orOperator(firstSalaryCriteria, secondSalaryCriteria)
        );
        return mongoTemplate.count(query, SalaryData.class);
    }

    @Override
    public List<SalaryData> deleteByLessThanOrGreatThen(String nameField, Integer lessThen, Integer greatThen) {
        return commonRepository.deleteByLessThanOrGreatThen(nameField, lessThen, greatThen, SalaryData.class);
    }

    @Override
    public List<SalaryData> incrementByField(String name) {
        return commonRepository.incrementByField(name, SalaryData.class);
    }

}
