package ru.dataengineeringhomework.nosqldatabaseproject.task.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;
import ru.dataengineeringhomework.nosqldatabaseproject.model.CountData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.DifficultFilterForClubGames;
import ru.dataengineeringhomework.nosqldatabaseproject.model.InFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.RangeFilter;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggData;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.AggDataByField;
import ru.dataengineeringhomework.nosqldatabaseproject.model.stat.CountByField;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.ClubGamesRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.repository.ClubRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.task.Task;
import ru.dataengineeringhomework.nosqldatabaseproject.writer.JsonFileWriter;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static org.springframework.data.domain.Sort.by;

@Component
@RequiredArgsConstructor
public class Task4 implements Task {

    private final JsonFileWriter jsonFileWriter;
    private final ClubRepository clubRepository;
    private final ClubGamesRepository clubGamesRepository;

    @Override
    public void run() {
        writeToJsonFirstTwelveClubsAndSortDescByStadiumSeats();
        writeToJsonFirstTenClubsSortedDescBySquadSizeAndFilteredByStadiumSeatsGreatEqualsThan50000();
        writeToJsonCountClubGamesByDifficultFilter();
        writeToJsonClubGamesByDifficultFilter();
        writeToJsonFirstTenClubGamesSortedByOwnGoalsFilteredByDifficultFilter();
        writeMaxMinAvgByStadiumSeats();
        writeMaxStadiumSeatsForMinSquadSize();
        writeMinSquadSizeForMaxStadiumSeats();
        writeCountByOwnManagerName();
        writeMaxMinAvgByOpponentGoalsGroupByOwnManagerName();
        deleteAndWriteClubsSquadSizeLessThen20OrGreatThen32();
        incrementForeignersNumberBy1AndWrite();
        upForeignersPercentageForDomesticCompetitionIdByTwentyPercentAndWrite();
        upStadiumSeatsByFiftyPercentWithHardFilterAndWrite();
        deleteByHardFilterAndWrite();
    }

    private void deleteByHardFilterAndWrite() {
        var deleteResult = clubRepository.deleteByInFiltersAndRangeFilters(
                List.of(
                        new InFilter("domestic_competition_id", List.of("BE1", "DK1"))
                ),
                List.of(
                        new RangeFilter("average_age", 22, 29),
                        new RangeFilter("last_season", 2015, 2023)
                ));

        var nameFile = "deleteByHardFilter.json";
        jsonFileWriter.saveToFile(nameFile, deleteResult);
    }

    private void upStadiumSeatsByFiftyPercentWithHardFilterAndWrite() {
        var updatedResult = clubRepository.multiplyFieldByInFiltersAndRangeFilters(
                "stadium_seats",
                1.5,
                List.of(
                        new InFilter("domestic_competition_id", List.of("NL1", "PO1"))
                ),
                List.of(
                        new RangeFilter("last_season", 2017, 2019),
                        new RangeFilter("squad_size", 22, 25)
                )
        );

        var nameFile = "upStadiumSeatsByFiftyPercentWithHardFilter.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void upForeignersPercentageForDomesticCompetitionIdByTwentyPercentAndWrite() {
        var updatedResult = clubRepository.multiplyFieldByInFilters(
                "foreigners_percentage",
                1.20,
                new InFilter("domestic_competition_id", List.of("ES1", "GB1"))
        );

        var nameFile = "upForeignersPercentageForDomesticCompetitionIdByTwentyPercent.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void incrementForeignersNumberBy1AndWrite() {
        var updatedResult = clubRepository.incrementByField("foreigners_number");

        var nameFile = "incrementForeignersNumberBy1.json";
        jsonFileWriter.saveToFile(nameFile, updatedResult);
    }

    private void deleteAndWriteClubsSquadSizeLessThen20OrGreatThen32() {
        var deleteResult = clubRepository.deleteByLessThanOrGreatThen("squad_size", 20, 30);

        var nameFile = "deletedClubsSquadSizeLessThen20OrGreatThen32.json";
        jsonFileWriter.saveToFile(nameFile, deleteResult);
    }

