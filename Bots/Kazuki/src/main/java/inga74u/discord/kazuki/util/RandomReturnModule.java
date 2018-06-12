package inga74u.discord.kazuki.util;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class RandomReturnModule {
    public static String errorResponse() {
        List<String> error = new ArrayList<>();
        error.add("Uhm:");
        error.add("C'mon:");
        error.add("Dude, Seriously:");
        error.add("Sorry:");
        
        return error.get(new Random().nextInt(error.size()));
    }

    public static String idleVoice() {
        List<String> idlePath = new ArrayList<>();
        idlePath.add("src/main/resources/audio/idleLines/idle1.mp3");
        idlePath.add("src/main/resources/audio/idleLines/idle2.mp3");
        idlePath.add("src/main/resources/audio/idleLines/idle3.mp3");
        idlePath.add("src/main/resources/audio/idleLines/idle4.mp3");

        return idlePath.get(new Random().nextInt(idlePath.size()));
    }
}
