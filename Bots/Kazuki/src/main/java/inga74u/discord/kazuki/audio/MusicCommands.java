package inga74u.discord.kazuki.audio;

import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import inga74u.discord.kazuki.core.Kazuki;
import inga74u.discord.kazuki.commands.CommandMap;
import inga74u.discord.kazuki.util.ChoiceTimer;
import inga74u.discord.kazuki.util.MathModule;
import inga74u.discord.kazuki.util.RandomReturnModule;
import inga74u.discord.kazuki.util.Secrets;
import inga74u.discord.kazuki.commands.Command.ExecutorType;
import inga74u.discord.kazuki.commands.Command;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.TextChannel;
import net.dv8tion.jda.core.entities.User;
import net.dv8tion.jda.core.entities.VoiceChannel;
import org.json.JSONObject;
import org.json.JSONTokener;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import java.io.IOException;
import java.net.URLEncoder;
import java.util.ArrayList;

public class MusicCommands {
    private final MusicManager manager;
    private final CommandMap cmdMap;
    private final EmbedBuilder eb = new EmbedBuilder();
    public boolean choiceTimerActive;

    public MusicCommands(CommandMap cmdMap) {
        this.manager = cmdMap.getManager();
        this.cmdMap = cmdMap;
    }

    @Command(name = "play", type = ExecutorType.USER, description = "Plays a song from either a link or a keyword Usage : '..play [query/link]'")
    private void play(Guild guild, User user, TextChannel tc, Kazuki kazuki, JDA jda, String context) throws IOException {
        if(guild == null) return;
        if(choiceTimerActive) return;
        if(context.equals("play") && manager.getPlayer(guild).getPlayer().isPaused()) {
            resume(guild, user, tc, kazuki, jda);
            return;
        }

        String query = context.replaceFirst("play ", "");

        if(!guild.getAudioManager().isConnected() && !guild.getAudioManager().isAttemptingToConnect()) {
            VoiceChannel voiceChannel = guild.getMember(user).getVoiceState().getChannel();
            if (voiceChannel == null) {

                eb.setAuthor(user.getName(), null, user.getAvatarUrl());
                eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
                eb.setTitle(RandomReturnModule.errorResponse());
                eb.setDescription("You must join a voice channel first...");
                eb.setFooter("kazuki.play()", null);
                eb.setColor(Secrets.EMBEDCOLOR);
                tc.sendMessage(eb.build()).queue();
                return;
            }
        }
        VoiceChannel voiceChannel = guild.getMember(user).getVoiceState().getChannel();
        // -----------------------------------------------------------------
        if(query.startsWith("http")) {
            guild.getAudioManager().openAudioConnection(voiceChannel);
            manager.loadTrack(user, tc, jda, guild, query);
            return;
        }
        // -----------------------------------------------------------------
        String keyword = URLEncoder.encode(query, "UTF-8");
        ArrayList<String> processedDurations = new ArrayList<>();

        String url_for_ids = "https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&maxResults=5&q=" + keyword + "&key=" + Secrets.YTAPIKEY;
        Document doc = Jsoup.connect(url_for_ids).timeout(10 * 1000).ignoreContentType(true).get();
        if(doc == null) System.out.println("Document is equal to NULL!");
        assert doc != null;
        String getJson = doc.text();
        JSONObject jsonObject = (JSONObject) new JSONTokener(getJson).nextValue();

        ArrayList<String> ids = new ArrayList<>();
        ArrayList<String> titles = new ArrayList<>();

        for (int i = 0; i < 5; i++) {
            ids.add(jsonObject.getJSONArray("items").getJSONObject(i).getJSONObject("id").getString("videoId"));
            titles.add(jsonObject.getJSONArray("items").getJSONObject(i).getJSONObject("snippet").getString("title"));
        }

        StringBuilder sb = new StringBuilder();
        for (String s : ids) {
            sb.append(s);
            sb.append(",");
        }
        String compactIds = sb.toString();

        String url_for_durations = "https://www.googleapis.com/youtube/v3/videos?id=" + compactIds + "&key=AIzaSyCsR0MMY396toGhc40rwx_JhLY3jRLgiiA&part=contentDetails";

        doc = Jsoup.connect(url_for_durations).timeout(10 * 1000).ignoreContentType(true).get();
        assert doc != null;
        getJson = doc.text();
        jsonObject = (JSONObject) new JSONTokener(getJson).nextValue();

        for (int i = 0; i < 5; i++) {
            processedDurations.add(MathModule.processDuration(jsonObject.getJSONArray("items").getJSONObject(i).getJSONObject("contentDetails").getString("duration")));
        }

        eb.setAuthor(user.getName(), null, user.getAvatarUrl());
        eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
        eb.setTitle("Pick a song: ");
        eb.setDescription("``1`` " + titles.get(0) + " (" + processedDurations.get(0) + ")\n");
        eb.appendDescription("``2`` " + titles.get(1) + " (" + processedDurations.get(1) + ")\n");
        eb.appendDescription("``3`` " + titles.get(2) + " (" + processedDurations.get(2) + ")\n");
        eb.appendDescription("``4`` " + titles.get(3) + " (" + processedDurations.get(3) + ")\n");
        eb.appendDescription("``5`` " + titles.get(4) + " (" + processedDurations.get(4) + ")\n");
        eb.addField("Side-note:", "This message will self destruct in 10 seconds!\n ", false);

        eb.setFooter("kazuki.giveChoice()", null);
        eb.setColor(Secrets.EMBEDCOLOR);
        tc.sendMessage(eb.build()).queue(message -> {
            new Thread(new ChoiceTimer(jda, ids, manager, guild, message, this), "giveChoice").start();
            this.choiceTimerActive = true;
        });
        eb.clearFields();
    }

