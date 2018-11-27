const subsetter = require('./../../src/subsetter');
const constants=require('./../../src/const');

function process(option){
    if (option === 'WOFF') {
        console.time('WOFF')
        subsetter.subsetToWoff(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`, `${constants.FONT_SUBSET_RANGE}`);
        console.timeEnd('WOFF')
    }else if (option === 'TTF') {
        console.time('TTF')
        subsetter.subsetToTTF(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`, `${constants.FONT_SUBSET_RANGE}`);
        console.timeEnd('TTF')
    }else if (option === 'OTF') {
        console.time('OTF')
        subsetter.subsetToOTF(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`, `${constants.FONT_SUBSET_RANGE}`);
        console.timeEnd('OTF')
    }else if (option === 'EOT') {
        console.time('EOT')
        subsetter.subsetToEOT(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`, `${constants.FONT_SUBSET_RANGE}`);
        console.timeEnd('EOT')
    }else if (option === 'MultipleFormats') {
        console.time('MultipleFormats')
        subsetter.subsetToMultipleFormats(`${constants.ROOT_PROJECT_PATH}/input/${constants.FONT_FILE_NAME}`, `${constants.ROOT_PROJECT_PATH}/output/${option}`, `${constants.FONT_SUBSET_RANGE}`);
        console.timeEnd('subsetToMultipleFormats')
    }else {
        console.log('Use npm start <subset TTF|subset OTF|subset EOT|subset WOFF|subset MutipleFormats>');
    }
}
module.exports={
    process,
}