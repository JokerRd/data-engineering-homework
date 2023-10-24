package ru.dataengineeringhomework.exercisefour;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.apache.commons.csv.CSVRecord;
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

public class CsvParser {

    private final static String[] HEADERS_CSV = {"id", "name", "surname", "age", "income", "phone"};


    public static void main(String[] args) {
        var pathToSave = definePathToSaveFileFromArgsOrDefault(args);

        var resultHandle = readAndHandleFile();

        var resultAsArrays = resultHandle.stream()
                .map(record -> record.values().toArray(String[]::new))
                .toList();

        saveResult(pathToSave, resultAsArrays);
    }

    private static List<Map<String, String>> readAndHandleFile() {
        var is = CsvParser.class.getClassLoader().getResourceAsStream("text_4_var_51");
        try (var reader = new BufferedReader(new InputStreamReader(is))) {
            var csvFormat = CSVFormat.DEFAULT.builder()
                    .setHeader(HEADERS_CSV)
                    .setSkipHeaderRecord(true)
                    .build();

            try (var csvReader = csvFormat.parse(reader)) {
                var transformedCsvData = csvReader.stream()
                        .map(CSVRecord::toMap)
                        .map(CsvParser::deleteColumnPhone)
                        .toList();

                var averageIncome = transformedCsvData.stream()
                        .map(record -> record.get("income"))
                        .map(CsvParser::trimNotDigitSymbol)
                        .mapToInt(Integer::parseInt)
                        .average()
                        .getAsDouble();

                return transformedCsvData
                        .stream()
                        .filter(record -> isIncomeMoreOrEqualsThenAverageIncome(record.get("income"), averageIncome))
                        .filter(CsvParser::isAgeMoreThenTwentyFivePlusModNumberVariant)
                        .sorted(Comparator.comparing(record -> Integer.valueOf(record.get("id"))))
                        .toList();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static Map<String, String> deleteColumnPhone(Map<String, String> record) {
        record.remove("phone");
        return record;
    }

    private static String trimNotDigitSymbol(String income) {
        return income.replaceAll("\\D", "");
    }

    private static boolean isIncomeMoreOrEqualsThenAverageIncome(String incomeAsStrWithRubleSymbol, double averageIncome) {
        var incomeAsStr = trimNotDigitSymbol(incomeAsStrWithRubleSymbol);
        var income = Integer.parseInt(incomeAsStr);
        return income >= averageIncome;
    }


    private static boolean isAgeMoreThenTwentyFivePlusModNumberVariant(Map<String, String> record) {
        var numberVariant = 51;
        var mod = numberVariant % 10;
        var ageAsStr = record.get("age");
        var age = Integer.parseInt(ageAsStr);
        return age > 25 + mod;
    }

    private static String definePathToSaveFileFromArgsOrDefault(String[] args) {
        var pathToSave = "result.csv";
        if (args.length == 1) {
            pathToSave = args[0];
        }
        return pathToSave;
    }

    private static void saveResult(String pathToSave, List<String[]> result) {
        try (CSVPrinter printer = new CSVPrinter(new FileWriter(pathToSave), CSVFormat.DEFAULT)) {
            printer.printRecords(result);
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}
