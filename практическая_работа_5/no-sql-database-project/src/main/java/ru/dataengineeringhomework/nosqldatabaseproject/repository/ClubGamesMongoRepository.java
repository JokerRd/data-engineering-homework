package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.ClubGames;

public interface ClubGamesMongoRepository extends MongoRepository<ClubGames, Long> {
}
