const net = require('net');
const readline = require('readline');

const client = new net.Socket();

client.connect(8084, 'localhost', () => {
    UI.showAlert('Подключено к серверу.')
    UI.showHint(`Введите /help чтобы посмотреть список команд`)
});

client.on('data', (data) => {
    const {username, message, action} = JSON.parse(data.toString())
    if(action){
        UI.showAction(username, action)
    } else{
        UI.showMessage(username, message)
    }
});

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let isSettingNewName = false

rl.on('line', (input) => {
    switch (input) {
        case '/help':
            UI.showHelp()
            break
        case '/exit':
            client.end();
            rl.close()
            break
        case '/rename':
            isSettingNewName = true
            UI.showAlert('Введите новое имя или "/" для отмены:')
            break
        default:
            if(isSettingNewName){
                isSettingNewName = false
                if(input !== '/') client.write('/name ' + input)
            }else{
                client.write(input);
            }
    }
});

class UI{
    static _systemMessage(message){
        return `\x1b[35m${message}\x1b[0m`
    }

    static _systemAlert(message){
        return `\x1b[33m${message}\x1b[0m`
    }

    static _systemHint(message){
        return `\x1b[90m${message}\x1b[0m`
    }

    static _userName(username){
        return `\x1b[32m${username}\x1b[0m`
    }

    static _message(message){
        return `\x1b[34m${message}\x1b[0m`
    }

    static _action(message){
        return `\x1b[37m${message}\x1b[0m`
    }

    static showAlert(message){
        console.log(UI._systemAlert(message))
    }

    static showHint(message){
        console.log(UI._systemHint(message))
    }

    static showHelp(){
        console.log(UI._systemMessage('/rename - сменить имя.'))
        console.log(UI._systemMessage('/exit - закрыть соединение.'))
    }

    static showMessage(userName, message){
        console.log(`${UI._userName(userName)}: ${UI._message(message)}`)
    }

    static showAction(userName, acton){
        console.log(`${UI._userName(userName)}: ${UI._action(acton)}`)
    }
}