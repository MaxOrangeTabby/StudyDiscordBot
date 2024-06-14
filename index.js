// Discord module
const { Client, GatewayIntentBits } = require('discord.js');

// Client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.once('ready', () => {
    console.log('Bot online');
});

// DO NOT SHARE THIS AT ANY COST
client.login('MTI1MTAyNTgyNDIxMjE4OTMwNQ.GzqZ7V.6a3VtgjmH46_FPzCXQTJNUTLFnbuVpVOexCgWM');
