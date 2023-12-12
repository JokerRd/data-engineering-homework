package ru.dataengineeringhomework.nosqldatabaseproject.model;

import org.springframework.data.domain.Sort;

public record AggWithSortRequest(String aggNameField,
                                 String groupNameField,
                                 String sortNameField,
                                 Sort.Direction direction) {
}
