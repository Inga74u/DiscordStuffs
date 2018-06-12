package inga74u.discord.kazuki.commands;

import inga74u.discord.kazuki.util.Secrets;
import inga74u.discord.kazuki.commands.Command.ExecutorType;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.entities.*;
import net.dv8tion.jda.core.entities.impl.UserImpl;
import java.util.List;

public class StandardCommands {
    private final CommandMap cmdMap;
    private final EmbedBuilder eb;
    
    public StandardCommands(CommandMap cmdMap) {
        this.cmdMap = cmdMap;
        eb = new EmbedBuilder();
    }
    
    @Command(name = "help", type = ExecutorType.USER, description = "The help command.")
    private void help(User user, MessageChannel channel) {
        EmbedBuilder eb = new EmbedBuilder();
        eb.setTitle("Commands list:");
        eb.setColor(Secrets.EMBEDCOLOR);
        for(SimpleCommand command : cmdMap.getCommands()) {
            String input = command.getName();
            eb.addField(input.substring(0, 1).toUpperCase() + input.substring(1), command.getDescription(), false);
        }
        if(!user.hasPrivateChannel()) user.openPrivateChannel().complete();
        ((UserImpl)user).getPrivateChannel().sendMessage(eb.build()).queue();
        channel.sendMessage(user.getAsMention() + ", I've sent a copy of the commands to our private channel.").queue();
    }
    
    @Command(name = "lore", type = ExecutorType.USER, description = "!!SPOILERS!! Displays the background of the character this bot is base on.")
    private void lore(User user, TextChannel tc, JDA jda) {
        eb.setAuthor(user.getName(), null, user.getAvatarUrl());
        eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
        eb.addField("Name", "Kazuki Kazami", true);
        eb.addField("Alias", "Thanatos", true);
        eb.addBlankField(false);
        eb.addField("\n!!WARNING SPOILERS!!", "Kazuki Kazami is Yuuji Kazami's elder sister who disappeared when Yuuji was ten years old. Despite her delicate and diminutive body, she is so intelligent that she can be called a genius. She was the same age as Amane Suou. They both went to the same school, “Takizono Private Academy”, and were on the basketball team. She \"died\" in a bus accident which greatly influences Yuuji's and Amane's life. After her \"death\", her mind was integrated with the Thanatos System by CIRS. Later on, it was found that she still has a functioning body.", false);
        eb.setFooter("kazuki.lore()", null);
        eb.setColor(Secrets.EMBEDCOLOR);
        tc.sendMessage(eb.build()).queue();
        eb.clearFields();
    }
    
    @Command(name = "purge", type = ExecutorType.USER, description = "Removes an amount of messages in a test channel [Usage: ..purge (number)]")
    private void purge(User user, Guild guild, TextChannel tc, JDA jda, String context) {
        if(guild == null) return;
        int number;
        try {
            number = Integer.parseInt(context.substring(6));
        } catch (Exception e) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle("No Messages Deleted...");
            eb.setDescription("The number you gave me does not look like any number I know of, and I am a computer.");
            eb.setFooter("kazuki.purge()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            tc.sendMessage(eb.build()).queue();
            eb.clearFields();
            return;
        }

        if(number < 1) {
            eb.setAuthor(user.getName(), null, user.getAvatarUrl());
            eb.setThumbnail(jda.getSelfUser().getAvatarUrl());
            eb.setTitle("No Messages Deleted...");
            eb.setDescription("That number was less than 1. I cannot delete less than 1 messages.");
            eb.setFooter("kazuki.purge()", null);
            eb.setColor(Secrets.EMBEDCOLOR);
            tc.sendMessage(eb.build()).queue();
            eb.clearFields();
        } else {
            number++;
            if(number > 100) number = 100;
            // HAS A RETRIEVE FUTURE!!!! USE THIS INSTEAD OF CHOICE LISTENER? no...
            // Retrieve future is for going forward after jumping back to a specific point in chat time

            List<Message> msgh = new MessageHistory(tc).retrievePast(number).complete();
            for(int i = 0; i < msgh.size(); i ++) {
                if(msgh.get(i).getContentRaw().equals(context)) msgh.remove(i);
            }
            tc.deleteMessages(msgh).queue();
        }
    }
    
    @Command(name = "mimic", type = ExecutorType.USER, description = "Mimics what you tell me to")
    private void mimic(TextChannel channel, String context) {
        if(context == null) return;
        channel.sendMessage(context.substring(6)).queue();
    }
    
    
    // THIS IS STILL A W.I.P, I KNOW MY CODE IS BAD!!!!!!!!!
    @Command(name = "idle", type = ExecutorType.USER)
    private void idle(Guild guild, User user, TextChannel channel, String context) {
        String state = (context + "-placeholder").replaceFirst("idle ", "").toLowerCase();
        switch (state) {
            case "state-placeholder":
                channel.sendMessage("Idle is currently " + cmdMap.getManager().getPlayer(guild).idle + " for your server.").queue();
                break;
            case "true-placeholder":
            case "on-placeholder":
                if (cmdMap.getManager().getPlayer(guild).idle) {
                    channel.sendMessage("Idle is already on for your server!").queue();
                } else {
                    channel.sendMessage("Idle has been turned on for your server.").queue();
                    cmdMap.getManager().getPlayer(guild).idle = true;
                }
                break;
            case "false-placeholder":
            case "off-placeholder":
                if (cmdMap.getManager().getPlayer(guild).idle) {
                    channel.sendMessage("Idle has been turned off for your server.").queue();
                    cmdMap.getManager().getPlayer(guild).idle = false;
                } else {
                    channel.sendMessage("Idle is already off for your server!").queue();
                }
                break;
            default:
                channel.sendMessage("Usage: ..idle [on/off]").queue();
                break;
        }
    }
}
