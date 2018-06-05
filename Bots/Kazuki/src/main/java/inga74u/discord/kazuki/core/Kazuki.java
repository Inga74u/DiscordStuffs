package inga74u.discord.kazuki.core;

import inga74u.discord.kazuki.commands.CommandMap;
import inga74u.discord.kazuki.event.DiscordListener;
import inga74u.discord.kazuki.util.Secrets;
import net.dv8tion.jda.core.AccountType;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDABuilder;
import javax.security.auth.login.LoginException;

public class Kazuki implements Runnable {
    private boolean running;
    private JDA jda;
    private CommandMap cmdMap;
    
    public Kazuki() throws LoginException {
        cmdMap = new CommandMap(this);
        jda = new JDABuilder(AccountType.BOT).setToken(Secrets.TOKEN).buildAsync();
        jda.addEventListener(new DiscordListener(cmdMap));
    }
    
    @Override
    public void run() {
        // Space for a logger if you want one. I didn't so this is left blank.
    }
    
    public JDA getJda() {
        return jda;
    }
    
    public void terminate() {
        running = false;
        jda.shutdown();
    }
}
