package ru.dataengineeringhomework.exercisetwo;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Parser {

    public static void main(String[] args) {
        var pathToSave = definePathToSaveFileFromArgsOrDefault(args);

        var averageList = readFileAndHandleData();

        saveResult(pathToSave, averageList);
    }

    private static String definePathToSaveFileFromArgsOrDefault(String[] args) {
        var pathToSave = "result.txt";
        if (args.length == 1) {
            pathToSave = args[0];
        }
        return pathToSave;
    }

    private static List<String> readFileAndHandleData() {
        var is = Parser.class.getClassLoader().getResourceAsStream("text_2_var_51");
        try (var reader = new BufferedReader(new InputStreamReader(is))) {
            return reader.lines()
                    .map(Parser::calculateAverageForString)
                    .toList();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static String calculateAverageForString(String dataAsStr) {
        var dataList = parseStringData(dataAsStr);
        var numbers = dataList.stream().map(Long::parseLong).toList();
        var average = calculateAverage(numbers);
        return String.valueOf(average);
    }

    private static List<String> parseStringData(String dataAsStr) {
        var data = dataAsStr.split("\\|");
        return Arrays.asList(data);
    }

    private static long calculateAverage(List<Long> numbers) {
        var sumNumbers = numbers.stream()
                .mapToLong(number -> number)
                .sum();
        return sumNumbers / numbers.size();
    }

    private static void saveResult(String pathToSave, List<String> result) {
        var outputPath = Paths.get(pathToSave);
        try {
            Files.write(outputPath, result);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
