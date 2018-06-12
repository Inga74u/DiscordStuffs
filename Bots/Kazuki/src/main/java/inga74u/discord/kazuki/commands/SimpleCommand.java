package inga74u.discord.kazuki.command;

import java.lang.reflect.Method;

public final class SimpleCommand {
    private final String name, description;
    private final Command.ExecutorType executorType;
    private final Object object;
    private final Method method;
    
    SimpleCommand(String name, String description, Command.ExecutorType executorType, Object object, Method method) {
        super();
        this.name = name;
        this.description = description;
        this.executorType = executorType;
        this.method = method;
    }
    
    public String getName() {
        return name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public Command.ExecutorType getExecutorType() {
        return executorType;
    }
    
    public Object getObject() {
        return object;
    }
    
    public Method getMethod() {
        return method;
    }
}