    @Command(name = "skip", type = ExecutorType.USER, description = "Skips the song currently playing.")
    private void skip(Guild guild, User user, TextChannel textChannel, JDA jda) {
        if(guild == null) return;
        if(!guild.getAudioManager().isConnected() && !guild.getAudioManager().isAttemptingToConnect()) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I'm not even in a voice channel...");
            eb.setFooter("kazuki.skip()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else if(manager.getPlayer(guild).getListener().getTracks().isEmpty() && manager.getPlayer(guild).getPlayer().getPlayingTrack() == null) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I can't skip nothing...");
            eb.setFooter("kazuki.skip()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle("Track Skipped:");
            eb.setDescription("'" + manager.getPlayer(guild).getPlayer().getPlayingTrack().getInfo().title + "'");
            eb.setFooter("kazuki.skip()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            manager.getPlayer(guild).skipTrack();
            textChannel.sendMessage(eb.build()).queue();
        }
    }

    @Command(name = "pause", type = ExecutorType.USER, description = "Pauses the song currently playing.")
    private void pause(Guild guild, User user, TextChannel textChannel, JDA jda) {
        if(guild == null) return;
        if(!guild.getAudioManager().isConnected() && !guild.getAudioManager().isAttemptingToConnect()) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I'm not even in a voice channel...");
            eb.setFooter("kazuki.pause()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else if(manager.getPlayer(guild).getListener().getTracks().isEmpty() && manager.getPlayer(guild).getPlayer().getPlayingTrack() == null) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I don't even have anything queued...");
            eb.setFooter("kazuki.pause()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else if(manager.getPlayer(guild).getPlayer().isPaused()) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I'm already paused...");
            eb.setFooter("kazuki.pause()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle("Paused Track:");
            eb.setDescription("'" + manager.getPlayer(guild).getPlayer().getPlayingTrack().getInfo().title + "'");
            eb.setFooter("kazuki.pause()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
            manager.getPlayer(guild).getPlayer().setPaused(true);
        }
    }

    @Command(name = "resume", type = ExecutorType.USER, description = "Resumes the song currently paused.")
    private void resume(Guild guild, User user, TextChannel textChannel, Kazuki kazuki, JDA jda) {
        if(guild == null) return;
        if(!manager.getPlayer(guild).getPlayer().isPaused()) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I'm not paused!");
            eb.setFooter("kazuki.resume()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else if(manager.getPlayer(guild).getListener().getTracks().isEmpty() && manager.getPlayer(guild).getPlayer().getPlayingTrack() == null) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("I can't resume nothing...");
            eb.setFooter("kazuki.resume()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle("Resumed Track:");
            eb.setDescription("'" + manager.getPlayer(guild).getPlayer().getPlayingTrack().getInfo().title + "'");
            eb.setFooter("kazuki.resume()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
            manager.getPlayer(guild).getPlayer().setPaused(false);
        }
    }

    @Command(name = "summon", type = ExecutorType.USER, description = "Summons me to join the voice channel you're in.")
    private void summon(Guild guild, TextChannel textChannel, User user) {
        if(guild == null) return;
        VoiceChannel voiceChannel = guild.getMember(user).getVoiceState().getChannel();
        guild.getAudioManager().openAudioConnection(voiceChannel);
    }

    @Command(name = "leave", type = ExecutorType.USER, description = "Tells me to leave any voice channel I'm in.")
    private void leave(Guild guild, TextChannel textChannel) {
        if(guild == null) return;
        AudioListener listener = new AudioListener(manager.getPlayer(guild));
        listener.getTracks().clear();
        manager.getPlayer(guild).getPlayer().stopTrack();
        guild.getAudioManager().closeAudioConnection();
    }

    @Command(name = "stop", type = ExecutorType.USER, description = "Stops the current song completely and clears the queue.")
    private void stop(Guild guild, User user, TextChannel textChannel, JDA jda) {
        if(guild == null) return;
        eb.setAuthor(user.getName(), null, user.getAvatarUrl());
        eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
        eb.setTitle("Stopped Current Track.");
        eb.setDescription("The queue has also been cleared.");
        eb.setFooter("kazuki.stop()", null);
        eb.setColor(Secrets.EMBEDCOLOR);
        textChannel.sendMessage(eb.build()).queue();

        AudioListener listener = new AudioListener(manager.getPlayer(guild));
        listener.clearQueue();
        manager.getPlayer(guild).getPlayer().stopTrack();
    }

    @Command(name = "queue", type = ExecutorType.USER, description = "Displays what songs are in the queue.")
    private void queue(Guild guild, TextChannel textChannel, User user, JDA jda) {
        if(guild == null) return;
        if(manager.getPlayer(guild).getPlayer().getPlayingTrack() == null){
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle(RandomReturnModule.errorResponse());
            eb.setDescription("There are no songs in the queue.");
            eb.setFooter("kazuki.queue()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
        } else {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle("Currently Playing Track:");
            eb.setDescription(manager.getPlayer(guild).getPlayer().getPlayingTrack().getInfo().title);

            if(!manager.getPlayer(guild).getListener().getTracks().isEmpty()) {
                StringBuilder sb = new StringBuilder();
                int i = 0;
                for(AudioTrack song : manager.getPlayer(guild).getListener().getTracks()) {
                    i = i + 1;
                    sb.append("\n``").append(i).append("`` ").append(song.getInfo().title);
                }
                eb.addField("Queued Tracks:", sb.toString(), false);
            } else {
                eb.addField("Queued Tracks:", "There are no queued tracks. Use " + cmdMap.getPrefix() + "play to add more!", false);
            }
            eb.setFooter("kazuki.queue()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            textChannel.sendMessage(eb.build()).queue();
            eb.clearFields();
        }
    }
}
