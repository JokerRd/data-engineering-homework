package ru.dataengineeringhomework.nosqldatabaseproject.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.math.BigInteger;

@Document("club_games")
@Getter
@Setter
@RequiredArgsConstructor
public class ClubGames {

    @Id
    @JsonIgnore
    private final BigInteger _id;

    @Field(name = "club_id")
    private final Long clubId;

    @Field(name = "game_id")
    private final Long gameId;

    private final String hosting;

    @Field(name = "is_win")
    private final Boolean isWin;

    @Field(name = "opponent_goals")
    private final Integer opponentGoals;

    @Field(name = "opponent_id")
    private final Long opponentId;

    @Field(name = "opponent_manager_name")
    private final String opponentManagerName;

    @Field(name = "opponentPosition")
    private final Integer opponentPosition;

    @Field(name = "own_goals")
    private final Integer ownGoals;

    @Field(name = "own_manager_name")
    private final String ownManagerName;

    @Field(name = "own_position")
    private final Integer ownPosition;

}
