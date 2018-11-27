const converter = require('./../../src/converter');
const constants=require('./../../src/const');

function process(option) {
    console.log('converter process:'+option)
    console.log(`Root project path ${constants.ROOT_PROJECT_PATH}`)
    if (option === 'TTF') {
        console.time('TTF')
        converter.convertToTTF(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`)
        console.timeEnd('TTF')
    } else if (option === 'OTF') {
        console.time('OTF')
        converter.convertToOTF(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`)
        console.timeEnd('OTF')
    } else if (option === 'EOT') {
        console.time('EOT')
        converter.convertToEOT(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`)
        console.timeEnd('EOT')
    } else if (option === 'WOFF') {
        console.time('WOFF')
        converter.convertToWoff(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`)
        console.timeEnd('WOFF')
    } else if (option === 'MultipleFormats') {
        console.log(option)
        console.time('MultipleFormats')
        converter.convertToMultipleFormats(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`)
        console.timeEnd('MultipleFormats')
    } else {
        console.log('Use npm start <convert TTF|convert OTF|convert EOT|convert WOFF|convert MutipleFormats>');
    }
}

module.exports = {
    process,
}
