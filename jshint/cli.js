var cli = require('jshint/src/cli/cli'),
    defReporter = require("jshint/src/reporters/default").reporter,
    shelljs = require("jshint/node_modules/shelljs"),
    jsHint = require("./jshint").JSHINT;

cli.run = function (options) {
    var files = cli.gather(options),
        results = [],
        data = [];

    files.forEach(function(file) {
        cli.lint(file, results, options.config, data);
    });

    (options.reporter || defReporter)(results, data, {verbose: options.verbose});

    return results.length === 0;
};

cli.lint = function(file, results, config, data) {
    var buffer,
        globals,
        lintData;
    config = config || {};
    config = JSON.parse(JSON.stringify(config));
    if (config.globals) {
        globals = config.globals;
        delete(config.globals);
    }

    try {
        buffer = shelljs.cat(file);
    } catch (err) {
        cli.error("Can't open " + file);
        process.exit(1);
    }
    buffer = buffer.replace(/^\uFEFF/, ""); // Remove potential Unicode BOM.

    if (jsHint(buffer, config, globals) === false) {
        jsHint.errors.forEach(function (error) {
            if (error) {
                results.push({file: file, error: error});
            }
        });
    }

    lintData = jsHint.data();
    if (lintData) {
        lintData.file = file;
        data.push(lintData);
    }
};

module.exports = cli;
