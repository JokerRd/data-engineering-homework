package ru.dataengineeringhomework.exercisesix;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class CatResponse {

    private List<CatLink> links;
    private List<CatFact> data;
}
