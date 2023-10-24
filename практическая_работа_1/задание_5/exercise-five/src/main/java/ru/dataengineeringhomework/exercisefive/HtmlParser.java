package ru.dataengineeringhomework.exercisefive;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class HtmlParser {
    public static void main(String[] args) {
        var pathToSave = definePathToSaveFileFromArgsOrDefault(args);

        var resultList = readFileAndHandleData();

        saveResult(pathToSave, resultList);
    }

    private static String definePathToSaveFileFromArgsOrDefault(String[] args) {
        var pathToSave = "result.csv";
        if (args.length == 1) {
            pathToSave = args[0];
        }
        return pathToSave;
    }

    private static List<String[]> readFileAndHandleData() {
        try(var is = HtmlParser.class.getClassLoader().getResourceAsStream("text_5_var_51")) {
            var document = Jsoup.parse(is, "UTF-8", "http://example.com/");
            var trElements = document.getElementsByTag("tr");
            return trElements.stream()
                    .map(HtmlParser::convertTrToCsvLines)
                    .toList();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static String[] convertTrToCsvLines(Element trElement) {
        var index = trElement.elementSiblingIndex();
        var searchTag = "td";
        if (index == 0) {
            searchTag = "th";
        }
        return trElement.getElementsByTag(searchTag).stream()
                .map(Element::text)
                .toArray(String[]::new);
    }

    private static void saveResult(String pathToSave, List<String[]> result) {
        try (CSVPrinter printer = new CSVPrinter(new FileWriter(pathToSave), CSVFormat.DEFAULT)) {
            printer.printRecords(result);
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}
