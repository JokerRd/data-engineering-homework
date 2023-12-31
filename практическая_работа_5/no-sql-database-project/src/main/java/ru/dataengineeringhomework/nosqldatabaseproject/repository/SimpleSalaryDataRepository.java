package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import org.springframework.data.domain.Sort;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.SalaryData;

import java.util.List;

public interface SimpleSalaryDataRepository {

    List<SalaryData> getAllSortedAndLimited(int limit, Sort sort);

    List<SalaryData> getByLessAge(int age, int limit, Sort sort);

    List<SalaryData> getByEqualsCityAndInJobsCollections(String city, List<String> jobs, int limit, Sort sort);

    long countByDifficultFilter();

    List<SalaryData> deleteByLessThanOrGreatThen(String nameField, Integer lessThen, Integer greatThen);

    List<SalaryData> incrementByField(String name);
}
