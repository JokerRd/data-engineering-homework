package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import org.springframework.data.domain.Sort;
import ru.dataengineeringhomework.nosqldatabaseproject.model.Club;
import ru.dataengineeringhomework.nosqldatabaseproject.model.ClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;

import java.util.List;

public interface ClubRepository {

    List<Club> getAllSortedAndLimited(int limit, Sort sort);

    List<Club> getByStadiumSeatsMoreThanFilterSortedAndLimited(int stadiumSeats,int limit, Sort sort);

    AggData getStatByField(String nameField);

    int getMaxValueByMinField(String maxNameField, String minNameField);

    int getMinValueByMaxField(String minNameField, String maxNameField);

    List<Club> deleteByLessThanOrGreatThen(String nameField, Integer lessThen, Integer greatThen);

    List<Club> incrementByField(String name);

    List<Club>  multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter);

    List<Club> multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier,
                                                            List<InFilter> inFilter, List<RangeFilter> rangeFilters);

    List<Club>  deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters);

}
