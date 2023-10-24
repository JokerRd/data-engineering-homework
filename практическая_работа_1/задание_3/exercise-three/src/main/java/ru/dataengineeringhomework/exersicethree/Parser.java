package ru.dataengineeringhomework.exersicethree;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Parser {
    public static void main(String[] args) {
        var pathToSave = definePathToSaveFileFromArgsOrDefault(args);

        var resultList = readFileAndHandleData();

        saveResult(pathToSave, resultList);
    }

    private static String definePathToSaveFileFromArgsOrDefault(String[] args) {
        var pathToSave = "result.txt";
        if (args.length == 1) {
            pathToSave = args[0];
        }
        return pathToSave;
    }

    private static List<String> readFileAndHandleData() {
        var is = Parser.class.getClassLoader().getResourceAsStream("text_3_var_51");

        try (var reader = new BufferedReader(new InputStreamReader(is))) {
            return reader.lines().map(Parser::filterData).toList();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    private static String filterData(String dataAsStr) {
        var dataList = parseStringData(dataAsStr);
        List<String> resultList = new ArrayList<>();

        for (var i = 0; i < dataList.size(); i++) {
            var number = dataList.get(i);
            if (number.equals("NA")) {
                number = calculateAverageBetweenPrevAndNextValue(dataList.get(i - 1), dataList.get(i + 1));
            }
            if (isSquareRootNumberMoreOrEqualsThenFiftyPlusNumberVariant(number)) {
                resultList.add(number);
            }
        }

        return String.join(",", resultList);
    }

    private static List<String> parseStringData(String dataAsStr) {
        var data = dataAsStr.split(",");
        return Arrays.asList(data);
    }


    private static String calculateAverageBetweenPrevAndNextValue(String prevValueAsStr, String nextValueAsStr) {
        var prevValue = Integer.valueOf(prevValueAsStr);
        var nextValue = Integer.valueOf(nextValueAsStr);
        var currentValue = (prevValue + nextValue) / 2;
        return String.valueOf(currentValue);
    }

    private static boolean isSquareRootNumberMoreOrEqualsThenFiftyPlusNumberVariant(String numberAsStr) {
        var numberVariant = 51;
        var number = Integer.parseInt(numberAsStr);
        var squareRootNumber = Math.sqrt(number);
        return squareRootNumber >= numberVariant + 50;
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
