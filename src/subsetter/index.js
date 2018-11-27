
const shelljs = require('shelljs')
const path = require('path');
//process.env.PWD+"/lib/linux/x64//subset -i GreatVibes-Regular.otf -o outputfont -u 0041:0043 -u 0061:0063"
// Runnable command in terminal: ./subset -i GreatVibes-Regular.otf -o outputfont -u 0061:0063
function subset(inputFontFile, outPutFontFile, subsetRange, format) {
    console.log('input file path', inputFontFile);
    console.log('output file path', outPutFontFile);
    console.log('subsetRange', subsetRange);
    if (process.platform == 'darwin') {
        console.log('Mac platform')
        shelljs.exec(`${process.env.PWD}/lib/osx/subset -i ${inputFontFile} -o ${outPutFontFile} ${format} -u ${subsetRange}`)
    } else if (process.platform == 'linux') {
        console.log('Linux platform')
        shelljs.exec(`${process.env.PWD}/lib/linux/x64//subset -i ${inputFontFile} -o ${outPutFontFile} ${format} -u ${subsetRange}`)
    }
}

function subsetToWoff(inputFontFile, outPutFontFile, subsetRange) {
    subset(inputFontFile, outPutFontFile, subsetRange, '-woff');
}

function subsetToTTF(inputFontFile, outPutFontFile, subsetRange) {
    subset(inputFontFile, outPutFontFile, subsetRange, '-ttf');
}

function subsetToOTF(inputFontFile, outPutFontFile, subsetRange) {
    subset(inputFontFile, outPutFontFile, subsetRange, '-otf');
}

function subsetToEOT(inputFontFile, outPutFontFile, subsetRange) {
    subset(inputFontFile, outPutFontFile, subsetRange, '-eot');
}

function subsetToMultipleFormats(inputFontFile, outPutFontFile, subsetRange) {
    subset(inputFontFile, outPutFontFile, subsetRange, '-woff -eot -ttf -otf');
}
module.exports = {
    subsetToWoff,
    subsetToTTF,
    subsetToEOT,
    subsetToOTF,
    subsetToMultipleFormats,

}