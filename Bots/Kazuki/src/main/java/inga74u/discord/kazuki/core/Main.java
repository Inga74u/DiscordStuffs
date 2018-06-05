package inga74u.discord.kazuki.core;

public class Main {
    public static void main(String[] args) {
        try {
            new Kazuki(dbo_terminateBot);
        } catch (LoginException le) {
            le.printStackTrace();
        }
    }
}
