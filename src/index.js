const fontFactory = require('./factory/fontFactory');

console.log(process.argv[2]);
fontFactory[process.argv[2]].process(process.argv[3]);
