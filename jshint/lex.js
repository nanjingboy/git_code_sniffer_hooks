var lexer = require("jshint/src/stable/lex.js").Lexer,
    state = require("jshint/src/stable/state.js").state,
    Token = {
        Identifier: 1,
        Punctuator: 2,
        NumericLiteral: 3,
        StringLiteral: 4,
        Comment: 5,
        Keyword: 6,
        NullLiteral: 7,
        BooleanLiteral: 8,
        RegExp: 9
    };

lexer.prototype.scanStringLiteral = function(checks) {
    /*jshint loopfunc:true */
    var quote = this.peek();

    // String must start with a quote.
    if (quote !== "\"" && quote !== "'") {
        return null;
    }

    // In JSON strings must always use double quotes.
    this.triggerAsync("warning", {
        code: "W108",
        line: this.line,
        character: this.char // +1?
    }, checks, function () { return state.jsonMode && quote !== "\""; });

    var value = "";
    var startLine = this.line;
    var startChar = this.char;
    var allowNewLine = false;

    this.skip();

    while (this.peek() !== quote) {
        while (this.peek() === "") { // End Of Line

            // If an EOL is not preceded by a backslash, show a warning
            // and proceed like it was a legit multi-line string where
            // author simply forgot to escape the newline symbol.
            //
            // Another approach is to implicitly close a string on EOL
            // but it generates too many false positives.

            if (!allowNewLine) {
                this.trigger("warning", {
                    code: "W112",
                    line: this.line,
                    character: this.char
                });
            } else {
                allowNewLine = false;

                // Otherwise show a warning if multistr option was not set.
                // For JSON, show warning no matter what.

                this.triggerAsync("warning", {
                    code: "W043",
                    line: this.line,
                    character: this.char
                }, checks, function () { return !state.option.multistr; });

                this.triggerAsync("warning", {
                    code: "W042",
                    line: this.line,
                    character: this.char
                }, checks, function () { return state.jsonMode && state.option.multistr; });
            }

            // If we get an EOF inside of an unclosed string, show an
            // error and implicitly close it at the EOF point.

            if (!this.nextLine()) {
                this.trigger("error", {
                    code: "E029",
                    line: startLine,
                    character: startChar
                });

                return {
                    type: Token.StringLiteral,
                    value: value,
                    isUnclosed: true,
                    quote: quote
                };
            }
        }

        allowNewLine = false;
        var char = this.peek();
        var jump = 1; // A length of a jump, after we're done
                      // parsing this character.

        if (char < " ") {
            // Warn about a control character in a string.
            this.trigger("warning", {
                code: "W113",
                line: this.line,
                character: this.char,
                data: [ "<non-printable>" ]
            });
        }

        // Special treatment for some escaped characters.
        if (char === "\\") {
            this.skip();
            char = this.peek();
            switch (char) {
                case "'":
                    this.triggerAsync("warning", {
                        code: "W114",
                        line: this.line,
                        character: this.char,
                        data: [ "\\'" ]
                    }, checks, function () {return state.jsonMode; });
                    break;
                case "b":
                    char = "\b";
                    break;
                case "f":
                    char = "\f";
                    break;
                case "n":
                    char = "\n";
                    break;
                case "r":
                    char = "\r";
                    break;
                case "t":
                    char = "\t";
                    break;
                case "0":
                    char = "\0";

                    // Octal literals fail in strict mode.
                    // Check if the number is between 00 and 07.
                    var n = parseInt(this.peek(1), 10);
                    this.triggerAsync("warning", {
                        code: "W115",
                        line: this.line,
                        character: this.char
                    }, checks,
                    function () { return n >= 0 && n <= 7 && state.directive["use strict"]; });
                    break;
                case "u":
                    char = String.fromCharCode(parseInt(this.input.substr(1, 4), 16));
                    jump = 5;
                    break;
                case "v":
                    this.triggerAsync("warning", {
                        code: "W114",
                        line: this.line,
                        character: this.char,
                        data: [ "\\v" ]
                    }, checks, function () { return state.jsonMode; });

                    char = "\v";
                    break;
                case "x":
                    var	x = parseInt(this.input.substr(1, 2), 16);

                    this.triggerAsync("warning", {
                        code: "W114",
                        line: this.line,
                        character: this.char,
                        data: [ "\\x-" ]
                    }, checks, function () { return state.jsonMode; });

                    char = String.fromCharCode(x);
                    jump = 3;
                    break;
                case "\\":
                case "\"":
                case "/":
                    break;
                case "":
                    allowNewLine = true;
                    char = "";
                    break;
                case "!":
                    if (value.slice(value.length - 2) === "<") {
                        break;
                    }
                default:
                    break;
            }
        }

        value += char;
        this.skip(jump);
    }

    this.skip();
    return {
        type: Token.StringLiteral,
        value: value,
        isUnclosed: false,
        quote: quote
    };
};

module.exports = lexer;
