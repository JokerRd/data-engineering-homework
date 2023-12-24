package ru.dataengineeringhomework.nosqldatabaseproject.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.math.BigInteger;

@Document("salary_data")
@Getter
@Setter
@RequiredArgsConstructor
public class SalaryData {

    @Id
    @JsonIgnore
    private final BigInteger _id;

    private final Long club_id;

    private final Integer age;

    private final String city;

    private final String job;

    private final Integer salary;

    private final Integer year;

}
