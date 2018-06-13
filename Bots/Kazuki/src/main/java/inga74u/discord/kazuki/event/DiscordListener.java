package inga74u.discord.kazuki.event;

import inga74u.discord.kazuki.commands.CommandMap;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.events.Event;
import net.dv8tion.jda.core.events.ReadyEvent;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.hooks.EventListener;
import javax.swing.*;


public class DiscordListener implements EventListener {
    private final CommandMap cmdMap;
    public DiscordListener(CommandMap cmdMap) {
        this.cmdMap = cmdMap;
        this.terminateBTN = terminateBTN;
    }

    @Override
    public void onEvent(Event e) {
        if(e instanceof ReadyEvent) onReady ((ReadyEvent) e);
        if(e instanceof MessageReceivedEvent) onMessage ((MessageReceivedEvent) e);
    }

    private void onReady(ReadyEvent re) {
        System.out.println("[JDA Kazuki-MainClass] INFO inga74u.discord.kazuki.event.DiscordListener -  Bot has completed startup and is ready for use!"); // This is pretty much obsolete because in the compiled version there is no visible console
        cmdMap.idle(true); // State of idle by default, note that idle sounds will not play until something else has been played (by that guilds player) before
    }

    private void onMessage(MessageReceivedEvent mre) {
        if(mre.getAuthor().equals(mre.getJDA().getSelfUser())) return;

        String msg = mre.getMessage().getContentRaw();
        if(msg.startsWith(cmdMap.getPrefix())) {
            msg = msg.replaceFirst(cmdMap.getPrefix(), "");
            if(cmdMap.commandFromUser(mre.getAuthor(), msg, mre.getMessage())) {
                if(mre.getTextChannel() != null && mre.getGuild().getSelfMember().hasPermission(Permission.MESSAGE_MANAGE)) {
                    if(mre.getMessage() != null) mre.getMessage().delete().queue();
                }
            }
        }
    }
}
