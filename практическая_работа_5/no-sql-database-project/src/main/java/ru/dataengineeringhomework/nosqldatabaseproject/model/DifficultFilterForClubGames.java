package ru.dataengineeringhomework.nosqldatabaseproject.model;

import java.util.List;

public record DifficultFilterForClubGames(List<String> ownManagers, List<Integer> ownGoals,
                                          List<Integer> opponentGoals, boolean isWin) {
}
