const fontFactory = require('./factory/fontFactory');

fontFactory[process.argv[2]].process(process.argv[3]);
