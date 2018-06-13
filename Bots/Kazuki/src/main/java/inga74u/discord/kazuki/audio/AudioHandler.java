package inga74u.discord.kazuki.audio;

import com.sedmelluq.discord.lavaplayer.player.AudioPlayer;
import com.sedmelluq.discord.lavaplayer.track.playback.AudioFrame;
import net.dv8tion.jda.core.audio.AudioSendHandler;

public class AudioHandler implements AudioSendHandler {
    private final AudioPlayer player;
    private AudioFrame lastFrame;

    public AudioHandler(AudioPlayer player) {
        this.player = player;
    }

    @Override
    public boolean canProvide() {
        if(lastFrame == null) lastFrame = player.provide();
        return lastFrame != null;
    }

    @Override
    public byte[] provide20MsAudio() {
        byte[] data = canProvide() ? lastFrame.getData() : null;
        lastFrame = null;
        return data;
    }

    @Override
    public boolean isOpus() {
        return true;
    }
}
