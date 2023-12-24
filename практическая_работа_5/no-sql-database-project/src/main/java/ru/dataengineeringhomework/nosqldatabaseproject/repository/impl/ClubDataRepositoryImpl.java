package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.Club;
import ru.dataengineeringhomework.nosqldatabaseproject.model.ClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.ClubDataMongoRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.ClubRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.CommonRepository;

import java.util.List;

import static org.springframework.data.domain.PageRequest.of;

@Repository
@RequiredArgsConstructor
public class ClubDataRepositoryImpl implements ClubRepository {

    private final ClubDataMongoRepository clubDataMongoRepository;
    private final MongoTemplate mongoTemplate;
    private final CommonRepository commonRepository;

    public List<Club> getAllSortedAndLimited(int limit, Sort sort) {
        var pageRequest = of(0, limit, sort);
        return clubDataMongoRepository.findAll(pageRequest).getContent();
    }

    public List<Club> getByStadiumSeatsMoreThanFilterSortedAndLimited(int stadiumSeats, int limit, Sort sort) {
        var pageRequest = of(0, limit, sort);
        var query = Query.query(
                Criteria.where("stadium_seats").gte(stadiumSeats)
        ).with(pageRequest);
        return mongoTemplate.find(query, Club.class);
    }

    @Override
    public AggData getStatByField(String nameField) {
        return commonRepository.getStatByField(nameField, "club");
    }

    @Override
    public int getMaxValueByMinField(String maxNameField, String minNameField) {
        return commonRepository.getMaxValueByMinField(maxNameField, minNameField, "club");
    }

    @Override
    public int getMinValueByMaxField(String minNameField, String maxNameField) {
        return commonRepository.getMinValueByMaxField(minNameField, maxNameField, "club");
    }

    @Override
    public List<Club> deleteByLessThanOrGreatThen(String nameField, Integer lessThen, Integer greatThen) {
        return commonRepository.deleteByLessThanOrGreatThen(nameField, lessThen, greatThen, Club.class);
    }

    @Override
    public List<Club> incrementByField(String name) {
        return commonRepository.incrementByField(name, Club.class);
    }

    @Override
    public List<Club> multiplyFieldByInFilters(String multiplyNameField, double multiplier, InFilter inFilter) {
        return commonRepository.multiplyFieldByInFilters(multiplyNameField, multiplier, inFilter, Club.class);
    }

    @Override
    public List<Club> multiplyFieldByInFiltersAndRangeFilters(String multiplyNameField, double multiplier, List<InFilter> inFilter, List<RangeFilter> rangeFilters) {
        return commonRepository.multiplyFieldByInFiltersAndRangeFilters(multiplyNameField, multiplier, inFilter, rangeFilters, Club.class);
    }

    @Override
    public List<Club> deleteByInFiltersAndRangeFilters(List<InFilter> inFilters, List<RangeFilter> rangeFilters) {
        return commonRepository.deleteByInFiltersAndRangeFilters(inFilters, rangeFilters, Club.class);
    }
}
