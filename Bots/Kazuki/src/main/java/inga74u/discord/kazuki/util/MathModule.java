package inga74u.discord.kazuki.util;

import java.text.SimpleDateFormat;
import java.util.Calendar;

public class MathModule {
    public static String getCurrentTime() {
        Calendar cal = Calendar.getInstance();
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
        String time = sdf.format(cal.getTime());
        return "[" + time + "]";
    }

    public static String convertTime(long milliseconds) {
        long minutes = (milliseconds / 1000) / 60;
        long remainder = remainder(milliseconds);
        return minutes + " minutes and " + remainder + " seconds.";
    }

    public static String convertTime_Short(long milliseconds) {
        long minutes = (milliseconds / 1000) / 60;
        long remainder = remainder(milliseconds);
        return " (" + minutes + ":" + remainder + ")";
    }

    public static String processDuration(String duration) {
        //ref PT 00H 00M 00S
        String stage1 = duration.replace("PT", "");
        if(stage1.contains("H")) {
            if(stage1.contains("M")) {
                if(stage1.contains("S")) {
                    // 00H 00M 00S
                    String[] stage2 = stage1.split("M"); // 00H 00, 00S
                    String[] stage3 = stage2[0].split("H"); // 00, 00, 00S

                    String hours = stage3[0];
                    String minutes = stage3[1];
                    String seconds = stage2[1].replace("S", "");

                    if(seconds.length() == 1) {
                        seconds = ":0" + seconds;
                    } else {
                        seconds = ":" + seconds;
                    }

                    if(minutes.length() == 1) {
                        minutes = ":0" + minutes;
                    } else {
                        minutes = ":" + minutes;
                    }

                    return hours + minutes + seconds;

                    // if Doesn't contain seconds (00H00M)
                } else {
                    // 00H 00M
                    String stage2[] = stage1.split("H"); // 00, 00M

                    String hours = stage2[0];
                    String minutes = stage2[1].replace("M", "");
                    String seconds = ":00";

                    if(minutes.length() == 1) {
                        minutes = ":0" + minutes;
                    } else {
                        minutes = ":" + minutes;
                    }
                    return hours + minutes + seconds;
                }

                // if Doesn't contain minutes
            } else {
                if(stage1.contains("S")) {
                    // 00H 00S
                    String stage2[] = stage1.split("H"); // 00, 00M

                    String hours = stage2[0];
                    String minutes = ":00";
                    String seconds = stage2[1].replace("S", "");

                    if(seconds.length() == 1) {
                        seconds = ":0" + seconds;
                    } else {
                        seconds = ":" + seconds;
                    }
                    return hours + minutes + seconds;
                } else {
                    // 00H
                    return stage1.replace("H", "") + ":00:00";
                }
            }


            // if Doesn't contain hours
        } else {
            if(stage1.contains("M")) {
                if(stage1.contains("S")) {
                    // 00M 00S
                    String[] stage2 = stage1.split("M");

                    String minutes = stage2[0];
                    String seconds = stage2[1].replace("S", "");

                    if(seconds.length() == 1) {
                        seconds = ":0" + seconds;
                    } else {
                        seconds = ":" + seconds;
                    }

                    return minutes + seconds;
                } else {
                    // 00M
                    String minutes = stage1.replace("M", "");
                    String seconds = ":00";

                    return minutes + seconds;
                }
            } else {
                // 00S
                return stage1;
            }
        }
    }

    private static long remainder(long milliseconds) {
        return (milliseconds / 1000) % 60;
    }
}
