const discord = require('discord.js');
const ytdl = require('ytdl-core');
const miniwa = new discord.Client();const readline = require('readline');
const rl = readline.createInterface({input: process.stdin, output: process.stdout});

// Ideas proudly stolen from my good friend Katistic!

var guilds = {};
var cmds = {};
var tcmds = {};

// Commands
function createCommand(name, desc, func) {
    cmds[name] = {
        'desc': desc,
        'function': func
    }
}

function createTerminalCommand(name, desc, func) {
    tcmds[name] = {
        'desc': desc,
        'function': func
    }
}

function parseCommand(msg) {
    var args = msg.content.split(" ");
    for(var i = 0; i < Object.keys(cmds).length; i++) {
        if(cmds[args[0].slice(guilds[msg.guild.id]['prefix'].length)] != undefined) {
            if(args.length > 1) {
                if(args[1] === "-h" || args[1] === "-help" || args[1] === "-?") {
                    msg.channel.send(cmds[args[0].slice(guilds[msg.guild.id]['prefix'].length)]['desc']);
                    return;
                }
            }
            cmds[args[0].slice(guilds[msg.guild.id]['prefix'].length)]['function'](msg);
            parsed = 1;
            break;
        } else {
            console.log("Unknown command!")
            break;
        }
    }
}

function parseTerminalCommand(context) {
    var args = context.split(" ");
    var parsed = 0;
    for(var i = 0; i < Object.keys(tcmds).length; i++) {
        if(tcmds[args[0]] != undefined) {
            if(args.length > 1) {
                if(args[1] === "-h" || args[1] === "-help" || args[1] === "-?") {
                    console.log(tcmds[args[0]]['desc']);
                    return;
                }
            }
            tcmds[args[0]]['function'](context);
            break;
        } else {
            console.log("Unknown command!");
            break;
        }
    }
}

function mimic(msg) {
    var args = msg.content.split(" ");
    if(args.length < 2) {
        msg.channel.send("Mimic requires more than 0 arguments");
        return;
    }
    args.shift();
    msg.channel.send(args.join(" "));
}

function prefix(msg) {
    var args = msg.content.split(" ");
    if(args.length < 2) {
        msg.channel.send("Must have args");
        return;
    }
    guilds[msg.guild.id]['prefix'] = args[1];
    msg.channel.send("Prefix changed to: " + guilds[msg.guild.id]['prefix']);
}

function purge(msg) {
    var args = msg.content.split(" ");
    if(args.length < 2) {
        msg.channel.send("Purge requires more than 0 arguments");
        return;
    }

    parseInt(args[1]);
    if(args[1] instanceof Number) {
        msg.channel.send("First argument must be a number");
        return;
    }
    args[1]++;
    if(args[1] > 100) args[1] = 100;
    msg.channel.bulkDelete(args[1]);
}

// Music commands
function play(msg) {
    var args = msg.content.split(" ");
    if(args.length < 2) {
        msg.channel.send("Play requires more than 0 arguments");
        return;
    }

    if(!msg.member.voiceChannel) {
        msg.channel.send("You must be in a voice channel");
        return;
    }

    if(!args[1].indexOf("youtube.com")) {
        msg.channel.send("1st argument must be a YouTube link");
        return;
    }

    guilds[msg.guild.id]['queue'].push(args[1]);

    if(!msg.guild.voiceConnection) {
        msg.member.voiceChannel.join().then(function(connection) {
            _play(connection, msg);
        });
    }
}

function _play(connection, msg) {
    guilds[msg.guild.id]['player'] = connection.playStream(ytdl(guilds[msg.guild.id]['queue'][0], {filter: "audioonly"}));
    guilds[msg.guild.id]['player'].on('end', function() {
        console.log("repeat");
        guilds[msg.guild.id]['queue'].shift();
        if(guilds[msg.guild.id]['queue'][0]) {
            _play(connection, msg);
        }
    });
}

async function queue(msg) {
    var queue = [];
    queue.push("Songs currently in the queue:");
    var finalMsg = await msg.channel.send("Fetching queue info...");
    for(var i = 0; i < guilds[msg.guild.id]['queue'].length; i++){
        const info = await ytdl.getInfo(guilds[msg.guild.id]['queue'][i]);
        var sec = parseInt(info.length_seconds);
        var mins = Math.floor(sec / 60);
        var remainder = sec % 60;
        queue.push("`" + (i + 1) + "` " + info.title + " (" + mins + ":" + remainder + ")");
    }
    finalMsg.delete();
    msg.channel.send(queue.join("\n "));
}

