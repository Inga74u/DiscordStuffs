package inga74u.discord.kazuki.event;

import inga74u.discord.kazuki.audio.MusicCommands;
import inga74u.discord.kazuki.audio.MusicManager;
import inga74u.discord.kazuki.util.RandomReturnModule;
import inga74u.discord.kazuki.util.Secrets;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.entities.*;
import net.dv8tion.jda.core.events.Event;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.hooks.EventListener;
import java.util.ArrayList;

public class ChoiceListener implements EventListener {
    private EmbedBuilder eb = new EmbedBuilder();
    private MusicManager manager;
    private ArrayList<String> ids;
    private Guild guild;
    private Message msg;
    private JDA jda;
    private MusicCommands musicCommands;

    public ChoiceListener(ArrayList<String> ids, MusicManager manager, Guild guild, Message msg, JDA jda, MusicCommands musicCommands) {
        this.ids = ids;
        this.manager = manager;
        this.guild = guild;
        this.msg = msg;
        this.jda = jda;
        this.musicCommands = musicCommands;
    }

    @Override
    public void onEvent(Event e) {
        if(e instanceof MessageReceivedEvent) onMessage((MessageReceivedEvent) e);
    }

    private void onMessage(MessageReceivedEvent e) {
        if(e.getAuthor().equals(e.getJDA().getSelfUser())) return;
        if(e.getTextChannel() != msg.getTextChannel()) return;

        User user = e.getAuthor();
        TextChannel tc = e.getTextChannel();
        String cmd = e.getMessage().getContentRaw();

        switch (cmd) {
            case "1":
            case Secrets.PREFIX + "play 1":
                play(guild, ids.get(0), user, tc, jda);
                break;

            case "2":
            case Secrets.PREFIX + "play 2":
                play(guild, ids.get(1), user, tc, jda);
                break;

            case "3":
            case Secrets.PREFIX + "play 3":
                play(guild, ids.get(2), user, tc, jda);
                break;

            case "4":
            case Secrets.PREFIX + "play 4":
                play(guild, ids.get(3), user, tc, jda);
                break;

            case "5":
            case Secrets.PREFIX + "play 5":
                play(guild, ids.get(4), user, tc, jda);
                break;

            default:
                eb.setAuthor(user.getName(), null, user.getAvatarUrl());
                eb.setThumbnail(e.getJDA().getSelfUser().getAvatarUrl());
                eb.setTitle(RandomReturnModule.errorResponse());
                eb.setDescription("That wasn't even an option...");
                if(manager.getPlayer(guild).getListener().getQueueSize() > 1) eb.setFooter("kazuki.queue()", null);
                if(manager.getPlayer(guild).getListener().getQueueSize() < 1) eb.setFooter("kazuki.play()", null);
                eb.setColor(Secrets.EMBEDCOLOR);
                tc.sendMessage(eb.build()).queue();
                eb.clearFields();
                break;
        }
        e.getMessage().delete().queue();
        terminate();
    }

    private void play(Guild guild, String song, User user, TextChannel tc, JDA jda) {
        if(guild == null) return;

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
                eb.clearFields();
            }
        }
        VoiceChannel voiceChannel = guild.getMember(user).getVoiceState().getChannel();
        guild.getAudioManager().openAudioConnection(voiceChannel);
        manager.loadTrack(user, tc, jda, guild, song);
    }

    public void terminate() {
        msg.delete().queue();
        musicCommands.choiceTimerActive = false;
        jda.removeEventListener(this);
    }
}
