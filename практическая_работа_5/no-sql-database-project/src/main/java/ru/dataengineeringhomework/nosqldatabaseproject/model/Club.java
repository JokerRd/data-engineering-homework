package ru.dataengineeringhomework.nosqldatabaseproject.model;


import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.math.BigInteger;

@Document("club")
@Getter
@Setter
@RequiredArgsConstructor
public class Club {

    @Id
    @JsonIgnore
    private final BigInteger _id;

    @Field(name = "club_id")
    private final Long clubId;

    @Field(name = "average_age")
    private final Double averageAge;

    @Field(name = "club_code")
    private final String clubCode;

    @Field(name = "coach_name")
    private final String coachName;

    @Field(name = "domestic_competition_id")
    private final String domesticCompetitionId;

    private final String filename;

    @Field(name = "last_season")
    private final String lastSeason;

    @Field(name = "foreigners_number")
    private final Integer foreignersNumber;

    @Field(name = "foreigners_percentage")
    private final Double foreignersPercentage;

    private final String name;

    @Field(name = "national_team_players")
    private final Integer nationalTeamPlayers;

    @Field(name = "net_transfer_record")
    private final String netTransferRecord;

    @Field(name = "squad_size")
    private final Integer squadSize;

    @Field(name = "stadium_name")
    private final String stadiumName;

    @Field(name = "total_market_value")
    private final String totalMarketValue;

    @Field(name = "stadium_seats")
    private Long stadiumSeats;

    @Field(name = "url")
    private final String url;

}