function pause(msg) {
    if(!guilds[msg.guild.id]['player']) return;
    if(!guilds[msg.guild.id]['queue'][0]) {
        msg.channel.send("I can't pause nothing...");
        return;
    }
    guilds[msg.guild.id]['player'].pause();
    msg.channel.send("Player paused.");
}

function resume(msg) {
    if(!guilds[msg.guild.id]['player']) return;
    if(!guilds[msg.guild.id]['player'].paused()) {
        msg.channel.send("I'm not even paused!");
        return;
    }
}

function stop(msg) {
    if(!guilds[msg.guild.id]['player']) return;
    if(!guilds[msg.guild.id]['queue'][0]) {
        msg.channel.sent("What am I supposed to be stopping?");
        return;
    }
    guilds[msg.guild.id]['queue'] = [];
    guilds[msg.guild.id]['player'].end();
}

function skip(msg) {
    if(guilds[msg.guild.id]['player']) guilds[msg.guild.id]['player'].end();
}

function join(msg) {

}

function summon(msg) {
    if(!msg.member.voiceChannel) {
        msg.channel.send("You must be in a voice channel");
        return;
    }

    msg.member.voiceChannel.join();
}

function leave(msg) {
    if(!msg.guild.voiceConnection) {
        msg.channel.send("I'm not connected to any VoiceChannels...");
        return;
    }
    msg.guild.voiceConnection.disconnect();
}

// Terminal commands
function shutdown(context) {
    //var args = context.split(" ");
    miniwa.destroy();
    rl.close();
}

// Main bot section
miniwa.on('ready', () => {
    console.log("Online in these guilds: ");
    miniwa.guilds.forEach(function (value, key, map) {
        guilds[key.toString()] = {
            'name': value.toString(),
            'prefix': "tsu.",
            'player': undefined,
            'queue': [],
            'guildSettings': {
                'idle': false,
                'adminOnly': false,
                'adminOnlyMusic': false
            }
        };
        console.log("   " + guilds[key.toString()]['name'] + ": " + key.toString()); // Just to test that it's working
    });
});

miniwa.on('message', msg => {
    if(msg.author.bot) return;
    if(msg.guild === null) return;
    if(guilds[msg.guild.id]['guildSettings']['adminOnly'] /* and user doesn't have admin */) return;
    if(!msg.content.startsWith(guilds[msg.guild.id]['prefix'])) return;
    parseCommand(msg);
});

// Standard commands
createCommand("mimic", "Mimics what you tell me too. (Usage: mimic [text to mimic])", mimic);
createCommand("prefix", "Changes the prefix. (Usage: prefix [new prefix])", prefix);
createCommand("purge", "Deletes an amount of messages from a TextChannel. (Usage: purge [number of messages to purge])", purge);
//createCommand("idle", "Sets the state for idle voice lines for the guild (Usage: idle, idle [on or true / off or false])", idle);

// Terminal commands
createTerminalCommand("shutdown", "Shuts down the bot and ends the program.", shutdown);

//Music commands
createCommand("play", "Uses a link to play a song. (Usage: play [YouTube song link])", play);
createCommand("queue", "Lists the first 10 songs in the queue. (Usage: queue)", queue);
createCommand("pause", "Pauses the currently playing song. (Usage: pause)", pause);
createCommand("resume", "Resumes the currently paused song, if there is one. (Usage: resume)", resume);
createCommand("stop", "Stops the currently playing song and clears the queue. (Usage: stop)", stop);
createCommand("skip", "Skips the currently playing song and starts the next if there is one. (Usage: skip)", skip);
createCommand("join", "Joins the VoiceChannel you specify. (Usage: join [channel id])", join);
createCommand("summon", "Joins the VoiceChannel you are currently in. (Usage: join)", summon);
createCommand("leave", "Leaves the VoiceChannel. This stops the currently playing song and clears the queue (Usage: leave)", leave);

/* This is also possible:
createCommand("cmdName", "cmdDesc", function(args) {
    // Do stuff
});
*/

rl.on('line', (input) => {
    parseTerminalCommand(input);
});

miniwa.login('TOKEN');
