package inga74u.discord.kazuki.idle;

import inga74u.discord.kazuki.audio.MusicManager;
import inga74u.discord.kazuki.audio.MusicPlayer;
import inga74u.discord.kazuki.util.RandomReturnModule;
import java.util.ArrayList;
import java.util.List;

public class Idle implements Runnable {
    private List<MusicPlayer> players = new ArrayList<>();
    private MusicManager manager;

    private boolean running;

    public Idle(MusicManager manager) {
        this.manager = manager;
    }

    @Override
    public void run() {
        running = true;
        while(running) { // If the boolean is running, loop this.
            try {
                players.clear();
                players.addAll(manager.getPlayers().values());
                for(MusicPlayer player : players) {
                    if (player.getGuild().getAudioManager().isConnected() && player.idle) {
                        if (player.getListener().getTracks().isEmpty() && player.getPlayer().getPlayingTrack() == null) {
                            manager.loadStealth(player, RandomReturnModule.idleVoice()); // Tell the music manager to load a track without a message.
                        }
                    }
                }
                Thread.sleep(30 * 1000);
            } catch(InterruptedException ie) {
                ie.printStackTrace();
            }
        }
    }

    public void terminate() { // A simple function to terminate this thread
        this.running = false; // Sets the boolean 'running' to false.
    }
}
