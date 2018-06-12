package inga74u.dicsord.kazuki.util;

import inga74u.dicsord.kazuki.audio.MusicCommands;
import inga74u.dicsord.kazuki.audio.MusicManager;
import inga74u.dicsord.kazuki.event.ChoiceListener;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.Message;
import java.util.ArrayList;

public class ChoiceTimer implements Runnable {
    private JDA jda;
    private ArrayList<String> ids;
    private MusicManager manager;
    private Guild guild;
    private Message msg;
    private MusicCommands musicCommands;



    public ChoiceTimer(JDA jda, ArrayList<String> ids, MusicManager manager, Guild guild, Message msg, MusicCommands musicCommands) {
        this.jda = jda;
        this.ids = ids;
        this.manager = manager;
        this.guild = guild;
        this.msg = msg;
        this.musicCommands = musicCommands;
    }

    @Override
    public void run() {
        ChoiceListener choiceListener = new ChoiceListener(ids, manager, guild, msg, jda, musicCommands);
        jda.addEventListener(choiceListener);
        try {
            Thread.sleep(10 * 1000);
        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }
        if(musicCommands.choiceTimerActive) choiceListener.terminate();
    }
}
