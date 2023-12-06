package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.SalaryData;

public interface SalarySpringDataRepository extends MongoRepository<SalaryData, Long> {


}
