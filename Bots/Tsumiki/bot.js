const discord = require('discord.js');
// Ideas proudly stolen from my good friend Katistic!

// Commands
var cmds = {};
var tcmds = {};

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
    var parsed = 0;
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
        }
    }

    if(parsed === 0) console.log("Unknown command!");
}

function parseTerminalCommand(context) {
    var args = context.split(" ");
    var parsed = 0;
    for(var i = 0; i < Object.keys(tcmds).length; i++) {
        if(tcmds[args[0]] != undefined) {
            tcmds[args[0]]['function'](context);
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

function preix(msg) { // I got lazy, I'll fix it later
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
    if(args[1] instanceof int) {
        msg.channel.send("First argument must be a number");
        return;
    }
    
    msg.channel.bulkDelete(args[1]);
}

function play(msg) {
    var args = msg.content.split(" ");
    if(args.length < 2) {
        msg.channel.send("Play requires more than 0 arguments");
        return;
    }
    
    if(!args[1].indexOf("youtube.com")) {
        msg.channel.send("1st argument must be a YouTube link");
        return;
    }
    //play stuff
}

// Main bot section
const miniwa = new discord.Client();
var guilds = {};

miniwa.on('ready', () => {
    miniwa.guilds.forEach(function (value, key, map) {
        guilds[key.toString()] = {
            'name': value.toString(),
            'prefix': "tsu."
            'player': ,
            'queue': []
        };
        console.log(guilds[key.toString()]['name'] + ": " + key.toString()); // Just to test that it's working
    });
});

miniwa.on('connect', connection => {

});

miniwa.on('message', msg => {
    if(msg.author.bot) return;
    if(msg.guild === null) return;
    if(!msg.content.startsWith(guilds[msg.guild.id]['prefix'])) return;
    parseCommand(msg);
});

createCommand("mimic", "Mimics what you tell me too. (Usage: mimic [text to mimic])", mimic);
createCommand("prefix", "Changes the prefix. (Usage: prefix [new prefix])", prefix);
createCommand("purge", "Deletes an amount of messages from a TextChannel. (Usage: purge [number of messages to purge])", purge);

/* This is also possible:

createCommand("funcName", "funcDesc", function(args) {
    // Do stuff
});

*/
miniwa.login('TOKEN');

const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (input) => {
    parseTerminalCommand(input);
});