    private void writeMaxMinAvgByOpponentGoalsGroupByOwnManagerName() {
        var aggDataByField = clubGamesRepository.getStatByFieldAndGroupByValue("opponent_goals", "own_manager_name");

        var result = convertAggDataByFieldToMap(aggDataByField);

        var nameFile = "maxMinAvgByOpponentGoalsGroupByOwnManagerName.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeCountByOwnManagerName() {
        var countByFieldList = clubGamesRepository.countByField("own_manager_name");

        var countByOwnManagerName = countByFieldList.stream().collect(Collectors.toMap(
                CountByField::value,
                CountByField::count
        ));

        var nameFile = "countByOwnManagerName.json";
        jsonFileWriter.saveToFile(nameFile, countByOwnManagerName);
    }

    private void writeMinSquadSizeForMaxStadiumSeats() {
        var minSalary = clubRepository.getMinValueByMaxField("squad_size", "stadium_seats");

        var result = Map.of("minSquadSize", minSalary);

        var nameFile = "minSquadSizeForMaxStadiumSeats.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxStadiumSeatsForMinSquadSize() {
        var maxSalary = clubRepository.getMaxValueByMinField("stadium_seats", "squad_size");

        var result = Map.of("maxStadiumSeats", maxSalary);

        var nameFile = "maxStadiumSeatsForSquadSize.json";
        jsonFileWriter.saveToFile(nameFile, result);
    }

    private void writeMaxMinAvgByStadiumSeats() {
        var aggData = clubRepository.getStatByField("stadium_seats");
        var nameFile = "maxMinAvgByStadiumSeats.json";
        jsonFileWriter.saveToFile(nameFile, aggData);
    }

    private void writeToJsonFirstTwelveClubsAndSortDescByStadiumSeats() {
        var data = clubRepository.getAllSortedAndLimited(20, Sort.by(Sort.Direction.DESC, "stadium_seats"));
        var nameFile = "first20SortStadiumSeatsDesc.json";
        jsonFileWriter.saveToFile(nameFile, data);
    }

    private void writeToJsonFirstTenClubsSortedDescBySquadSizeAndFilteredByStadiumSeatsGreatEqualsThan50000() {
        var data = clubRepository.getByStadiumSeatsMoreThanFilterSortedAndLimited(50000,
                10, Sort.by(Sort.Direction.DESC, "squad_size"));
        var nameFile = "first10SortSquadSizeDescFilterStadiumSeatsGTE50000.json";
        jsonFileWriter.saveToFile(nameFile, data);
    }

    private void writeToJsonFirstTenClubGamesSortedByOwnGoalsFilteredByDifficultFilter() {
        var data = clubGamesRepository.filterByDifficultFilterSortedLimited(
                new DifficultFilterForClubGames(
                        List.of("Unai Emery", "Guus Hiddink", "Mircea Lucescu", "Rudi Garcia"),
                        List.of(0, 1),
                        List.of(3, 4),
                        true
                ), 10, Sort.by(Sort.Direction.DESC, "own_goals")
        );
        var nameFile = "first10SortOwnGoalsDescDifficultFilter.json";
        jsonFileWriter.saveToFile(nameFile, data);
    }

    private void writeToJsonClubGamesByDifficultFilter() {
        var data = clubGamesRepository.filterByDifficultFilter(
                new DifficultFilterForClubGames(
                        List.of("Unai Emery", "Guus Hiddink", "Mircea Lucescu", "Rudi Garcia"),
                        List.of(0, 1),
                        List.of(3, 4),
                        true
                )
        );
        var nameFile = "difficultFilter.json";
        jsonFileWriter.saveToFile(nameFile, data);
    }

    private void writeToJsonCountClubGamesByDifficultFilter() {
        var count = clubGamesRepository.countByDifficultFilter(
                new DifficultFilterForClubGames(
                        List.of("Unai Emery", "Guus Hiddink", "Mircea Lucescu", "Rudi Garcia"),
                        List.of(0, 1),
                        List.of(3, 4),
                        true
                )
        );
        var nameFile = "countByDifficultFilter.json";
        var countData = new CountData(count);
        jsonFileWriter.saveToFile(nameFile, countData);
    }

    private Map<String, AggData> convertAggDataByFieldToMap(List<AggDataByField> aggDataByFields) {
        return aggDataByFields.stream()
                .collect(Collectors.toMap(
                        AggDataByField::value,
                        forValue -> new AggData(forValue.max(), forValue.min(), forValue.avg()),
                        (o1, o2) -> o1,
                        LinkedHashMap::new
                ));
    }


    @Override
    public Integer getNumberTask() {
        return 4;
    }
}
