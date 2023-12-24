package ru.dataengineeringhomework.nosqldatabaseproject.repository.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.ClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.DifficultFilterForClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.ClubGamesMongoRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.ClubGamesRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.CommonRepository;

import java.util.List;

import static org.springframework.data.domain.PageRequest.of;

@Repository
@RequiredArgsConstructor
public class ClubGamesRepositoryImpl implements ClubGamesRepository {

    private final ClubGamesMongoRepository clubGamesMongoRepository;
    private final MongoTemplate mongoTemplate;
    private final CommonRepository commonRepository;


    @Override
    public long countByDifficultFilter(DifficultFilterForClubGames difficultFilter) {
        var query = buildDifficultQuery(difficultFilter);
        return mongoTemplate.count(query, ClubGames.class);
    }

    @Override
    public List<ClubGames> filterByDifficultFilter(DifficultFilterForClubGames difficultFilter) {
        var query = buildDifficultQuery(difficultFilter);
        return mongoTemplate.find(query, ClubGames.class);
    }

    @Override
    public List<ClubGames> filterByDifficultFilterSortedLimited(DifficultFilterForClubGames difficultFilter,
                                                                int limit, Sort sort) {
        var query = buildDifficultQuery(difficultFilter);
        var pageRequest = of(0, limit, sort);
        return mongoTemplate.find(query.with(pageRequest), ClubGames.class);
    }

    @Override
    public List<CountByField> countByField(String nameField) {
        return commonRepository.countByField(nameField, "club_games");
    }

    @Override
    public List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup) {
        return commonRepository.getStatByFieldAndGroupByValue(nameField, nameFieldForGroup, "club_games");
    }


    private Query buildDifficultQuery(DifficultFilterForClubGames difficultFilter) {
        var firstSalaryCriteria = Criteria.where("own_goals").in(difficultFilter.ownGoals());
        var secondSalaryCriteria = Criteria.where("opponent_goals").in(difficultFilter.opponentGoals());

        return Query.query(
                Criteria.where("own_manager_name").in(difficultFilter.ownManagers())
                        .and("is_win").is(difficultFilter.isWin())
                        .orOperator(firstSalaryCriteria, secondSalaryCriteria)
        );
    }
}
