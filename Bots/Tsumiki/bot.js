const discord = require('discord.js');
// Ideas proudly stolen from my good friend Katistic!

// Commands
var cmds = {};

function createCommand(name, desc, func) {
    cmds[name] = {
        'desc': desc,
        'function': func
    }
}

function parseCommand(msg) {
    var args = msg.content.split(" ");
    var parsed = 0;
    for(var i = 0; i < Object.keys(cmds).length; i++) {
        if(cmds[args[0].slice(guilds[msg.guild.id]['prefix'].length)] != undefined) {
            cmds[args[0].slice(guilds[msg.guild.id]['prefix'].length)]['function'](msg);
            parsed = 1;
        }
    }

    if(parsed === 0) console.log("Unknown command!");
}

function mimic(msg) {
    var args = msg.content.split(" ");
    if(args.length < 2) {
        msg.channel.send("Mimic requires more than 0 arguments");
    } else {
        args.shift();
        msg.channel.send(args.join(" "));
    }
}



// Main bot section
const miniwa = new discord.Client();
var guilds = {};

miniwa.on('ready', () => {
    miniwa.guilds.forEach(function (value, key, map) {
        guilds[key.toString()] = {
            'name': value.toString(),
            'prefix': "tsu."
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

createCommand("mimic", "mimics", mimic);

/* This is also possible:

createCommand("funcName", "funcDesc", function(args) {
    // Do stuff
});

*/
miniwa.login('TOKEN');
