package inga74u.discord.kazuki.audio;

import com.sedmelluq.discord.lavaplayer.player.AudioPlayer;
import com.sedmelluq.discord.lavaplayer.player.event.AudioEventAdapter;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import com.sedmelluq.discord.lavaplayer.track.AudioTrackEndReason;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingDeque;

public class AudioListener extends AudioEventAdapter {
    private final BlockingQueue<AudioTrack> tracks = new LinkedBlockingDeque<>();
    private final MusicPlayer player;

    public AudioListener(MusicPlayer player) {
        this.player = player;
    }

    public int getQueueSize() {
        return tracks.size();
    }

    public void nextTrack() {
        if(tracks.isEmpty()) {
            player.getPlayer().stopTrack();
        }
        player.getPlayer().startTrack(tracks.poll(), false);
    }

    @Override
    public void onTrackEnd(AudioPlayer player, AudioTrack track, AudioTrackEndReason endReason) {
        if(endReason.mayStartNext) nextTrack();
    }

    public void queue(AudioTrack track) {
        if(!player.getPlayer().startTrack(track, true)) tracks.offer(track);
    }

    public void clearQueue() {
        tracks.clear();
    }

    public BlockingQueue<AudioTrack> getTracks() {
        return tracks;
    }
}
