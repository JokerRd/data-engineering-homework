package ru.dataengineeringhomework.nosqldatabaseproject.writer;

import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import java.io.IOException;
import java.nio.file.Path;

@Component
@RequiredArgsConstructor
public class JsonFileWriter {

    private final ObjectMapper objectMapper;

    public void saveToFile(String nameFile, Object data) {
        try {
            var saveFile = Path.of(nameFile).toFile();
            var writer = objectMapper.writer(new DefaultPrettyPrinter());
            writer.writeValue(saveFile, data);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
