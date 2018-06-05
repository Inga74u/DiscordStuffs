package inga74u.discord.kazuki.commands;

import inga74u.discord.kazuki.audio.MusicCommands;
import inga74u.discord.kazuki.audio.MusicManager;
import inga74u.discord.kazuki.core.Kazuki;
import inga74u.discord.kazuki.idle.Idle;
import inga74u.discord.kazuki.util.Secrets;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.entities.*;
import java.lang.reflect.Method;
import java.lang.reflect.Parameter;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class CommandMap {
    private Map<String, SimpleCommand> commands = new HashMap<>();
    private Kazuki kazuki;
    private MusicManager manager;
    private Idle idle;
    public int idleStatus;
    
    public CommandMap(Kazuki kazuki) {
        manager = new MusicManager();
        this.kazuki = kazuki;
        registerCommands(new StandardCommands(this), new MusicCommands(this));
    }
    
    public String getPrefix() {
        return Secrets.PREFIX;
    }
    
    public void idle(int status) {
        switch(status) {
            case 0:
                idle.terminate();
                idle = null;
                break;
            case 1:
                idle = new Idle(manager);
                new Thread(idle).start();
                break;
            defult:
                System.out.println("Idle must be either 0 or 1");
                break;
        }
    }
    
    public MusicManager getManager() {
        return manager;
    }
    
    public Collection<SimpleCommand> getCommands() {
        return commands.values();
    }
    
    private void registerCommands(Object...cmds) {
        for(Object cmd : cmds) {
            for(Method method : cmd.getClass().getDeclaredMethods()) {
                if(method.isAnnotationPresent(Command.class)) {
                    Command fcmd = method.getAnnotation(Command.class);
                    method.setAccessible(true);
                    SimpleCommand scmd = new SimpleCommand(fcmd.name, fcmd.description(), fcmd.type(), cmd, method);
                    commands.put(fcmd.name(), scmd);
                }
            }
        }
    }
    
    public boolean cmdFromUser(User user, String cmd, Message msg) {
        Object[] tcmd = getCommand(cmd);
        if(tcmd[0] == null || ((SimpleCommand) tcmd[0]).getExecutorType() != Command.ExecutorType.USER) return false;
        try {
            execute(((SimpleCommand) tcmd[0]), cmd, (String[]) tcmd[1], msg);
        } catch(Exception e) {
            System.out.println("That command didn't work");
            e.printStackTrace();
        }
        return true;
    }
    
    private Object[] getCommand(String cmd) {
        String[] cmdSplit = cmd.split(" ");
        String[] args = new String[cmdSplit.length - 1];
        System.arraycopy(cmdSplit, 1, args, 0, cmdSplit.length - 1);
        SimpleCommand scmd = commands.get(cmdSplit[0]);
        return new Object[]{scmd, args};
    }
    
    private void execute(SimpleCommand scmd, String cmd, String[] args, Message msg) throws Exception {
        Parameter[] params = scmd.getMethod().getParameters();
        Object[] objects = new Object[params.length];
        for(int i = 0; i < params.length; i++) {
            if(params[i].getType() == String[].class) objects[i] = args;
            else if(params[i].getType() == User.class) objects[i] = msg == null ? null : msg.getAuthor();
            else if(params[i].getType() == TextChannel.class) objects[i] = msg == null ? null : msg.getTextChannel();
            else if(params[i].getType() == PrivateChannel.class) objects[i] = msg == null ? null : msg.getPrivateChannel();
            else if(params[i].getType() == MessageChannel.class) objects[i] = msg == null ? null : msg.getChannel();
            else if(params[i].getType() == Guild.class) objects[i] = msg == null ? null : msg.getGuild();
            else if(params[i].getType() == String.class) objects[i] = cmd;
            else if(params[i].getType() == Message.class) objects[i] = msg;
            else if(params[i].getType() == JDA.class) objects[i] = kazuki.getJda();
            else if(params[i].getType() == Kazuki.class) objects[i] = kazuki;
        }
        scmd.getMethod().invoke(scmd.getObject(), objects);
    }
}
