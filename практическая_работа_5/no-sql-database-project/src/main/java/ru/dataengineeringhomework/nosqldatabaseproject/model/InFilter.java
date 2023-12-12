package ru.dataengineeringhomework.nosqldatabaseproject.model;

import java.util.List;

public record InFilter(String nameField, List<String> values) {
}
