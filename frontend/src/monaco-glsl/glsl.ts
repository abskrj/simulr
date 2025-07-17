/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

export const language = {
    // Set defaultToken to invalid to see what you do not tokenize yet
    defaultToken: 'invalid',

    keywords: [
        'asm',
        'break',
        'case',
        'catch',
        'class',
        'const',
        'continue',
        'default',
        'delete',
        'do',
        'else',
        'export',
        'extern',
        'false',
        'for',
        'if',
        'import',
        'in',
        'new',
        'operator',
        'private',
        'protected',
        'public',
        'return',
        'static',
        'super',
        'switch',
        'this',
        'throw',
        'true',
        'try',
        'volatile',
        'while',

        'define',
        'undef',
        'ifdef',
        'ifndef',
        'else',
        'elif',
        'endif',
        'error',
        'pragma',
        'version',
        'extension',

        'layout',
        'location',
        'binding',
        'shared',
        'packed',
        'std140',
        'std430'
    ],

    typeKeywords: [
        'bool',
        'double',
        'float',
        'int',
        'uint',
        'void',
        'vec2',
        'vec3',
        'vec4',
        'dvec2',
        'dvec3',
        'dvec4',
        'bvec2',
        'bvec3',
        'bvec4',
        'ivec2',
        'ivec3',
        'ivec4',
        'uvec2',
        'uvec3',
        'uvec4',
        'mat2',
        'mat3',
        'mat4',
        'mat2x2',
        'mat2x3',
        'mat2x4',
        'mat3x2',
        'mat3x3',
        'mat3x4',
        'mat4x2',
        'mat4x3',
        'mat4x4',
        'dmat2',
        'dmat3',
        'dmat4',
        'dmat2x2',
        'dmat2x3',
        'dmat2x4',
        'dmat3x2',
        'dmat3x3',
        'dmat3x4',
        'dmat4x2',
        'dmat4x3',
        'dmat4x4',

        'sampler1D',
        'sampler2D',
        'sampler3D',
        'samplerCube',
        'sampler1DShadow',
        'sampler2DShadow',
        'samplerCubeShadow',
        'sampler1DArray',
        'sampler2DArray',
        'sampler1DArrayShadow',
        'sampler2DArrayShadow',
        'samplerBuffer',
        'sampler2DMS',
        'sampler2DMSArray',

        'isampler1D',
        'isampler2D',
        'isampler3D',
        'isamplerCube',
        'isampler1DArray',
        'isampler2DArray',
        'isamplerBuffer',
        'isampler2DMS',
        'isampler2DMSArray',

        'usampler1D',
        'usampler2D',
        'usampler3D',
        'usamplerCube',
        'usampler1DArray',
        'usampler2DArray',
        'usamplerBuffer',
        'usampler2DMS',
        'usampler2DMSArray',

        'sampler2DRect',
        'sampler2DRectShadow',
        'isampler2DRect',
        'usampler2DRect',

        'image1D',
        'image2D',
        'image3D',
        'imageCube',
        'image1DArray',
        'image2DArray',
        'imageBuffer',
        'image2DMS',
        'image2DMSArray',

        'iimage1D',
        'iimage2D',
        'iimage3D',
        'iimageCube',
        'iimage1DArray',
        'iimage2DArray',
        'iimageBuffer',
        'iimage2DMS',
        'iimage2DMSArray',

        'uimage1D',
        'uimage2D',
        'uimage3D',
        'uimageCube',
        'uimage1DArray',
        'uimage2DArray',
        'uimageBuffer',
        'uimage2DMS',
        'uimage2DMSArray'
    ],

    operators: [
        '=',
        '>',
        '<',
        '!',
        '~',
        '?',
        ':',
        '==',
        '<=',
        '>=',
        '!=',
        '&&',
        '||',
        '++',
        '--',
        '+',
        '-',
        '*',
        '/',
        '&',
        '|',
        '^',
        '%',
        '<<',
        '>>',
        '+=',
        '-=',
        '*=',
        '/=',
        '&=',
        '|=',
        '^=',
        '%=',
        '<<=',
        '>>='
    ],

    // we include these common regular expressions
    symbols: /[=><!~?:&|+\-*/^%]+/,
    escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,
    integersuffix: /(ll|LL|u|U|l|L)?/,
    floatsuffix: /[fFlL]?/,
    encoding: /u|u8|U|L/,

    // The main tokenizer for our languages
    tokenizer: {
        root: [
            // C++ 11 Raw String
            [/@encoding?R\"(?:([^ ()\\\t\r\n]+))\((?:.|\r|\n)*?\)\1\"/, 'string'],

            // identifiers and keywords
            [
                /[a-zA-Z_]\w*/,
                {
                    cases: {
                        '@typeKeywords': 'keyword.type',
                        '@keywords': 'keyword',
                        '@default': 'identifier'
                    }
                }
            ],

            // The preprocessor checks must be before whitespace as they check /^\s*#/ which
            // otherwise would be consumed by whitespace.

            // Preprocessor directive
            [/^\s*#\s*\w+/, 'keyword.directive'],

            // query type names that are not defined as keywords
            //
            // These are some of the less common GLSL keywords and may not be supported
            // by all environments. They also may be removed in future versions of GLSL.
            [
                /(subroutine|in|out|inout|uniform|varying|buffer|shared|coherent|volatile|restrict|readonly|writeonly|atomic_uint|layout|centroid|flat|smooth|noperspective|patch|sample|invariant|precise|lowp|mediump|highp|precision)\b/,
                'keyword'
            ],

            // whitespace
            { include: '@whitespace' },

            // delimiters and operators
            [/[{}()\[\]]/, '@brackets'],
            [
                /@symbols/,
                {
                    cases: {
                        '@operators': 'operator',
                        '@default': ''
                    }
                }
            ],

            // numbers
            [/\d*\d+[eE]([\-+]?\d+)?(@floatsuffix)/, 'number.float'],
            [/\d*\.\d+([eE][\-+]?\d+)?(@floatsuffix)/, 'number.float'],
            [/0[xX][0-9a-fA-F']*[0-9a-fA-F](@integersuffix)/, 'number.hex'],
            [/0[0-7']*[0-7](@integersuffix)/, 'number.octal'],
            [/0[bB][0-1']*[0-1](@integersuffix)/, 'number.binary'],
            [/\d[\d']*\d(@integersuffix)/, 'number'],
            [/\d(@integersuffix)/, 'number'],

            // delimiter: after number because of .\d floats
            [/[;,.]/, 'delimiter'],

            // strings
            [/"([^"\\]|\\.)*$/, 'string.invalid'], // non-teminated string
            [/"/, 'string', '@string'],

            // characters
            [/'[^\\']'/, 'string'],
            [/(')(@escapes)(')/, ['string', 'string.escape', 'string']],
            [/'/, 'string.invalid']
        ],

        comment: [
            [/[^\/*]+/, 'comment'],
            // [/\/\*/, 'comment', '@push' ],    // nested comment not allowed :-(
            ['\\*/', 'comment', '@pop'],
            [/[\/*]/, 'comment']
        ],

        string: [
            [/[^\\"]+/, 'string'],
            [/@escapes/, 'string.escape'],
            [/\\./, 'string.escape.invalid'],
            [/"/, 'string', '@pop']
        ],

        whitespace: [
            [/[ \t\r\n]+/, 'white'],
            [/\/\*/, 'comment', '@comment'],
            [/\/\/.*$/, 'comment']
        ]
    }
}; 