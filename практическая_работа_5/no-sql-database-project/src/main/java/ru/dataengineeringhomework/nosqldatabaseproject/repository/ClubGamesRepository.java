package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import org.springframework.data.domain.Sort;
import ru.dataengineeringhomework.nosqldatabaseproject.model.ClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.DifficultFilterForClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;

import java.util.List;

public interface ClubGamesRepository {

    long countByDifficultFilter(DifficultFilterForClubGames difficultFilter);

    List<ClubGames> filterByDifficultFilter(DifficultFilterForClubGames difficultFilter);

    List<ClubGames> filterByDifficultFilterSortedLimited(DifficultFilterForClubGames difficultFilter, int limit, Sort sort);

    List<CountByField> countByField(String nameField);

    List<AggDataByField> getStatByFieldAndGroupByValue(String nameField, String nameFieldForGroup);
}
