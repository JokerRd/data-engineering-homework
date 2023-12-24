package ru.dataengineeringhomework.nosqldatabaseproject.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import ru.dataengineeringhomework.nosqldatabaseproject.model.Club;;

public interface ClubDataMongoRepository extends MongoRepository<Club, Long> {
}
