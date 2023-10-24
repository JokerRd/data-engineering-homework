package ru.dataengineeringhomework.exercisesix;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.hc.client5.http.fluent.Request;

public class JsonParser {

    public static void main(String[] args) {
        var pathToSave = definePathToSaveFileFromArgsOrDefault(args);

        var data = requestForData();
        var catResponse = convertBytesToCatResponse(data);
        var html = convertCatResponseToHtml(catResponse);
        saveResult(pathToSave, html);
    }

    private static String definePathToSaveFileFromArgsOrDefault(String[] args) {
        var pathToSave = "result.html";
        if (args.length == 1) {
            pathToSave = args[0];
        }
        return pathToSave;
    }

    private static byte[] requestForData() {
        try {
            return Request.get("https://catfact.ninja/facts?max_length=100&limit=10")
                    .execute()
                    .returnContent()
                    .asBytes();
        } catch (IOException exception) {
            throw new RuntimeException(exception);
        }
    }

    private static CatResponse convertBytesToCatResponse(byte[] data) {
        var objectMapper = new ObjectMapper()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        try {
            return objectMapper.readValue(data, CatResponse.class);
        } catch (IOException exception) {
            throw new RuntimeException(exception);
        }
    }


    private static String convertCatResponseToHtml(CatResponse response) {
        var headerTemplate = "<tr><th>Order number</th><th>Fact about cat</th><th>Length fact</th><th>Fact link</th><th>Is link active?</th></tr>";
        var dateTrTemplate = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>";
        var tableTemplate = "<table>%s</table>";
        List<String> trList = new ArrayList<>();
        trList.add(headerTemplate);
        for (var i = 0; i < response.getData().size(); i++) {
            var fact = response.getData().get(i);
            var link = response.getLinks().get(i + 1);
            var tr = dateTrTemplate.formatted(i, fact.getFact(), fact.getLength(), link.getUrl(), formatActive(link.getActive()));
            trList.add(tr);
        }
        return tableTemplate.formatted(String.join("\n", trList));
    }

    private static String formatActive(boolean isActive) {
        return isActive ? "Yes" : "No";
    }

    private static void saveResult(String pathToSave, String result) {
        var outputPath = Paths.get(pathToSave);
        try {
            Files.writeString(outputPath, result);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
