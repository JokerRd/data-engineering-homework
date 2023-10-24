package ru.dataengineeringhomework.exerciseone;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Parser {

    public static void main(String[] args) {
        var pathToSave = definePathToSaveFileFromArgsOrDefault(args);

        var frequencyMap = readFileAndHandleData();

        var sortedResultList = getSortedListByFrequencyDescFromMap(frequencyMap);

        saveResult(pathToSave, sortedResultList);
    }

    private static String definePathToSaveFileFromArgsOrDefault(String[] args) {
        var pathToSave = "result.txt";
        if (args.length == 1) {
            pathToSave = args[0];
        }
        return pathToSave;
    }

    private static Map<String, Integer> readFileAndHandleData() {
        Map<String, Integer> frequencyMap = new HashMap<>();
        var is = Parser.class.getClassLoader().getResourceAsStream("text_1_var_51");
        try (var reader = new BufferedReader(new InputStreamReader(is))) {
            reader.lines().forEach(line -> handleData(line, frequencyMap));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return frequencyMap;
    }

    private static void handleData(String line, Map<String, Integer> frequencyMap) {
        var dataList = parseStringData(line);

        for (var word : dataList) {
            if (frequencyMap.containsKey(word)) {
                var currentFrequency = frequencyMap.get(word);
                var newFrequency = currentFrequency + 1;
                frequencyMap.put(word, newFrequency);
            } else {
                frequencyMap.put(word, 1);
            }
        }
    }

    private static List<String> parseStringData(String dataAsStr) {
        var data = dataAsStr.split("[\\s\\p{Punct}]");
        return Arrays.asList(data);
    }

    private static List<String> getSortedListByFrequencyDescFromMap(Map<String, Integer> frequencyMap) {
        return frequencyMap.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .map(entry -> concatWordAndFrequency(entry.getKey(), entry.getValue()))
                .toList();
    }


    private static String concatWordAndFrequency(String word, Integer frequency) {
        return String.join(":", word, frequency.toString());
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
