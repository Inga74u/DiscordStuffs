package inga74u.discord.kazuki.audio;

import com.sedmelluq.discord.lavaplayer.player.AudioLoadResultHandler;
import com.sedmelluq.discord.lavaplayer.player.AudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.player.DefaultAudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.source.AudioSourceManagers;
import com.sedmelluq.discord.lavaplayer.tools.FriendlyException;
import com.sedmelluq.discord.lavaplayer.track.AudioPlaylist;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import inga74u.discord.kazuki.util.*;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.TextChannel;
import net.dv8tion.jda.core.entities.User;
import java.util.HashMap;
import java.util.Map;

public class MusicManager {
    private final AudioPlayerManager manager = new DefaultAudioPlayerManager();
    private final Map<String, MusicPlayer> players = new HashMap<>();
    private final EmbedBuilder eb = new EmbedBuilder();

    public MusicManager() {
        AudioSourceManagers.registerRemoteSources(manager);
        AudioSourceManagers.registerLocalSource(manager);
    }

    public synchronized MusicPlayer getPlayer(Guild guild) {
        if(!players.containsKey(guild.getId())) players.put(guild.getId(), new MusicPlayer(manager.createPlayer(), guild));
        return players.get(guild.getId());
    }

    public void loadTrack(User user, TextChannel tc, JDA jda, Guild guild, String source) {
        MusicPlayer player = getPlayer(tc.getGuild());
        guild.getAudioManager().setSendingHandler(player.getAudioHandler());

        manager.loadItemOrdered(player, source, new AudioLoadResultHandler() {

            @Override
            public void trackLoaded(AudioTrack track) {
                eb.setTitle("Track added to queue:").setDescription("'" + track.getInfo().title + "'\n");
                eb.addField("Length:", MathModule.convertTime(track.getInfo().length), false);
                eb.addField("Side-note:", "The song may not start right away as it has to be downloaded first.\n", false);
                player.playTrack(track);
                output();
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {
                eb.setTitle("Songs from playlist added to queue: ");
                int total = 0;
                for (int i = 0; i < playlist.getTracks().size() && i < Secrets.MAXSONGS; i++) {
                    AudioTrack track = playlist.getTracks().get(i);
                    int songCount = i + 1;
                    eb.appendDescription("\n ``" + songCount + "`` " + track.getInfo().title + MathModule.convertTime_Short(track.getInfo().length));
                    player.playTrack(track);
                    total++;
                }
                eb.addField("Total songs added: ", total + " (Maximum: " + Secrets.MAXSONGS + ")", false);
                output();
            }

            @Override
            public void noMatches() {
                eb.setTitle(RandomReturnModule.errorResponse());
                eb.setDescription("I couldn't find anything by: " + source);
                output();
            }

            @Override
            public void loadFailed(FriendlyException fe) {
                eb.setTitle(RandomReturnModule.errorResponse());
                eb.setDescription("``That request failed:`` " + fe.getMessage());
                output();
            }

            public void output() {
                eb.setAuthor(user.getName(), null, user.getAvatarUrl());
                eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
                eb.setFooter("kazuki.play()", null);
                eb.setColor(Secrets.EMBEDCOLOR);
                tc.sendMessage(eb.build()).queue();
                eb.clearFields();
            }
        });
    }

    public void loadTrack(MusicPlayer player, final String source) {

        player.getGuild().getAudioManager().setSendingHandler(player.getAudioHandler());

        manager.loadItemOrdered(player, source, new AudioLoadResultHandler() {

            @Override
            public void trackLoaded(AudioTrack track) {
                player.playTrack(track);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {

            }

            @Override
            public void noMatches() {

            }

            @Override
            public void loadFailed(FriendlyException e) {

            }
        });
    }

    public Map<String, MusicPlayer> getPlayers() {
        return players;
    }
}
