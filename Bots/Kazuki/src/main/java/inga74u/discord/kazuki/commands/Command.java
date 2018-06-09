package inga74u.discord.kazuki.commands;

import java.lang.annotation.ElementType;
import java.lang.annotation.Rentention;
import java.lang.annotation.RententionPolicy;
import java.lang.annotation.Target;

@Target(value = ElementType.METHOD)
@Rentention(RetentionPolicy.RUNTIME)

public @interface Command {
  String name();
  String description() default "Description unset.";
  ExecutorType type() default ExecutorType.ALL;
  
  // This also had CONSOLE, for commands called from the Thanatos console. We don't need that in this project
  enum ExecutorType {
    ALL, USER
  }
}
